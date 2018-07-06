--[[--ldoc desc
@module main
@author JinZhang

Date   2018-07-06 16:04:16
Last Modified by   JinZhang
Last Modified time 2018-07-06 16:53:01
]]

require("_load");

local CharacterAcManager = require("CharacterAcManager");
g_CharacterAcManager = new(CharacterAcManager);

g_CharacterAcManager:onAction(); -- 玩家操作