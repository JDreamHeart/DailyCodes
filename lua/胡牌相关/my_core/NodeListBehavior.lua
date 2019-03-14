local NodeListHandle = import(".NodeListHandle");

local M = {};

function M:getCardsInHandAndMarks(handCards)
	--获取手上的牌，从小到大排序，癞子默认最大
	local marks = {};  --用来保存是否遍历过的标记
	local cardsInHand = {};
	for _,card in ipairs(handCards.nativeCards) do
		marks[card.tByte] = true;
		table.insert(cardsInHand,{
				byte = card.byte,
				tByte = card.tByte,
				nLaiZi = false,
				beChange = {card.byte},
			});
	end
	table.sort(cardsInHand,function(a,b) return a.tByte < b.tByte; end);
	for _,card in ipairs(handCards.laiziCards) do
		marks[card.tByte] = true;
		table.insert(cardsInHand,{
				byte = card.byte,
				tByte = card.tByte,
				nLaiZi = true,
				--[[
				  beChange:
				  值为-1，表示可当作任何牌；
				  为0，表示只是不能当作本身；
				  为1个byte值，表示只能当做byte值的牌;
				  为1个table（里面有多张牌的byte值），表示可当作多张牌；
				]]
				beChange = -1,
			});
	end
	return cardsInHand,marks;
end


--初始化手牌的节点链表
function M:initNodesList(handCards)
	--获取手上的牌和标记数组
	local cardsInHand,marks = self:getCardsInHandAndMarks(handCards);

	--创建结点链表，并保存到handCards.nodeList中
	NodeListHandle:creatNodesList(handCards.nodesList,{},marks,cardsInHand,3);

end

--移除一个节点
function M:removeNode(nodesList,card)
	for tByte,node in pairs(nodesList) do
		if tByte == card.tByte then
			nodesList[node] = nil;
		else
			M:removeNode(node.nextNodes,card.tByte);
		end
	end
end

--添加一个节点【要在添加牌到手牌后，才调用此方法】
function M:addNode(nodesList,card,handCards)
	local cardInfo = {
		byte = card.byte,
		tByte = card.tByte,
		nLaiZi = card.nLaiZi,
		beChange = card.nLaiZi and card.beChange or {card.byte},
	};

	--获取手上的牌【转换后的数据】和marks
	local cardsInHand,marks = self:getCardsInHandAndMarks(handCards);

	--在已有的节点上添加节点
	NodeListHandle:toDoAddNode(nodesList,cardInfo,{},marks,cardsInHand);

	--在nodesList上创建cardInfo对应的节点，并补充后面的节点
	NodeListHandle:toDoAddNewNode(nodesList,cardInfo,{},marks,cardsInHand);

end

return M;