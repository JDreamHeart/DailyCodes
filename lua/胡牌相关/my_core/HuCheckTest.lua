local NodeListBehavior = import(".NodeListBehavior")

local M = {};

local Debug = false;

function M:toCreateHandCardByBytes(bytes)
	local handCards = {
		nativeCards = {},
		laiziCards = {},
        nodesList = {},
	};
	local countMap = {};
	for _,byte in ipairs(bytes) do
		--生成tByte时使用
		if not countMap[byte] then
			countMap[byte] = 0;
		end
		countMap[byte] = countMap[byte] + 1;

		--根据byte初始化牌的相关数据
		local card = {
			byte = byte,
			tByte = byte * 0x0100 + countMap[byte];
		};
	end
    NodeListBehavior:initNodesList(handCards);
end

function M:test()
    local bytes = {1,1,2,2,3,3,4,4,5,5,6,6,7,7};
    self:toCreateHandCardByBytes(bytes);
end

return M;