-- require("dump")
-- require("dumpToFile")

--打印matrix【必须是纯数据矩阵，且能用ipairs函数遍历完全】
local function dumpMatrix(matrix)
	local result = "matrix = {\n";
	local function _pairs_matrix(mt,count)
		local str = "";
		for k,v in ipairs(mt) do
			if type(v) == "table" then
				local tStr = string.rep("\t",count);
				local enterStr = "";
				local endTStr = "";
				if type(v[1]) == "table" then
					enterStr = "\n";
					endTStr = tStr;
				end
				str = str..tStr.."["..tostring(k).."] = {"..enterStr.._pairs_matrix(v,count + 1);
				str = str..endTStr.."},\n";
			else
				local subStr = "";
				if k > 1 then
					subStr = ",";
				end
				str = str..subStr..tostring(v);
			end
		end
		return str;
	end
	result = result.._pairs_matrix(matrix,1).."}\n";
	print(result)
end

--深度复制st，返回新的table【影响性能，谨慎使用】
local function copyTab(st)
    local tab = {}
    for k, v in pairs(st or {}) do
        if type(v) ~= "table" then
            tab[k] = v
        else
            tab[k] = copyTab(v)
        end
    end
    return tab
end
----------------------------------------------------------------
-- 正常题
-- 打印出所有10位数, 并且各个数位上(个位  十位  百位 千位 ...)的数字都不重复的数
function fun1()
	--打印的上限
	local count = 0;
	local countLimit = 20;
	--程序开始
	local minNum = 0;
	local maxNum = 9;
	local function _nodes_pairs(nodes,nodeMatrix,nodesList,minNum,maxNum)
		for i = minNum,maxNum do
			if nodeMatrix[i] == 1 and ((#nodes == 0 and i > 0) or #nodes > 0) then
				--将遍历结果保存起来
				table.insert(nodes,i);
				if #nodes == maxNum+1 then
					-- local numStr = ""
					-- for _,v in ipairs(nodes) do
					-- 	numStr = numStr..tostring(v)
					-- end
					table.insert(nodesList,tonumber(table.concat(nodes)));
					-- --简要测试
					-- count = count + 1;
					-- if count == countLimit then
					-- 	dumpMatrix(nodesList)
					-- 	error("")
					-- end
					-- -- 测试nodes
					-- local test = "";
					-- for _,vv in ipairs(nodes) do
					-- 	test = test..tostring(vv)..",";
					-- end
					-- print(tostring(count)..":"..test);
					-- --测试nodesList
					-- if count == countLimit then
					-- 	print(#nodesList)
					-- 	local count1 = 0
					-- 	for k,v in ipairs(nodesList) do
					-- 		local test = ""
					-- 		for _,vv in ipairs(v) do
					-- 			test = test..tostring(vv)
					-- 		end
					-- 		print(tostring(k)..":"..test)
					-- 		count1 = count1 + 1
					-- 		if count1 == countLimit then
					-- 			error("")
					-- 		end
					-- 	end
					-- 	error("");
					-- end
				end

				--递归遍历
				nodeMatrix[i] = 0;
				_nodes_pairs(nodes,nodeMatrix,nodesList,minNum,maxNum)
				nodeMatrix[i] = 1;
				table.remove(nodes);
			end
		end

	end
	--初始化数据
	local nodesList = {};--所有树节点列表
	local nodeMatrix = {};--节点矩阵（用来存储未遍历过的节点）
	for i = minNum,maxNum do
		nodeMatrix[i] = 1;
	end
	--进行递归
	_nodes_pairs({},nodeMatrix,nodesList,minNum,maxNum);

	print(#nodesList)
	for k,v in ipairs(nodesList) do
		print(tostring(k)..":"..tostring(v))
		count = count + 1
		if count == countLimit then
			error("")
		end
	end
end

-- 运行结果
fun1();
--[[
1234567890
...
1357924680
...
2458307916
...
...
...
9876543210
]]--


----------------------------------------------------------------
-- 附加题
-- 做一个字符串解析四则运算计算器
function fun2(str)
	-- if loadstring then
	-- 	return loadstring("return "..str)();  --lua语言的loadstring函数用法
	-- elseif load then
	-- 	return load("return "..str)();  --lua语言的load函数用法
	-- else
		local opFuncMap = {
			["+"] = function(a,b) return a+b; end;
			["-"] = function(a,b) return a-b; end;
			["*"] = function(a,b) return a*b; end;
			["/"] = function(a,b) return a/b; end;
		};
		local opWeight = {
			["+"] = 1;
			["-"] = 1;
			["*"] = 2;
			["/"] = 2;
		};
		local baseOpWeight = {
			["("] = 10;
			[")"] = 10;
		};
		
		---自想的方法【开始】---
		local stack = {};
		local opWeightStack = {};
		local baseWeight = 0;
		local isNumFlag = false;
		for i in string.gfind(str,"%S") do
			local stackLen = #stack;
		    local num = tonumber(i);
		    if not num then
		    	isNumFlag = false;
		        if i == "(" then
		            baseWeight = baseWeight + baseOpWeight[i];
		        elseif i == ")" then
		            baseWeight = baseWeight - baseOpWeight[i];
		        else
		        	if stackLen == 0 or stack[stackLen].numType == 1 then
		        		print("输入公式错误：操作符被放在首位，或者两个运算符之间没有数字！！")
		        	end
		    		table.insert(stack, {valStr = i, numType = 1, isDone = false});
		    		table.insert(opWeightStack, {index = stackLen+1, weight = baseWeight + opWeight[i]});
		        end
		    else
		    	if isNumFlag then
		    		stack[stackLen].valStr = stack[stackLen].valStr..i;
		    	else
			    	isNumFlag = true;
			    	table.insert(stack, {valStr = i, numType = 0, isDone = false, newVal = nil});
		    	end
		    end
		end
		table.sort(opWeightStack,function(a,b)
			if a.weight == b.weight then
				return a.index < b.index;
			else
				return a.weight > b.weight;
			end
		end);
		
		local stackLen = #stack;
		for _,v in ipairs(opWeightStack) do
			local preNumNode = stack[v.index - 1];
			local nextNumNode = stack[v.index + 1];
			local preNum = preNumNode.newVal or tonumber(preNumNode.valStr);
			local nextNum = nextNumNode.newVal or tonumber(nextNumNode.valStr);
			if not preNum or not nextNum then
				assert(false,"输入公式错误：操作符的前一个或者后一个数字有问题！！");
			end

			--重置stack上的相关节点数据
			local newNum = opFuncMap[stack[v.index].valStr](preNum,nextNum);
			stack[v.index - 1].isDone = true;
			stack[v.index].isDone = true;
			stack[v.index + 1].isDone = true;
			for idx = v.index - 1, 1, -1 do
				if stack[idx].isDone then
					if stack[idx].numType == 0 then
						stack[idx].newVal = newNum;
					end
				else
					break;
				end
			end
			for idx = v.index + 1, stackLen do
				if stack[idx].isDone then
					if stack[idx].numType == 0 then
						stack[idx].newVal = newNum;
					end
				else
					break;
				end
			end
		end
		return stack[1].newVal;

		---自想的方法【结束】---
		

		---网上搜的的思路【开始】---
		--[[
			网上搜的四则运算一般方法（后缀表达式）：
			1、遇到操作数：直接添加到后缀表达式中；
			2、栈为空时，遇到操作符，直接入栈；
			3、遇到左括号，将左括号入栈；
			4、遇到右括号，执行出栈操作，并将出栈元素添加到后缀表达式中，直到弹出的栈是左括号，不把左括号添加到后缀表达式；
			5、遇到其他运算符（加减乘除）：弹出所有优先级 >= 该操作符的栈顶元素，然后将该运算符入栈；
			6、最终将栈中的元素依次出栈，添加到后缀表达式。
		]]
		-- local tmpOpStack = {};
		-- local houZhuiList = {};
		-- local tempStr = "";
		-- for char in string.gfind(str,"%S") do
		-- 	if tonumber(char) then
		-- 		tempStr = tempStr..char;
		-- 	else
		-- 		if tempStr ~= "" then
		-- 			table.insert(houZhuiList,tonumber(tempStr));
		-- 		end
		-- 		if (#tmpOpStack == 0 and char ~= ")") or (tmpOpStack[#tmpOpStack] and tmpOpStack[#tmpOpStack] == "(") or char == "(" then
		-- 			table.insert(tmpOpStack,char);
		-- 		else
		-- 			if char == ")" then
		-- 				for i=#tmpOpStack,1,-1 do
		-- 					if tmpOpStack[i] == "(" then
		-- 						table.remove(tmpOpStack,i);
		-- 						break;
		-- 					else
		-- 						local opChar = table.remove(tmpOpStack,i);
		-- 						table.insert(houZhuiList,opChar);
		-- 					end
		-- 				end
		-- 			else
		-- 				for i=#tmpOpStack,1,-1 do
		-- 					if tmpOpStack[i] ~= "(" and opWeight[tmpOpStack[i]] >= opWeight[char] then
		-- 						local opChar = table.remove(tmpOpStack,i);
		-- 						table.insert(houZhuiList,opChar);
		-- 					else
		-- 						break;
		-- 					end
		-- 				end
		-- 				table.insert(tmpOpStack,char);
		-- 			end
		-- 		end
		-- 		tempStr = "";
		-- 	end
		-- end
		-- if tempStr ~= "" then
		-- 	table.insert(houZhuiList,tonumber(tempStr));
		-- end
		-- for i=#tmpOpStack,1,-1 do
		-- 	if tmpOpStack[#tmpOpStack] ~= "(" then
		-- 		local opChar = table.remove(tmpOpStack,i);
		-- 		table.insert(houZhuiList,opChar);
		-- 	end
		-- end
		-- dumpMatrix(houZhuiList)
		-- --[[
		-- 	后缀表达式求值：
		-- 	1、设置一个栈，开始时，栈为空；
		-- 	2、然后从左到右扫描后缀表达式，若遇操作数，则进栈；
		-- 	3、若遇运算符，则从栈中退出两个元素，先退出的放到运算符的右边，后退出的放到运算符左边，运算后的结果再进栈，直到后缀表达式扫描完毕；
		-- 	4、最后，栈中仅有一个元素，即为运算的结果。
		-- ]]
		-- local numStack = {};
		-- for k,v in ipairs(houZhuiList) do
		-- 	if type(v) == "number" then
		-- 		table.insert(numStack,v);
		-- 	else
		-- 		local rightNum = table.remove(numStack);
		-- 		local leftNum = table.remove(numStack);
		-- 		local newNum = opFuncMap[v](leftNum,rightNum);
		-- 		-- print(tostring(k)..":"..tostring(leftNum))
		-- 		-- print(tostring(k)..":"..tostring(rightNum))
		-- 		-- print(tostring(k)..":"..tostring(newNum))
		-- 		table.insert(numStack,newNum);

		-- 	end
		-- end
		-- return numStack[1];

		---网上搜的的思路【结束】---


	-- end

end

-- 运行结果
-- print( fun2( " 1 + 2 ")); -- 3
print( fun2( "(3*2+3)/3+(9/3*2)*(1+3-9)")); -- -27
-- print( fun2( " 1+2 *3")); -- 7



----------------------------------------------------------------
-- 送命题
-- 将1.2.3...16，填入4*4的方格中，
-- 使横竖各行以及对角线上的数字的和等于34。
-- 列出所有可能的组合(一共7040种)
function fun3()
	--打印的上限
	local count = 0;
	local countLimit = 100;
	--程序开始
	local minNum = 1;
	local maxNum = 16;
	local mtNum = 4;
	local numSum = 34;
	--获取节点的总和
	local function getNodesSum(nodes)
		local sum = 0;
		for _,v in ipairs(nodes) do
			sum = sum + v;
		end
		return sum;
	end
	--根据nodes递归设置list链表
	local function setListByNodes(startId,list,nodes)
		if nodes[startId] then
			if startId == #nodes then
				list[nodes[startId]] = 1;
			elseif not list[nodes[startId]] then
				list[nodes[startId]] = {};
			end
			setListByNodes(startId+1,list[nodes[startId]],nodes)
		end
	end
	--递归遍历，获取4个数总和为34的所有组合
	local function _nodes_pairs(nodes,marks,list)
		for i = minNum,maxNum do
			if marks[i] == true then
				--插入节点
				table.insert(nodes,i);
				marks[i] = false;
				--将遍历结果保存起来
				local nodesSum = getNodesSum(nodes);
				if #nodes == mtNum and nodesSum == numSum then
					setListByNodes(1,list,nodes);
					-- --测试nodes
					-- count = count + 1;
					-- local test = "";
					-- for _,vv in ipairs(nodes) do
					-- 	test = test..tostring(vv)..",";
					-- end
					-- print(tostring(count)..":"..test);
				end

				--判断是否继续递归遍历
				if #nodes < mtNum and nodesSum < numSum then
					_nodes_pairs(nodes,marks,list);
				end
				--移除节点
				marks[i] = true;
				table.remove(nodes);
			end
		end
	end
	--获取所有列表的封装函数
	local function getListEquNumSumByMtNum()
		local marks = {};
		for i = minNum,maxNum do
			marks[i] = true;
		end
		local list = {};
		_nodes_pairs({},marks,list);
		return list;
	end

	--根据传入的参数获取坐标列表
	local function getCoListByMtNum()
		--初始化coList
		local coList = {};
		for n = 1,2*mtNum+2 do
			coList[n] = {}
		end
		--给coList进行赋值
		for i = 1,mtNum do
			for j = 1,mtNum do
				--横向坐标列表
				table.insert(coList[2*i-1],{i,j});
				--纵向坐标列表
				table.insert(coList[2*j],{i,j});
				--对角线上坐标列表
				if i == j then
					table.insert(coList[2*mtNum + 1],{i,j});
				elseif (i + j) == (mtNum + 1) then
					table.insert(coList[2*mtNum + 2],{i,j});
				end
			end
		end
		return coList;
	end

	--设置操作后的记录
	local function setMarksRecordFalse(marksRecord,k)
		if marksRecord.marks[k] == true then
			marksRecord.marks[k] = false;
			marksRecord.remainNum = marksRecord.remainNum - 1;
			return true;
		end
		return false;
	end
	--重置操作后的记录
	local function resetMarksRecordFalse(marksRecord,k)
		if marksRecord.marks[k] == false then
			marksRecord.marks[k] = true;
			marksRecord.remainNum = marksRecord.remainNum + 1;
		end
	end
	--根据链表获取所有矩阵
	local function pairsMatrixsByList(matrixs,linkList,coList,marksRecord,matrix,startIdx)
		for stIdx = startIdx,#coList do
			local coordinates = coList[stIdx];
			--注意不能用深复制，以下方式赋值引用跟JS类似
			local listSub = {};
			listSub = linkList;
			--遍历坐标数组
			for idx = 1,#coordinates do
				local row,col = coordinates[idx][1],coordinates[idx][2];
				--print(tostring(row)..";"..tostring(col))
				if matrix[row][col] == -1 then
					for k,_ in pairs(listSub) do
						if setMarksRecordFalse(marksRecord,k) then
							--设置矩阵数据
							matrix[row][col] = k;
							--递归遍历
							local ret = pairsMatrixsByList(matrixs,linkList,coList,marksRecord,matrix,stIdx);
							--重置操作后的数据
							matrix[row][col] = -1;
							resetMarksRecordFalse(marksRecord,k);
						end
					end
					return;
				else
					--重新赋listSub值
					listSub = listSub[matrix[row][col]]
					if not listSub then
						return;
					elseif listSub == 1 then
						--如果所有矩阵数据都填充完，则把数据保存至matrixs
						if stIdx == #coList and idx == #coordinates and marksRecord.remainNum == 0 then
							table.insert(matrixs,copyTab(matrix));

							-- --测试用
							-- count = count + 1;
							-- if count == countLimit then
							-- 	dumpMatrix(matrixs);
							-- 	error("");
							-- end
						end
					end
				end
			end 
		end
	end

	--开始矩阵遍历
	local linkList = getListEquNumSumByMtNum();
	local coList = getCoListByMtNum();
	--初始化marksRecord
	local marksRecord = {
		marks = {};
		remainNum = 0;
	};
	for i = minNum,maxNum do
		marksRecord.marks[i] = true;
		marksRecord.remainNum = marksRecord.remainNum + 1;
	end

	--初始化matrix
	local matrix = {};
	for i = 1,mtNum do
		matrix[i] = {};
		for j = 1,mtNum do
			matrix[i][j] = -1;
		end
	end

	--所有矩阵
	local matrixs = {};
	--递归遍历
	pairsMatrixsByList(matrixs,linkList,coList,marksRecord,matrix,1)
	print(#matrixs)
	-- dumpMatrix(matrixs)
end;

-- 运行结果
-- fun3();
--[[
Case 1
16  3  2 13
 5 10 11  8
 9  6  7 12
 4 15 14  1

Case 2
 1  8  9 16
 7 13  4 10
14  2 15  3
12 11  6  5

...
...

Case 7040
 1 15 14  4
12  6  7  9
 8 10 11  5
13  3  2 16
]]