--
-- Author: Your Name
-- Date: 2018-02-07 14:35:23
--

import("framework._load");
local BehaviorBase = import("BehaviorBase")
BehaviorFactory = import("BehaviorFactory");
local BehaviorExtend = import("BehaviorExtend");

function handler(obj, method)
    return function(...)
        if method and obj then
           return method(obj, ...)
        end    
    end
end

local ConfigLoadBehavior = class(BehaviorBase)
ConfigLoadBehavior.className_  = "ConfigLoadBehavior";

function ConfigLoadBehavior:ctor()
    ConfigLoadBehavior.super.ctor(self, "ConfigLoadBehavior", nil, 1)
end

function ConfigLoadBehavior:dtor()
	
end

---对外导出接口
ConfigLoadBehavior.exportInterface = {
    "loadGameConfig",
}

---对外暴露的接口
function ConfigLoadBehavior:loadGameConfig(object,data)
	print(99)
end

function ConfigLoadBehavior:bind(object)
    for i,v in ipairs(self.exportInterface) do
        object:bindMethod(self, v,   handler(self, self[v]),true);
    end
end

function ConfigLoadBehavior:unBind(object)
    for i,v in ipairs(self.exportInterface) do
        object:unbindMethod(self, v);
    end 
end

function ConfigLoadBehavior:reset(object)

end


local TESTBehavior = class(BehaviorBase)
TESTBehavior.className_  = "ConfigLoadBehavior";

function TESTBehavior:ctor()
    TESTBehavior.super.ctor(self, "TESTBehavior", {"ConfigLoadBehavior"}, 1)
end

function TESTBehavior:dtor()
	
end

---对外导出接口
TESTBehavior.exportInterface = {
    "loadGameConfig",
}

---对外暴露的接口
function TESTBehavior:loadGameConfig(object,data)
	print(2)
end

function TESTBehavior:bind(object)
	local v = "loadGameConfig"
	object:bindMethod(self, v,   handler(self, self[v]),true);
    -- for i,v in ipairs(self.exportInterface) do
    --     object:bindMethod(self, v,   handler(self, self[v]));
    -- end
end

function TESTBehavior:unBind(object)
    for i,v in ipairs(self.exportInterface) do
        object:unbindMethod(self, v);
    end 
end

function TESTBehavior:reset(object)

end

local map = {
	TESTBehavior = TESTBehavior;
	ConfigLoadBehavior = ConfigLoadBehavior;
}

BehaviorFactory.combineBehaviorsClass(map)


local obj = {};
BehaviorExtend(obj);

function obj:loadGameConfig(a)
	print(a);
end


local a = new(obj);

a:bindBehavior("TESTBehavior")
-- a:bindBehavior("ConfigLoadBehavior")
a:loadGameConfig(1)

-- a:unBindBehavior("ConfigLoadBehavior")
a:loadGameConfig(3)
