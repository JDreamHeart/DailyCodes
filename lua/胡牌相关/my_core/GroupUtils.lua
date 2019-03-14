local GroupUtilsLib = import(".GroupUtilsLib");

local GroupUtils = {};

GroupUtils.GroupType = {
	JIANG = 1,
	KE = 2,
	SHUN = 3,
};
GroupUtils.CardsType = {
	SAME = 1;
	SHUN = 2;
};
GroupUtils.GroupTCardLimit = {
	[GroupUtils.GroupType.JIANG] = 3,
	[GroupUtils.GroupType.KE] = 3,
	[GroupUtils.GroupType.SHUN] = 3,
};

GroupUtils.FuncConfig = {
	[GroupUtils.CardsType.SAME] = "findSame",
	[GroupUtils.CardsType.SHUN] = "findShun",
};

---将tb中的数据合并到sourceTb中
function GroupUtils:mergeToSourceTb(sourceTb,tb)
	for _,elem in ipairs(tb) do
		table.insert(sourceTb,elem);
	end
end

---创建groupInfo
function GroupUtils:createGroupInfo(groupType,beChange,isEnd)
 	local groupInfo = {
		groupType = groupType,
		beChange = beChange,
		isEnd = isEnd,
	};
	return groupInfo;
end

---根据传进来的beChange和类型，检查cardByte是否满足要求
function GroupUtils:isCardByteInBeChange(cardByte,beChange,cardsType)
	local bCType = type(beChange);
	if bCType == "table" then
		for _,byte in ipairs(beChange) do
            if GroupUtils.FuncConfig[cardsType] then
                return GroupUtilsLib[GroupUtils.FuncConfig[cardsType]](GroupUtilsLib,byte,cardByte);
            else
                assert(false,"没有配置查找"..tostring(cardsType).."类型的方法名！！");
            end
		end
	elseif bCType == "number" and beChange == -1 then
		return true;
	else
		assert(false,"传进来的beChange有问题！！！");
	end
	return false;
end

--查找组合的公共部分
function GroupUtils:findGroupSub(cardBeChange, groupBeChange, CardsType)
	local newCardBeChange = {};
	local bCType = type(cardBeChange);
	if bCType == "table" then
		local flag = false;
		for _,byte in ipairs(cardBeChange) do
			if self:isCardByteInBeChange(byte,groupBeChange,CardsType) then
				table.insert(newCardBeChange, byte);
				flag = true;
			end
		end
		if not flag then
			return {};
		end
	elseif bCType == "number" and cardBeChange == -1 then
		newCardBeChange = cardBeChange;
	else
		assert(false,"传进来的cardInfo有问题！！！");
	end
	return newCardBeChange;
end

---通过传的信息查找相同的group
function GroupUtils:findSameGroup(cardInfo,groupInfos)
	--校验数据标志
	local flag = false;
	--初始化返回数据
	local sameGroupInfos = {};
	--检测group
	for _,groupInfo in ipairs(groupInfos) do
		if groupInfo.groupType == -1 then
			--校验数据
			if flag then
				assert(false,"位置"..tostring(_).."：有两个相同类型的组合！！！");
			end
			flag = true; --设置标志

			--保存要返回的数据
			local newBechange = self:findGroupSub(cardInfo.beChange, groupInfo.beChange, self.CardsType.SAME);
			if #newBechange > 0 then
				table.insert(sameGroupInfos, self:createGroupInfo(self.GroupType.JIANG,newBechange,true));
				table.insert(sameGroupInfos, self:createGroupInfo(self.GroupType.KE,newBechange,false));
			end

		elseif groupInfo.groupType == self.GroupType.KE and groupInfo.isEnd == false then

			--校验数据
			if flag then
				assert(false,"位置"..tostring(_).."：有两个相同类型的组合！！！");
			end
			flag = true; --设置标志

			--保存要返回的数据
			local newBechange = self:findGroupSub(cardInfo.beChange, groupInfo.beChange, self.CardsType.SAME);
			if #newBechange > 0 then
				table.insert(sameGroupInfos, self:createGroupInfo(self.GroupType.KE,newBechange,true));
			end

		end
	end
	return #sameGroupInfos>0, sameGroupInfos;
end

---通过传的信息查找可组成顺子的group
function GroupUtils:findShunGroup(cardInfo,groupInfos)
	--校验数据标志
	local flag = false;
	--初始化返回数据
	local shunGroupInfos = {};
	--检测group
	for _,groupInfo in ipairs(groupInfos) do
		if groupInfo.groupType == -1 then
			--校验数据
			if flag then
				assert(false,"位置"..tostring(_).."：有两个相同类型的组合！！！");
			end
			flag = true; --设置标志

			--保存要返回的数据
			local newBechange = self:findGroupSub(cardInfo.beChange, groupInfo.beChange, self.CardsType.SHUN);
			if #newBechange > 0 then
				table.insert(shunGroupInfos, self:createGroupInfo(self.GroupType.SHUN,newBechange,false));
			end	

		elseif groupInfo.groupType == self.GroupType.SHUN and groupInfo.isEnd == false  then

			--校验数据
			if flag then
				assert(false,"位置"..tostring(_).."：有两个相同类型的组合！！！");
			end
			flag = true; --设置标志

			--保存要返回的数据
			local newBechange = self:findGroupSub(cardInfo.beChange, groupInfo.beChange, self.CardsType.SHUN);
			if #newBechange > 0 then
				table.insert(shunGroupInfos, self:createGroupInfo(self.GroupType.SHUN,newBechange,true));
			end

		end
	end
	return #shunGroupInfos>0, shunGroupInfos;
end

--通过Info信息查找group
function GroupUtils:findGroupByInfo(cardInfo,nodes)

	--如果还没有节点，直接返回true，不进行以下的逻辑
	if #nodes == 0 then
		local groupInfo = self:createGroupInfo(-1,cardInfo.beChange,false);
		return true,{groupInfo};
	end

	--开始检测group
	local groupInfos = {}
	local preNode = nodes[#nodes];

	--检测相同的组合
	local sameFlag,sameGroupInfos = self:findSameGroup(cardInfo,preNode.groupInfos);
	if sameFlag then
		self:mergeToSourceTb(groupInfos,sameGroupInfos);
	end

	--检测顺子的组合
	local shunFlag,shunGroupInfos = self:findShunGroup(cardInfo,preNode.groupInfos);
	if shunFlag then
		self:mergeToSourceTb(groupInfos,shunGroupInfos);
	end

	return #groupInfos>0,groupInfos;
end

return GroupUtils;