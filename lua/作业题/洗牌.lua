local PokerConfig = {
	HUA_SE = {
		[1] = "方块",
		[2] = "梅花",
		[3] = "红桃",
		[4] = "黑桃",
	},
	DIAN_SHU = {
		[1]  = "3",
		[2]  = "4",
		[3]  = "5",
		[4]  = "6",
		[5]  = "7",
		[6]  = "8",
		[7]  = "9",
		[8]  = "10",
		[9]  = "J",
		[10] = "Q",
		[11] = "k",
		[12] = "A",
		[13] = "2",
	},
	WANG_IDX = 14,
	WANG_CARD = {
		[1] = "小王",
		[2] = "大王",
	},
};


local shuffleHandle = {};

--初始化牌
function shuffleHandle:initCards(cardNum)
	local mt = {
			__eq = function(a,b)
				return a.mByte == b.mByte;
			end,
			__lt = function(a,b)
				return a.mByte < b.mByte;
			end,
			__le = function(a,b)
				return a.mByte <= b.mByte;
			end,
			__tostring = function(tb)
				local retStr = "";
		    	if tb.mValue == PokerConfig.WANG_IDX then
		    		retStr = PokerConfig.WANG_CARD[tb.mType];
		    	else
		    		retStr = PokerConfig.HUA_SE[tb.mType]..PokerConfig.DIAN_SHU[tb.mValue];
		    	end
		        return retStr;
		    end,
		};
	for idx = 1,cardNum do
		--初始化牌
		local cardType = (idx-1) % 4 + 1;
		local cardValue = math.ceil(idx/4);
		local card = {
			mByte = cardValue * 0x10 + cardType,
			mType = cardType,
			mValue = cardValue,
		};
		--设置元表
		setmetatable(card, mt);
		--保存牌的数据
		table.insert(self.pokers, card);
	end
end

--初始化数据
function shuffleHandle:initData(cardNum,playerNum)
	--初始化基本属性
	self.pokers = {};
	self.players = {
		landlordPokers = {};
	};
	for i = 1,playerNum do
		self.players[i] = {};
	end
	self.playerNum = playerNum;

	--初始化牌
	self:initCards(cardNum)
end

--洗牌
function shuffleHandle:sheffle()
    local pokers = self.pokers;
    local pokersNum = #pokers;
    math.randomseed(tonumber(string.reverse(tostring(os.time())):sub(1,6))) --设置随机数种子
    for k = 1,#pokers do
        local random = math.random(pokersNum)
        pokers[k],pokers[random] = pokers[random],pokers[k] --交换数据
    end
end

--按顺序插入数据
-- local function insertTableByOrder(tb,elem,isDecending)
-- 	for i = #tb,1,-1 do
-- 		if isDecending and (not (tb[i] <= elem)) then
-- 			table.insert(tb, i+1, elem);
-- 			return;
-- 		elseif tb[i] < elem then
-- 			table.insert(tb, i+1, elem);
-- 			return;
-- 		end
-- 	end
-- 	table.insert(tb, 1, elem);
-- end

--发牌
function shuffleHandle:deal(reserveCardsNum)
	local players = self.players;
	local pokers = self.pokers;
	--开始发牌
    for i = #pokers,1,-1 do
        if i <= reserveCardsNum then
        	-- insertTableByOrder(players.landlordPokers, pokers[i]);
            table.insert(players.landlordPokers, pokers[i]);
        else
            local seatId = i % self.playerNum + 1;
        	-- insertTableByOrder(players[seatId], pokers[i]);
            table.insert(players[seatId], pokers[i]);
        end
    end
    --进行排序【耗时】
    for k,v in pairs(self.players) do
    	table.sort(v,function (a,b)
    		return a.mByte < b.mByte;
    	end);
    end
end

--[[
--创建打印用的元表
local function createCardPrint(_t)
	local cardsTb = {}
	--设置元表
	local mt = {
	    __index = function(tb,k)
	    	local card = _t[k];
	    	local retStr = "";
	    	if card.mValue == PokerConfig.WANG_IDX then
	    		retStr = PokerConfig.WANG_CARD[card.mType];
	    	else
	    		retStr = PokerConfig.HUA_SE[card.mType]..PokerConfig.DIAN_SHU[card.mValue];
	    	end
	        return retStr;
	    end,
	};
	setmetatable(cardsTb, mt);
	return cardsTb;
end
--设置Metatable
function shuffleHandle:toCreateCardPrint()
	local playersCards = {};
    for k,v in pairs(self.players) do
    	table.sort(v,function (a,b)
    		return a.mByte < b.mByte;
    	end);
    	playersCards[k] = createCardPrint(v);
    end
    return playersCards;
end
]]

--打印洗牌结果
function shuffleHandle:printResult(playersCards)
	local playCards = playersCards or self.players;
	for seatId,cards in ipairs(playCards) do
		print("玩家"..tostring(seatId).."：");
		local printStr = "";
		for i = 1,#self.players[seatId] do
			printStr = printStr..tostring(cards[i]).." ";
		end
		print(printStr.."\n");
	end
	print("地主牌：");
	local printStr = "";
	for i = 1,#self.players.landlordPokers do
		printStr = printStr..tostring(playCards.landlordPokers[i]).." ";
	end
	print(printStr.."\n");
end

--主函数
function shuffleHandle:main()
	self:initData(54,3);
	self:sheffle();
	self:deal(3);
	-- local playersCards = self:toCreateCardPrint();
 --    self:printResult(playersCards);
 	self:printResult();
end

--运行主函数
-- shuffleHandle:main();

--性能测试
shuffleHandle:initData(54,3);
local s = os.time();
local count = 100;
for i=1,count do
	shuffleHandle:sheffle();
	shuffleHandle:deal(3);
end
local e = os.time();

print((e-s)/count);