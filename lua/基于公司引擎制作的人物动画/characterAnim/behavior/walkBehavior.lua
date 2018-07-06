--[[--ldoc desc
@module WalkBehavior
@author JinZhang

Date   2018-07-06 15:50:35
Last Modified by   JinZhang
Last Modified time 2018-07-06 16:30:15
]]

local WalkBehavior = class(BehaviorBase);
WalkBehavior.className_  = "WalkBehavior";

function WalkBehavior:ctor()
    WalkBehavior.super.ctor(self, "WalkBehavior", nil, 1);
end

function WalkBehavior:dtor()
	
end

---对外导出接口
local exportInterface = {
    "onWalk",
}

function WalkBehavior:onWalk()
	print("to do walk !")
end

function WalkBehavior:bind(object)
    for i,v in ipairs(exportInterface) do
        object:bindMethod(self, v, handler(self, self[v]),true);
    end
end

function WalkBehavior:unBind(object)
    for i,v in ipairs(exportInterface) do
        object:unbindMethod(self, v);
    end 
end

return WalkBehavior;