--[[--数据对象访问接口DAO（Data Access Object）
@module DAO
@author YuchengMo

Date   2018-01-30 11:12:47
Last Modified by   YuchengMo
Last Modified time 2018-01-30 11:30:31
]]
--


local DAO = {};

function DAO:init()
	self.gameDataObjs = {};
	self.hallDataObjs = {};
	local mt = {
		__index = function(t,k,v)
			if self.hallDataObjs[k] then
				return self.hallDataObjs[k];
			end
			if self.gameDataObjs[k] then
				return self.gameDataObjs[k]
			end
		end
	}
	setmetatable(self,mt);
end

function DAO:addHallDataObject(key,obj)
	if self:isExist(key) == true then
		error("不能重复key " .. key)
	end
	self.hallDataObjs[key] = obj;
end

function DAO:isExist(key)
	if self.hallDataObjs[key] then
		return true;
	end
	if self.gameDataObjs[key] then
		return true;
	end
	return false;
end


function DAO:addGameDataObject(key,obj)
	if self:isExist(key) == true then
		error("不能重复key " .. key)
	end
	self.gameDataObjs[key] = obj;
end

--[[--
释放游戏数据对象
]]
function DAO:releaseDataObject()
	for k,v in pairs(self.gameDataObjs) do
		delete(v)
	end
end

return DAO;