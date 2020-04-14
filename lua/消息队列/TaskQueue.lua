local tasklet = require("tasklet")
local TaskQueue = class(); -- 使用的是元表

function TaskQueue:ctor( ... )
	self:reset()
end

function TaskQueue:dtor( ... )
	self:reset()
end

function TaskQueue:reset()
	if self.m_curTask and self.m_curTask.coroutine then
		tasklet.cancel(self.m_curTask)
	end
	self.m_curTask = nil

	if self.m_timerEvent then
		self.m_timerEvent:cancel()
	end
	self.m_timerEvent = nil

	self.m_taskList = {}
	self.isRunning = false
end

function TaskQueue:run()
	self.isRunning = true
	if self.m_timerEvent then
		self.m_timerEvent:cancel()
	end
	self.m_timerEvent = schedule(function (dt)
		self:update(dt)
	end, nil, -1); -- 每帧执行一次
end

function TaskQueue:push(task, ...)
	if type(task) == "table" then
		assert(task.coroutine, "invalid task!!!");
		table.insert(self.m_taskList, task);
	else
		assert(type(task) == "function", "invalid task!!!");
		table.insert(self.m_taskList, {
			func = task, 
			args = {...},
		});
	end
	self:update();
end

function TaskQueue:unshift(task, ... )
	if type(task) == "table" then
		assert(task.coroutine, "invalid task!!!");
		table.insert(self.m_taskList, 1, task);
	else
		assert(type(task) == "function", "invalid task!!!");
		table.insert(self.m_taskList, 1, {
			func = task,
			args = {...},
		});
	end
	self:update();
end

function TaskQueue:pause( ... )
	Log.d("TaskQueue:pause")
	self.isRunning = false
end

function TaskQueue:resume( ... )
	Log.d("TaskQueue:resume")
	self.isRunning = true
end

function TaskQueue:getTaskSize( ... )
	return #self.m_taskList
end

function TaskQueue:update( dt )
	if self.m_curTask then
		if self.m_curTask.func then
			return
		elseif self.m_curTask.action and coroutine.status(self.m_curTask.coroutine) == "suspended" then
			return
		else
			self.m_curTask = nil
		end
	end

	if #self.m_taskList == 0 then
		return;
	end

	if self.isRunning then 
		local t = table.remove(self.m_taskList, 1);
		self.m_curTask = t
		if t.func then
			t.func(unpack(t.args));
			self.m_curTask = nil
		end
		self:update()
	end
end

return TaskQueue