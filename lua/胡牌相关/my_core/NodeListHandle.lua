local GroupUtils = import(".GroupUtils");

local NodeListHandle = {};

function NodeListHandle:creatNode(cardInfo,groupInfos)
	local node = {
		tByte = cardInfo.tByte,
		nLaiZi = cardInfo.nLaiZi,
		groupInfos = groupInfos,
		nextNodes = {},
	};
	return node;
end

--检查节点信息
function NodeListHandle:checkInfo(cardInfo,nodes)
	local ret,groupInfos = GroupUtils:findGroupByInfo(cardInfo,nodes);
	if ret then
		local theNode = self:creatNode(cardInfo,groupInfos);
		table.insert(nodes,theNode);
	end
	return ret;
end
--重置节点信息
function NodeListHandle:resetInfo(cardInfo,nodes)
	--直接移除最后一个节点
	table.remove(nodes);
end

--创建节点链表
function NodeListHandle:creatNodesList(nodesList,nodes,marks,cardsInHand)
	for _,cardInfo in ipairs(cardsInHand) do
		if marks[cardInfo.tByte] == true then
			if self:checkInfo(cardInfo,nodes) then
				local lastNode = nodes[#nodes];
				nodesList[cardInfo.tByte] = lastNode;
				marks[cardInfo.tByte] = false;
				--递归遍历
				self:creatNodesList(nodesList[cardInfo.tByte].nextNodes,nodes,marks,cardsInHand);
				--重置数据
				marks[cardInfo.tByte] = true;
				self:resetInfo(cardInfo,nodes);
			end
		end
	end
end

--添加节点到节点链表中
function NodeListHandle:addNodeToNodesList(nodesList,cardInfo,nodes,marks,cardsInHand)
	local lastNode = nodes[#nodes];
	nodesList[cardInfo.tByte] = lastNode;
	marks[cardInfo.tByte] = false;
	--递归遍历
	self:creatNodesList(nodesList[cardInfo.tByte].nextNodes,nodes,marks,cardsInHand);
	--重置数据
	marks[cardInfo.tByte] = true;
end

--在已有的节点上添加节点
function NodeListHandle:toDoAddNode(nodesList,cardInfo,nodes,marks,cardsInHand)
	for tByte,node in pairs(nodesList) do
		if marks[tByte] == true then
			table.insert(nodes,{
				byte = node.byte,
				nLaiZi = node.nLaiZi,
				weight = node.weight,
			});
			marks[tByte] = false;
			if self:checkInfo(cardInfo,nodes) then
				self:addNodeToNodesList(nodesList,cardInfo,nodes,marks,cardsInHand);
				self:resetInfo(cardInfo,nodes);
			else
				self:toDoAddNode(node.nextNodes,cardInfo,nodes,marks,cardsInHand);
			end
			marks[tByte] = true;
			table.remove(nodes)
		end
	end
end

--在nodesList上创建cardInfo对应的节点，并补充后面的节点
function NodeListHandle:toDoAddNewNode(nodesList,cardInfo,nodes,marks,cardsInHand)
	if self:checkInfo(cardInfo,nodes) then
		self:addNodeToNodesList(nodesList,cardInfo,nodes,marks,cardsInHand);
		self:resetInfo(cardInfo,nodes);
	end
end

return NodeListHandle;