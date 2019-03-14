--
-- 实现消息分发类相关接口，并编写测试用例，测试用例中能体现嵌套注册,不建议参考引擎的实现，自行思考如何实现
-- 重点：嵌套
-- Date: 2017-12-06 14:49:38
--


local EventDispatcher = {};


function EventDispatcher:ctor( ... )
    self.m_listeners = {};
    self.m_index = 0;
end

function EventDispatcher:dtor( ... )
    self.m_listeners = nil;
    self.m_index =nil;
end


function EventDispatcher:register(event,target,callback)
    if not self.m_listeners[event] then
        self.m_listeners[event] = {};
    end
    table.insert(self.m_listeners[event], {target = target, callback = callback});
end

function EventDispatcher:unRegister(event,target,callback)
    local listeners = self.m_listeners[event];
    if listeners then
        for i = #listeners,1,-1 do
            local listener = listeners[i];
            if target == listener.target and callback == listener.callback then
                table.remove(listeners,i);
            end
        end
        if #listeners == 0 then
            self.m_listeners[event] = nil;
        end
    end
end

function EventDispatcher:unRegisterByTaget(event,target,callback)
    local listeners = self.m_listeners[event];
    if listeners then
        for i = #listeners,1,-1 do
            local listener = listeners[i];
            if target == listener.target then
                table.remove(listeners,i);
            end
        end
        if #listeners == 0 then
            self.m_listeners[event] = nil;
        end
    end
end

function EventDispatcher:dispatch(event,data)
    assert(self.m_listeners[event], "没有注册event为" ..event.. "的事件!!!");
    for _,listener in ipairs(self.m_listeners[event]) do
        listener.callback(listener.target, data); 
    end
end



---编写测试用例,可以利用之前写的面向对象机制,下面只是参考，需要考虑消息unRegister嵌套问题，关于对象的概念可以拷贝引擎的object类，然后require
local function main( ... )
	g_EventDispatcher = new(EventDispatcher) -- EventDispatcher.Create();
	ClassA = class()
	function ClassA:ctor( ... )
		g_EventDispatcher:register("ClassA",self,self.test)
	end

	function ClassA:dtor( ... )
		g_EventDispatcher:dispatch("ClassB",{test = 1})
		g_EventDispatcher:unRegister("ClassA",self,self.test)
	end

	function ClassA:test( ... )
		local ClassB = new(ClassB,...);
	end


	ClassB = class()
	function ClassB:ctor( ... )
		g_EventDispatcher:register("ClassA",self,self.test)
		g_EventDispatcher:register("ClassB",self,self.test2)
	end
	function ClassB:dtor( ... )
		g_EventDispatcher:unRegisterByTaget(self)
	end

	function ClassB:test( ... )
		dump(" ClassB:test")
		delete(g_TextA);
	end

	function ClassB:test2( ... )
		dump(" ClassB:test2")
		delete(self);
	end



	local a = new(ClassA)
	g_TextA = a ;
	g_EventDispatcher:dispatch("ClassA",{test = 1})

end


-- return EventDispatcher;