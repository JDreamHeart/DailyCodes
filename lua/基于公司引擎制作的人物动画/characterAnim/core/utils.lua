-- @Author: JimZhang
-- @Date:   2018-07-07 09:32:43
-- @Last Modified by:   JimDreamHeart
-- @Last Modified time: 2018-07-07 18:28:02

local function copyGroup(group)
	local newGroup = {};
	table.copyTo(newGroup, group);
	return newGroup;
end

local function getArrayByNum(num)
	local arr = {};
	for i = 1, num do
		arr[i] = i;
	end
	return arr;
end

local function getFullArrangement(tb, params)
	-- 递归函数
	local function _fullArrange(tb, tbCount, groups, group, usedMap)
		for i = 1, tbCount do
			if not usedMap[i] then
				usedMap[i] = true;
				table.insert(group, tb[i]);
				if #group == tbCount then
					local newGroup = copyGroup(group);
					table.insert(groups, newGroup);
					if params.exCheckFunc then
						params.exCheckFunc(tb, params, groups, newGroup);
					end
				else
					_fullArrange(tb, tbCount, groups, group, usedMap);
				end
				table.remove(group);
				usedMap[i] = false;
			end
		end
	end

	local groups = {};
	_fullArrange(tb, #tb, groups, {}, {});

	return groups;
end

return {
	getArrayByNum = getArrayByNum,
	getFullArrangement = getFullArrangement,
}