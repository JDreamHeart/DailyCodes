--[[
	修改函数测试【只测试用，一般不使用该文件】
	@author JinZhang
]]

local ChouJiangLib = class("ChouJiangLib",GameObject);



---有玩家自摸胡时，从牌墙首翻开连续的4张牌。牌墙剩余牌张数不足时，剩几张翻几张。
function ChouJiangLib.tttest(object,fanCards)
	local limitCount = 4
	local settleConfig = object.m_tableDB:queryConfig("settleConfig");
    --抽奖牌张数
    local isEnable, params = g_RulesEngine.isEnable(object.m_tableDB, "choujiang100001");
    if params and params[1] then
        limitCount = params[1];
    end

    local endType = object.m_tableDB.params.endType;
    if endType == settleConfig.SettleType.ZiMo then
		local fanCards = {};
        local wall = object.m_tableDB.tableCards.cards;
        for i ,v in ipairs(wall) do
	        if i > limitCount then
		        break;
	        end 
            table.insert(fanCards,v)
        end
	    return fanCards
    end

    return {}
end

---对应规则 1，5，9，中 
function ChouJiangLib.defaultJiang(object,fanCards)
	local userJiangInfo = { }
	local allUser = object.m_tableDB.gameUsers:getAllUser();
	for _, user in ipairs (allUser) do
		local tempJiangInfo = {}
		if user.huCard.byte then 
			local huUser = user.nSeatId;
			local jiangCards = {};
			local jiangValue = 0;
			for _,fanCard in ipairs(fanCards) do
				local row,col = fanCard:getMatrix();
				if((row>=0 and row<=2) and (col == 1 or col ==5 or col ==9)) or(fanCard.byte == 0x41) then
					table.insert(jiangCards, fanCard.byte);
					jiangValue = jiangValue+1;
				end
			end
			tempJiangInfo.fanCards = fanCards
        	tempJiangInfo.huSeatId = huUser
        	tempJiangInfo.jiangCards = jiangCards
        	tempJiangInfo.jiangValue = jiangValue
        	userJiangInfo[huUser] = tempJiangInfo
   		else 
            userJiangInfo[user.nSeatId] = {}
        end
	end
	return userJiangInfo;
end

--对应规则方位抽奖
function ChouJiangLib.directionJiang(object,fanCards)
	local userJiangInfo = {};
	local curBanker = object.m_tableDB.curBanker;
	local huUser  = 0;
	local allUser = object.m_tableDB.gameUsers:getAllUser();
	local leftToBanker = (curBanker+3)%4;
	if leftToBanker ==0 then
		leftToBanker = 4;
	end
	local rightToBanker = curBanker%4+1;
	local oppositeToBanker = (curBanker+2)%4;
	if oppositeToBanker == 0 then
		oppositeToBanker = 4;
	end

    local function getJianginfo(huUser)
        local huUser = huUser
        local jiangCards = {};
	    local jiangValue = 0;
        local tempJiangInfo = {}
        --庄家胡牌的情况
	    if huUser == curBanker then
		    for _,fanCard in ipairs(fanCards) do
			    local row,col = fanCard:getMatrix()
			    if((row>=0 and row<=2) and (col == 1 or col ==5 or col ==9)) or(fanCard.byte ==0x31) then
				    table.insert(jiangCards,fanCard.byte);
				    jiangValue = jiangValue+1;
			    end
		    end
	    --庄家上家胡牌的情况
	    elseif huUser == leftToBanker then
		    for _,fanCard in ipairs(fanCards) do
			    local row,col = fanCard:getMatrix()
			    if((row>=0 and row<=2) and (col == 4 or col ==8 )) or(fanCard.byte ==0x34 or fanCard.byte == 0x43) then
				    table.insert(jiangCards,fanCard.byte);
				    jiangValue = jiangValue+1;
			    end
		    end
	    --庄家下家胡牌的情况
	    elseif huUser == rightToBanker then
		    for _,fanCard in ipairs(fanCards) do
			    local row,col = fanCard:getMatrix()
			    if((row>=0 and row<=2) and (col == 2 or col ==6 )) or(fanCard.byte ==0x32 or fanCard.byte == 0x41) then
				    table.insert(jiangCards,fanCard.byte);
				    jiangValue = jiangValue+1;
			    end
		    end
	    --庄家对家胡牌的情况
	    elseif huUser == oppositeToBanker then
		    for _,fanCard in ipairs(fanCards) do
			    local row,col = fanCard:getMatrix()
			    if((row>=0 and row<=2) and (col==3 or col ==7 )) or(fanCard.byte ==0x33 or fanCard.byte == 0x42) then
				    table.insert(jiangCards,fanCard.byte);
				    jiangValue = jiangValue+1;
			    end
		    end
	    end
        tempJiangInfo.fanCards = fanCards
        tempJiangInfo.huSeatId = huUser
        tempJiangInfo.jiangCards = jiangCards
        tempJiangInfo.jiangValue = jiangValue
        userJiangInfo[huUser] = tempJiangInfo
    end

    for _,user in ipairs (allUser) do 
		if user.huCard.byte then 
			huUser = user.nSeatId;
            getJianginfo(huUser)
		else 
            userJiangInfo[user.nSeatId] = {}
        end
	end
    return userJiangInfo
end

-- 对应规则区间抽奖
function ChouJiangLib.rangeJiang(object,fanCards )
	local jiangCards = {};
	local jiangValue = 0;
	for _,fanCard in ipairs(fanCards) do
		local row,col = fanCard:getMatrix()

		if((row>=0 and row<=2) and (col==1 or col ==2 or col==3 )) then 
			table.insert(jiangCards,fanCard);
			jiangValue = jiangValue+1;
		elseif((row>=0 and row<=2) and (col==4 or col ==5 or col==6 ))then
			table.insert(jiangCards,fanCard);
			jiangValue = jiangValue+2;
		elseif((row>=0 and row<=2) and (col==7 or col ==8 or col==9 ))then
			table.insert(jiangCards,fanCard);
			jiangValue = jiangValue+3;
		elseif(fanCard.value == 0x41) then
			table.insert(jiangCards,fanCard);
			jiangValue = jiangValue+4;
		end
	end
	return jiangCards,jiangValue;
end


--choujiang110001/choujiang300001 打牌流程开始前，从牌墙尾翻开连续的4张牌。
function ChouJiangLib.grabJiangTailCard(object)
   local cards = {}
   for i=1,4 do 
       local card = table.remove(object.m_tableDB.tableCards.cards,1) 
       table.insert(cards,card.tByte)
   end	
   return cards
end	

return ChouJiangLib;