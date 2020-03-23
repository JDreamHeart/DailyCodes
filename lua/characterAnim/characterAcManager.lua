--[[--ldoc desc
@module CharacterAcManager
@author JinZhang

Date   2018-07-06 16:04:07
Last Modified by   JinZhang
Last Modified time 2018-07-06 16:38:05
]]

local CharacterAcManager = class();

BehaviorExtend(CharacterAcManager);

function CharacterAcManager:ctor()
	self:bindBehavior("CharacterBehavior");
end

function CharacterAcManager:dtor()

end

return CharacterAcManager;