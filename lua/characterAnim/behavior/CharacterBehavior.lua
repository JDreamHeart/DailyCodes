--[[--ldoc desc
@module CharacterBehavior
@author JinZhang

Date   2018-07-06 15:45:33
Last Modified by   JinZhang
Last Modified time 2018-07-06 16:30:44
]]

local CharacterBehavior = class(BehaviorBase);
CharacterBehavior.className_  = "CharacterBehavior";

function CharacterBehavior:ctor()
    local depends = {
        "WalkBehavior",
    };
    CharacterBehavior.super.ctor(self, "CharacterBehavior", depends, 1);
end

function CharacterBehavior:dtor()
	
end

---对外导出接口
local exportInterface = {
    "onAction",
}

function CharacterBehavior:onAction(object, key, params)
    key = key or "walk";
    print("onAction("..key..")")
    if string.len(key) > 0 then
        local keyFirst = string.sub(key, 0, 1);
        local funcName = "on" .. string.gsub(key, keyFirst, string.upper(keyFirst), 1);
        if object[funcName] then
            object[funcName](object, params);
        end
    end
end

function CharacterBehavior:bind(object)
    for i,v in ipairs(exportInterface) do
        object:bindMethod(self, v, handler(self, self[v]),true);
    end
end

function CharacterBehavior:unBind(object)
    for i,v in ipairs(exportInterface) do
        object:unbindMethod(self, v);
    end 
end

return CharacterBehavior;