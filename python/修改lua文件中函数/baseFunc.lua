--[[
    所要修改的函数汇总文件
    @author JinZhang
]]

REPLACE:

function Mahjong:removeOpCards(cards)
    for i = 1, #cards do
        local card = cards[i]
        local row, col = card:getMatrix()
        if card:isLaizi() then
            self.lz_matrix[row][-1] = self.lz_matrix[row][-1] - 1
        else
            self.matrix[row][-1] = self.matrix[row][-1] - 1
        end
    end
end

function MakeBehavior:makeOpGroup(object,user,opData)
    return user.handCards:makeOpGroup(opData.opcode, opData.card, opData.group);
end

function MakeBehavior:updateOpGroup(object,user,opData)
    local opcode = opData.opcode
    --根据card对象找到碰group ;
    local opGroup = user.handCards:getOpGroupByCard(opData.group[1]) ;
    table.insert(opGroup.opCards,opData.group[4]);
    user.handCards:remove(opData.group[4]);
    opGroup.opCode = opcode ;
    return false; --没有调用handCards:makeOpGroup，则返回false
end

function MakeBehavior:makeOrUpdateOpGroup(object,user,opData)

    --判断是否追杠的数值
    local groupLimitNum = 3
    if opData.opcode == OPE_ROW_3_GANG_4 or opData.opcode == OPE_SPECIAL_BU_GANG then
        groupLimitNum = 4
    end

    --判断是否追杠
    if #opData.group == groupLimitNum then      --幺杠、九杠、风杠、喜杠
        return user.handCards:makeOpGroup(opData.opcode, opData.card, opData.group);
    elseif #opData.group > groupLimitNum then   --追杠
        local opcode = opData.opcode
        local groupNum = #opData.group
        --根据card对象找到碰group ;
        local opGroup = user.handCards:getOpGroupByCard(opData.group[1]) ;
        table.insert(opGroup.opCards,opData.group[groupNum]);
        user.handCards:remove(opData.group[groupNum]);
        opGroup.opCode = opcode;
        return false; --没有调用handCards:makeOpGroup，则返回false
    else
        if opData.opcode == OPE_SHUANG_HUA_GANG and #opData.group == 2 then
            return user.handCards:makeOpGroup(opData.opcode, opData.card, opData.group);
        else
            error("opData.group错误！！")
        end
    end
end


ADD:

function gangLogic.toDoOpGroup(tableDB, user, opGroup, opCode)
    local object = tableDB.gameManager.m_stage;
    if object.className__ == "PlayCardStage" then
        local fucName = g_OpCodeConfig.makeFuc[opCode]
        if fucName then
            local newOpGroup = {};
            table.copyTo(newOpGroup, opGroup); --拷贝一份，防止影响原来的数据
            local opData = {  --构造opData
                doUser = user,
                opcode = opCode,
                card = newOpGroup[#newOpGroup],
                group = newOpGroup,
            };
            local ret,theOpGroup = object[fucName](object, user, opData);-- 调用函数
            assert(ret ~= nil, "所配置的函数，没有返回值！！！");
            if ret then
                return true,{},theOpGroup;
            end
        end
    end
    local removeTb = {};
    for k=1,#opGroup do
        if user.handCards:remove(opGroup[k]) then
            table.insert(removeTb, opGroup[k]);
        end
    end
    return false,removeTb;
end

function gangLogic.unDoOpGroup(tableDB, user, isDoneOpGroup, removeTb, theOpGroup)
    if isDoneOpGroup then
        user.handCards:undoOpGroup(tableDB, theOpGroup);
    elseif removeTb and #removeTb > 0 then
        for k=1,#removeTb do
            user.handCards:add(removeTb[k]);
        end
    end
end

REPLACE:

function gangLogic.checkCanGangAfterTing(params,ruleParams, resultData)
    local user = params.doUser;
    if user.isTing == 1 or user.isXiaoSaTing == 1 then
        local opGroups = resultData.opGroups;
        local handCards = params.doUser.handCards;
        local userTingCards = user.tingCards;
        for i=#opGroups,1,-1 do
            local isDoneOpGroup,removeTb,theOpGroup = gangLogic.toDoOpGroup(params.tableDB, user, opGroups[i], resultData.opCode);

            local ting_params = {};
            ting_params.tableDB = params.tableDB;
            ting_params.handCards = handCards;
            ting_params.doUser = user;
            local tmp_ting_cards, tmp_hu_groups = tingUtil.isTing(ting_params,true)
            local isCanGang;
            if #userTingCards > 0 and #userTingCards == #tmp_ting_cards then --如果能听的牌数相等并且一样则可以开杠
                isCanGang = true;
                for i=1,#userTingCards do
                    if userTingCards[i].byte ~= tmp_ting_cards[i].byte then
                        isCanGang = false;
                        break;
                    end 
                end
            end

            if not isCanGang then
                table.remove(opGroups,i);
            end

            gangLogic.unDoOpGroup(params.tableDB, user, isDoneOpGroup, removeTb, theOpGroup);
        end
    end
end

function gangLogic.checkCanAnGangAfterTing( params,ruleParams, resultData)
    local user = params.doUser;
        if user.isTing == 1 or user.isXiaoSaTing == 1 then
        local opGroups = resultData.opGroups;
        local handCards = params.doUser.handCards;
        local userTingCards = user.tingCards;
        
        if resultData.opCode == OPE_AN_GANG or resultData.opCode == OPE_HUA_GANG then
            for i=#opGroups,1,-1 do
                local isDoneOpGroup,removeTb,theOpGroup = gangLogic.toDoOpGroup(params.tableDB, user, opGroups[i], resultData.opCode);

                local ting_params = {};
                ting_params.tableDB = params.tableDB;
                ting_params.handCards = handCards;
                ting_params.doUser = user;
                local tmp_ting_cards, tmp_hu_groups = tingUtil.isTing(ting_params,true)
                local isCanGang;
                if #userTingCards == #tmp_ting_cards then --如果能听的牌数相等并且一样则可以开杠
                    isCanGang = true;
                    for i=1,#userTingCards do
                        if userTingCards[i].byte ~= tmp_ting_cards[i].byte then
                            isCanGang = false;
                            break;
                        end 
                    end
                end

                if not isCanGang then
                    table.remove(opGroups,i);
                end
                
                gangLogic.unDoOpGroup(params.tableDB, user, isDoneOpGroup, removeTb, theOpGroup);
            end
        else  
            for i=#opGroups,1,-1 do
                table.remove(opGroups,i);
            end 
        end
    end
end

function gangLogic.checkCanAnBuGangAfterTing( params,ruleParams, resultData)
    local user = params.doUser;
    if user.isTing == 1 or user.isXiaoSaTing == 1 then
        local opGroups = resultData.opGroups;
        local handCards = params.doUser.handCards;
        local userTingCards = user.tingCards;
        
        if resultData.opCode == OPE_AN_GANG or resultData.opCode == OPE_BU_GANG then
            for i=#opGroups,1,-1 do
                local isDoneOpGroup,removeTb,theOpGroup = gangLogic.toDoOpGroup(params.tableDB, user, opGroups[i], resultData.opCode);

                local ting_params = {};
                ting_params.tableDB = params.tableDB;
                ting_params.handCards = handCards;
                ting_params.doUser = user;
                local tmp_ting_cards, tmp_hu_groups = tingUtil.isTing(ting_params,true)
                local isCanGang;
                if #userTingCards == #tmp_ting_cards then --如果能听的牌数相等并且一样则可以开杠
                    isCanGang = true;
                    for i=1,#userTingCards do
                        if userTingCards[i].byte ~= tmp_ting_cards[i].byte then
                            isCanGang = false;
                            break;
                        end 
                    end
                end

                if not isCanGang then
                    table.remove(opGroups,i);
                end
                
                gangLogic.unDoOpGroup(params.tableDB, user, isDoneOpGroup, removeTb, theOpGroup);
            end
        else  
            for i=#opGroups,1,-1 do
                table.remove(opGroups,i);
            end 
        end
    end
end

function gangLogic.checkCanAnGangAfterFakeTing(params, ruleParams, resultData)
    local user = params.doUser;
    if user.isFakeTing == 1 and user.tingOpcode == OPE_TRY_FAKE_TING then
        local opGroups = resultData.opGroups;
        local handCards = params.doUser.handCards;
        local userTingCards = user.tingCards;
        if resultData.opCode == OPE_AN_GANG or resultData.opCode == OPE_BU_GANG then
            for i = #opGroups, 1, -1 do
                local isDoneOpGroup,removeTb,theOpGroup = gangLogic.toDoOpGroup(params.tableDB, user, opGroups[i], resultData.opCode);

                local ting_params = { };
                ting_params.tableDB = params.tableDB;
                ting_params.handCards = handCards;
                ting_params.doUser = user;
                local tmp_ting_cards, tmp_hu_groups = tingUtil.isTing(ting_params, true)
                local isCanGang;
                if #tmp_ting_cards > 0 then
                    -- 如果能听的牌数相等并且一样则可以开杠
                    isCanGang = true;
                end
                if not isCanGang then
                    table.remove(opGroups, i);
                end
                
                gangLogic.unDoOpGroup(params.tableDB, user, isDoneOpGroup, removeTb, theOpGroup);
            end
        else
            for i = #opGroups, 1, -1 do
                table.remove(opGroups, i);
            end
        end
    end
end

function gangLogic.checkGangAfterTing( params,ruleParams, resultData)
    local user = params.doUser
    if user.isTing == 1 then
        local opGroups = resultData.opGroups
        local handCards = params.doUser.handCards
        for i=#opGroups,1,-1 do
            local isDoneOpGroup,removeTb,theOpGroup = gangLogic.toDoOpGroup(params.tableDB, user, opGroups[i], resultData.opCode);

            local ting_params = {}
            ting_params.tableDB = params.tableDB
            ting_params.handCards = handCards
            ting_params.doUser = user
            local tmp_ting_cards, tmp_hu_groups = tingUtil.isTing(ting_params,true)
            if #tmp_ting_cards > 0 then

            else
                table.remove(opGroups,i)
            end

            gangLogic.unDoOpGroup(params.tableDB, user, isDoneOpGroup, removeTb, theOpGroup);
        end
    end
end

function gangLogic.checkGangAfterHu(params, ruleParams, resultData)
    local user = params.doUser;
    if user.status == g_GameConst.USER_STATE_TYPE.HUED then
        local opGroups = resultData.opGroups;
        local handCards = params.doUser.handCards;
        local userTingCards = user.tingCards;
        for i= #opGroups, 1, -1 do
            local isDoneOpGroup,removeTb,theOpGroup = gangLogic.toDoOpGroup(params.tableDB, user, opGroups[i], resultData.opCode);

            local ting_params = {};
            ting_params.tableDB = params.tableDB;
            ting_params.handCards = handCards;
            ting_params.doUser = user;
            local tmp_ting_cards, tmp_hu_groups = tingUtil.isTing(ting_params, true)
            local isCanGang;
            if #userTingCards > 0 and #userTingCards == #tmp_ting_cards then --如果能听的牌数相等并且一样则可以开杠
                isCanGang = true;
                for i = 1, #userTingCards do
                    if userTingCards[i].byte ~= tmp_ting_cards[i].byte then
                        isCanGang = false;
                        break;
                    end 
                end
            end

            if not isCanGang then
                table.remove(opGroups,i);
            end
            
            gangLogic.unDoOpGroup(params.tableDB, user, isDoneOpGroup, removeTb, theOpGroup);
        end
    end
end

