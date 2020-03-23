--[[--ldoc desc
@module BehaviorMap
@author JinZhang

Date   2018-07-06 16:17:18
Last Modified by   JinZhang
Last Modified time 2018-07-06 16:50:15
]]
local CharacterBehavior = import(".CharacterBehavior");
local WalkBehavior = import(".WalkBehavior");

local BehaviorMap = {
	CharacterBehavior = CharacterBehavior,
	WalkBehavior = WalkBehavior;
};


BehaviorFactory.combineBehaviorsClass(BehaviorMap);

return BehaviorMap;