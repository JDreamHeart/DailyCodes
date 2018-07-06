--[[--MessageQueen 协议栈，所有麻将的消息先经过这里，每次弹一个消息出栈
@module MessageQueen
@author YuchengMo

Date   2017-12-20 11:34:59
Last Modified by   LensarZhang
Last Modified time 2018-04-09 16:48:40


]]

local packetId = 0


--使用方法： 在config/CMDOP.lua下配置
--wait等待动画执行
--interval持续执行
--delay 延时执行
local MessageQueen = {};
local g_EventDispatcher = BYKit.EventDispatcher

local default = {
	delay = 0,
}

function MessageQueen:ctor()
	self.m_msgQueen = {}; ---取包定时器
	if self.m_processHandler == nil then
		self.m_processHandler = g_Scheduler:scheduleUpdate(handler(self,self.processMessage));
	end
	-- if g_EventDispatcher and g_Event then
	-- 	g_EventDispatcher:register(g_Event.clearStack,self,self.clearStack)
	-- end
end

function MessageQueen:dtor()
	self.m_msgQueen = {}; ---取包定时器
	if self.m_processHandler then
		g_Scheduler:unSchedule(self.m_processHandler);
		self.m_processHandler = nil;
	end
	if g_EventDispatcher then
		g_EventDispatcher:unRegisterAllEventByTarget(self)
	end
end

---接收到消息
function MessageQueen:onRecv(cmd,data)

	if cmd == g_CMD.S2C.HEART_RESPONSE then
		g_EventDispatcher:dispatch(cmd,data);
		return;
	end

	local cmdStr = string.format("%02x", cmd);
	local flag = false;
	local key = nil;
	for k,v in pairs(g_CMD.S2C) do
		if v == cmd then
			flag = true;
			key = k;
			break;
		end
	end
	if flag == false then
		return;
	end
	packetId = packetId + 1;

	data.packetId__ = packetId;

	---生成协议配置数据
	local opConfig = checktable(g_CMD.op[cmd]);
	local op = clone(default);
	table.merge(op,opConfig);
	data.time__ = os.time();
	local msg = {cmd = cmd,data = data,op = op,_time = os.date("%m/%d/%y, %H:%M:%S", os.time())};
	table.insert(self.m_msgQueen,msg)

	if key then
		dumpToFile(key,msg)
	end



end

---处理消息,每帧取一个消息分发出去
function MessageQueen:processMessage(dt)
	if self.isDtor == true then
		return;
	end
	local msg = self.m_msgQueen[1];---取栈顶
	if msg == nil then
		return;
	end

	local cmd,data,op = msg.cmd,msg.data,msg.op;

	--如果配置了协议等待动画，则检索相应的动画是否播放完毕，播放完毕才取协议数据
	if op.wait then
		if not g_AnimManager then
			return
		end
		local anim = g_AnimManager:getAnim(op.wait)
		if anim then
		    assert(type(anim.isPlaying) == "boolean","协议等待动画必须有isPlaying变量，动画播放之前是false，调用play 置为true，结束为false，具体代码可以参考定庄动画")
			if anim.isPlaying == true then --正在播放动画
				-- assert(anim.isPlaying,"必须有isPlaying变量")
			else
				op.wait = nil;
			end
		else
			op.wait = nil;
		end
	else
		op.delay = op.delay -  dt;
		if op.delay <= 0 then
			if op.interval and type(op.interval) == "number" then
				if op.isDispatch == nil then
					g_EventDispatcher:dispatch(cmd,data);
					op.isDispatch = true;
				end
				op.interval = op.interval -  dt;
				if op.interval <= 0 then
					---数据出栈
					table.remove(self.m_msgQueen,1)		
				end
				return;
			else
				---数据出栈
				table.remove(self.m_msgQueen,1)
				---分发事件
				-- dump(data,cmd)
				g_EventDispatcher:dispatch(cmd,data);
			end
		end
	end

end

-- 清空协议队列
function MessageQueen:clearQueen( ... )
	if self.m_msgQueen then
		while table.remove(self.m_msgQueen,1) do
	    end
	end
end
return MessageQueen;

