--[[--ldoc desc
@module BY9HeadBehavior
@author 莫玉成

Date   2017-12-27
Last Modified by   YuchengMo
Last Modified time 2017-12-27 11:52:24
]]


local BY9HeadBehavior = class(BehaviorBase)
BY9HeadBehavior.className_  = "BY9HeadBehavior";

function BY9HeadBehavior:ctor()
    BY9HeadBehavior.super.ctor(self, "BY9HeadBehavior", nil, 1)
end

function BY9HeadBehavior:dtor()
	
end

---对外导出接口
local exportInterface = {
    "updateView",
}

---对外暴露的接口
function BY9HeadBehavior:updateView(object)

end

function BY9HeadBehavior:bind(object)
    for i,v in ipairs(exportInterface) do
        object:bindMethod(self, v,   handler(self, self[v]));
    end 
end



function BY9HeadBehavior:unBind(object)
    for i,v in ipairs(exportInterface) do
        object:unbindMethod(self, v);
    end 
end

function BY9HeadBehavior:reset(object)

end

return BY9HeadBehavior;