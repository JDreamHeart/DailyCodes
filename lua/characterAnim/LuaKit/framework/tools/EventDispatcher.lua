---
--扩展引擎底层的接口，方便项目调用
--@module EventDispatcher
--@author myc

-- 注消掉指定对象的所有监听

local EventDispatcher = {};

---
-- 构造函数.
function EventDispatcher:ctor()
	self.m_listener = {};
	self.m_tmpListener = {};
	self.m_userKey = Event.End;
end

function EventDispatcher:unRegisterAllEventByTarget(obj)
	if not obj then return end
	for event,v in pairs(self.m_listener) do
		local arr = v;
		for i=1,table.maxn(arr) do
			local listerner = arr[i];
			if listerner and (listerner["obj"] == obj) then
				self:unregister(event,obj,listerner.func);
			end
		end
	end
end

function EventDispatcher:cleanup()
	for event,listeners in pairs(self.m_tmpListener) do 
		self.m_listener[event] = self.m_listener[event] or {};
		local arr = self.m_listener[event];
		--for k,v in pairs(listeners) do 
		for i=1,table.maxn(listeners) do 
			local listener = listeners[i];
			if listener then
				arr[#arr+1] = listener;
				table.sort(arr,function(a,b)
					return a.priority > b.priority;
				end)
			end
		end
	end

	self.m_tmpListener = {};

	for _,listeners in pairs(self.m_listener) do
		--for k,v in pairs(listeners) do
		local removeTab = {};
		for i=1,table.maxn(listeners) do 
			local listener = listeners[i];
			if listener and (listener.mark == "EventState.RemoveMarked" or listener.func == nil) then 
				-- listeners[i] = nil;
				table.insert(removeTab,listener);
			end
		end
		for _,v in ipairs(removeTab) do
			for i,listener in ipairs(listeners) do
				if v==listener then
					table.remove(listeners,i);
					break;
				end
			end
		end
	end
end

function EventDispatcher:register(event, obj, func,priority)
	local arr;
	if self.m_dispatching then
		self.m_tmpListener[event] = self.m_tmpListener[event] or {};
		arr = self.m_tmpListener[event];
	else
		self.m_listener[event] = self.m_listener[event] or {};
		arr = self.m_listener[event];
	end
	priority = checkint(priority);
	arr[#arr+1] = {["obj"] = obj,["func"] = func,priority = priority};
	table.sort(arr,function(a,b)
		return a.priority > b.priority;
	end)
end


---
-- 清除注册事件.
-- 必须当obj和func都和注册事件时的相同时，才会取消注册。
-- 也就是说，可使用同一个函数与不同的obj配合注册多次。
-- 如：
--
--		local event = EventDispatcher.getInstance():getUserEvent()
--		local function eventResolver(obj,...)
--		
--		end
--		
--		local objA = {}
--		local objB = {}
--		EventDispatcher.getInstance():register(event, objA, eventResolver)
--		EventDispatcher.getInstance():register(event, objB, eventResolver)
--		EventDispatcher.getInstance():unregister(event, objA, eventResolver) -- 此步操作后，objB注册的事件依然有效
--
-- @param self
-- @param #number event 事件ID。
-- @param obj 注册事件时传入的obj。
-- @param #function func 注册事件时传入的回调函数。
function EventDispatcher:unregister(event, obj, func)
	if not self.m_listener[event] then return end; 

	local arr = self.m_listener[event] or {};
	--for k,v in pairs(arr) do 
	local removeCount = 0;
	for i=1,table.maxn(arr) do 
		local listerner = arr[i];
		if listerner then
			if (listerner["func"] == func) and (listerner["obj"] == obj) then 
				arr[i].mark = "EventState.RemoveMarked";
				
				if not self.m_dispatching then
					removeCount = removeCount + 1;
					if removeCount > 1 then
						error("存在多次移除情况")
					end
					table.remove(arr,i)
					-- break;
				end

				--don't break so fast now,take care of the dump event listener
				--return
			end
		end
	end
end



---
-- 派发消息事件.
-- 
-- @param self
-- @param #number event 事件ID。
-- @param ... 其他需要携带的参数，这些参数会传给@{#EventDispatcher.register}所注册的事件的回调函数。
-- @return #boolean 如果有此事件的接收者，并且所有处理函数都返回了true，则dispatch方法返回true。可以用来标识是否有回调函数实际响应这个消息。
function EventDispatcher:dispatch(event, ...)
	if not self.m_listener[event] then return end;

	self.m_dispatching = true;

	local ret = false;
	local listeners = self.m_listener[event] or {};
	--for _,v in pairs(listeners) do 
	for i=1,table.maxn(listeners) do 
		local listener = listeners[i]
		if listener then
			if listener["func"] and  listener["mark"] ~= "EventState.RemoveMarked" then 
				ret = ret or listener["func"](listener["obj"],...);
			end
		end
	end

	self.m_dispatching = false;

	self:cleanup();

	return ret;
end


function EventDispatcher:dtor( ... )
	self.m_listener = nil;
end


return EventDispatcher;