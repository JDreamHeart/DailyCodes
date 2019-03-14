local GroupUtils = import(".GroupUtils");
local NodeListBehavior = import(".NodeListBehavior");

local HuHandle = {};

---检测组合权重映射表
local function checkMarks(marks)
	for _,v in pairs(marks) do
		if v == true then
			return false;
		end
	end
	return true;
end

--[[--
	检测胡牌组合
	@params groupsMap = {
		"jiang" = 1; --将的个数
		"Ke" = 4;
		"shUn" = 4;
	}
]]
function HuHandle:parseGroupTypeMap(groupsMap)
	local groupTypeMap = {};
	for k,v in pairs(groupsMap) do
		local upperKey = string.upper(k);
		if GroupUtils.GroupType[upperKey] then
			groupTypeMap[GroupUtils.GroupType[upperKey]] = tonumber(v);
		else
			print("输入的groupsMap的key值【"..k.."】有误！！！");
		end
	end
	return groupTypeMap;
end

--检测huGroupInfos的胡牌番数信息，并转换成正常的mahjong中groups格式
function HuHandle:pauseToCheckHuGroups(huGroupInfos)
	return true,huGroupInfos;
end

---递归检测胡牌组合
function HuHandle:toCheckHuGroups(nodesList,marks,groupTypeMap,originNodesList,groupsList,huGroupInfos,tByteGroups,beChanges)
	for tByte,node in pairs(nodesList) do
		if marks[tByte] == true then
			table.insert(tByteGroups,tByte);
			--设置标志为false
			marks[tByte] = false;

			for _,groupInfo in ipairs(node.groupInfos) do
				table.insert(beChanges,groupInfo.beChange);
				--判断是否为胡牌所要的组合
				if groupInfo.isEnd and groupInfo.groupType > 0 and groupTypeMap[groupInfo.groupType] and groupTypeMap[groupInfo.groupType] > 0 then
					--设置相关信息

					table.insert(huGroupInfos,{tBytes = tByteGroups, beChanges = beChanges, groupType = groupInfo.groupType});
					groupTypeMap[groupInfo.groupType] = groupTypeMap[groupInfo.groupType] - 1;
					--如果能组合成胡牌的groups，保存groups
					if checkMarks(marks) then
						--暂停去检测胡牌组合
						local ret,newGroups = self:pauseToCheckHuGroups(huGroupInfos);
						if ret then
							table.insert(groupsList,newGroups);
						end
                    else
					    --递归遍历
					    self:toCheckHuGroups(originNodesList,marks,groupTypeMap,originNodesList,groupsList,huGroupInfos,{},{});
					end
					--重置相关信息
					groupTypeMap[groupInfo.groupType] = groupTypeMap[groupInfo.groupType] + 1;
					table.remove(huGroupInfos);
				else
					self:toCheckHuGroups(node.nextNodes,marks,groupTypeMap,originNodesList,groupsList,huGroupInfos,tByteGroups,beChanges);
				end
				table.remove(beChanges);
			end

			--重置标志为true
			marks[tByte] = true;
			table.remove(tByteGroups);
		end
	end
end

---检测胡牌组合
function HuHandle:checkHuGroups(handCards,groupsMap)
	--保存相关数据
	self.handCards = handCards;

	local originNodesList = handCards.nodesList;

	--获取手上的牌的标记数组
	local _,marks = NodeListBehavior:getCardsInHandAndMarks(handCards);

	local groupTypeMap = self:parseGroupTypeMap(groupsMap);

	--手牌的所有组合列表
	local groupsList = {};

	--递归遍历检测胡牌组合
    --[[
        存在问题：1.按照tByte值来遍历的话，会出现重复的组合情况，导致最后返回的胡牌组合列表groupsList 会非常大！！
                  2.必须要有过滤！！！【然而 还得仔细思考一下。。。】
    ]]
	self:toCheckHuGroups(originNodesList,marks,groupTypeMap,originNodesList,groupsList,{},{},{});

	return #groupsList, groupsList;
end

return HuHandle;