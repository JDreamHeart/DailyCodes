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

-- local mt0 = mat.create({1,2,3})
-- print(tostring(mt0))

-- local mt2 = mt0:T()
-- print(tostring(mt2))

-- local data = {
-- 	 2, 1,-5, 1,
-- 	 1,-3, 0,-6,
-- 	 0, 2,-1, 2,
-- 	 1, 4,-7, 6,
-- }
-- local mt1 = mat.create(data, 4, 4);

-- local data = {
-- 	 1, 2, 3,
-- 	 2, 2, 1,
-- 	 3, 4, 3,
-- }
-- local mt1 = mat.create(data, 3, 3);

local data = {
	 1, 0, 0, 0,
	 1, 2, 0, 0,
	 2, 1, 3, 0,
	 1, 2, 1, 4,
}
local mt1 = mat.create(data, 4, 4);

print(mt1:D())
print("_______________")
local d2 = mt1:I()
for i,v in ipairs(d2.data_) do
	d2.data_[i] = v * 24;
end
print(tostring(d2))