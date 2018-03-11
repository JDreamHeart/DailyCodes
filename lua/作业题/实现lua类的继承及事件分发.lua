----------------------------------------------------------------- 类的继承 ------------------------------------------------------------------

--[[
实例化对象通过create 销毁对象通过delete，继承通过class，
父类接口必须显示调用 不允许参考引擎的实现，
实现原理主要依据对lua元表的理解和百度的资料
]]

local Class = {};

function Class.create(obj)
    local newObj = {};
    local mt = {
        __index = obj,
        __newindex = function(tb,k,v)
            rawset(tb,k,v);
        end,
    };
    setmetatable(newObj, mt);
    newObj:ctor();
    return newObj;
end

function Class.delete(obj)
    -- local resetMetatable = function(o)
    --     local theMt = getmetatable(o);
    --     local theObj = theMt and theMt.__index;
    --     if theObj then
    --         theObj:dtor();
    --         resetMetatable(theObj);
    --     end
    -- end
    obj:dtor();
    setmetatable(obj, nil);
    -- resetMetatable(obj);
    -- setmetatable(obj, {__mode = "k"});
end

-- Class.mt = {
    -- __index = function(t,k)
    --     return _t[k];
    -- end,
    -- __newindex = function (t,k,v)
    --     _t[k] = v;
    -- end,
--     __call = Class.new;
-- };

function Class.init()
    local obj = {
        ctor = function() end,
        dtor = function() end,
    };
    return obj;
end

--设置Metatable
function Class.inherit(super,className)
    if type(super) ~= "table" then
        className = super;
        super = Class.init();
    end
    local obj = {};
    obj.super = super;
    --重置父类方法，防止出现死循环调用
    local superCtor = obj.super.ctor;
    obj.super.ctor = function(theSelf, ...)
        if theSelf and theSelf.className_ == super.className_ then
            superCtor(super, ...);
        else
            superCtor(super, theSelf, ...);
        end
    end
    local superDtor = obj.super.dtor;
    obj.super.dtor = function(theSelf, ...)
        if theSelf and theSelf.className_ == super.className_ then
            superDtor(super, ...);
        else
            superDtor(super, theSelf, ...);
        end
    end
    -- if type(obj) == "table" then
    --     obj.__index = super;
    -- end
    -- setmetatable(obj,Class.mt);
    obj.create = Class.create;
    obj.delete = Class.delete;
    obj.className_ = className;
    return obj;
end

-- return Class;

--程序运行

local function class(super,className)
    return Class.inherit(super,className)
end

-- local DDZCard = class("Card");

-- function DDZCard:ctor()
--     self.super.ctor(self)
-- end

-- function DDZCard:dtor()
--    self.super.dtor(self)
-- end

-- local obj = DDZCard:create()

-- obj:delete()


-------------------------------------------------------------------- 事件分发 --------------------------------------------------------------------

local EventDispatcher = class("101");


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
    -- for _,listener in ipairs(self.m_listeners[event]) do
    local listeners = self.m_listeners[event];
    for i = 1,#listeners do
        local listener = listeners[i];
        listener.callback(listener.target, data); 
    end
end



---编写测试用例,可以利用之前写的面向对象机制,下面只是参考，需要考虑消息unRegister嵌套问题，关于对象的概念可以拷贝引擎的object类，然后require
local function main( ... )

    g_EventDispatcher = EventDispatcher:create();

    ClassA = class("1001")
    function ClassA:ctor( ... )
        g_EventDispatcher:register("ClassA",self,self.test) --注册ClassA的test函数
    end

    function ClassA:dtor( ... )
        g_EventDispatcher:dispatch("ClassB",{test = 1})
        g_EventDispatcher:unRegister("ClassA",self,self.test)
        print("ClassA:dtor")
    end

    function ClassA:test( ... )
        print("ClassA:test")
        local ClassB = ClassB:create(...);
    end


    ClassB = class("1002")
    function ClassB:ctor( ... )
        print("ClassB:ctor")
        g_EventDispatcher:register("ClassA",self,self.test)  --注册ClassB的test函数
        g_EventDispatcher:register("ClassB",self,self.test2)
    end
    function ClassB:dtor( ... )
        g_EventDispatcher:unRegisterByTaget(self)
        print("ClassB:dtor")
    end

    function ClassB:test( ... )
        print(" ClassB:test")
        local data = ...;
        print(" ClassB:test__" .. data.test)
        g_TextA:delete();
    end

    function ClassB:test2( ... )
        print(" ClassB:test2")
        self:delete();
    end


    local a = ClassA:create();
    g_TextA = a ;
    g_EventDispatcher:dispatch("ClassA",{test = 1})

end

main( ... )