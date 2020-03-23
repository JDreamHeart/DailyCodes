--[[--ldoc desc
@module Matrix
@author JinZhang

Date   2018-07-06 15:46:54
Last Modified by   JinZhang
Last Modified time 2018-07-06 16:07:34
]]
local utils = import(".utils");

local mt = {};

--[[--
   对应表达式 a == b
]]
 mt.__eq = function(m1, m2) 
    if m1.m_ == m2.m_ and m1.n_ == m2.n_ then
        for i = 1, #m1.data_ do
            if m1.data_[i] ~= m2.data_[i] then
                return false;
            end
        end
    end
end

--[[--
    对应表达式 a + b
]]
mt.__add = function(m1, m2)
    if m1.m_ == m2.m_ and m1.n_ == m2.n_ then
        local data = {};
        for i = 1, #m1.data_ do
            data[i] = m1.data_[i] + m2.data_[i];
        end
        return m1.new(data, m1.m_, m1.n_);
    end
end

--[[--
    对应表达式 a - b
]]
mt.__sub = function(m1, m2)
    if m1.m_ == m2.m_ and m1.n_ == m2.n_ then
        local data = {};
        for i = 1, #m1.data_ do
            data[i] = m1.data_[i] - m2.data_[i];
        end
        return m1.new(data, m1.m_, m1.n_);
    end
end

--[[--
    对应表达式 a * b
]]
mt.__mul = function(m1, m2)
    local mType1 = type(m1);
    local mType2 = type(m2);
    if mType1 == mType2 then
        if m1.n_ == m2.m_ then
            local data = {};
            for i = 1, m1.m_ do
                for j = 1, m2.n_ do
                    local val = 0;
                    for k = 1, m1.n_ do
                        val = val + m1.data_[(i - 1) * m1.n_ + k] * m2.data_[(k - 1) * m2.n_ + j];
                    end
                    data[(i - 1) * m2.n_ + j] = val;
                end
            end
            return m1.new(data, m1.m_, m2.n_);
        end
    else
        local numberM;
        local matrixM;
        if mType1 == "number" then
            numberM = m1;
            matrixM = m2;
        elseif mType2 == "number" then
            matrixM = m1;
            numberM = m2;
        else
            return;
        end
        local data = {};
        for i = 1, #matrixM.data_ do
            data[i] = numberM * matrixM.data_[i];
        end
        return matrixM.new(data, matrixM.m_, matrixM.n_);
    end
end

--[[--
    对应表达式 a / b , 其中bixuwei不等于0的数字
]]
mt.__div = function(m1, m2)
    if type(m2) == "number" and m2 ~= 0 then
        local data = {};
        for i = 1, #m1.data_ do
            data[i] = m1.data_[i] / m2;
        end
        return m1.new(data, m1.m_, m1.n_);
    end
end

--[[--
    tostirng(m)
    功能：将参数m转换为字符串，此函数将会触发元表的__tostring事件
]]
mt.__tostring = function(m)
    local stringTb = {};
    for i = 1, m.m_ do
        local rowData = {};
        for j = 1, m.n_ do
            table.insert(rowData, m.data_[(i - 1) * m.n_ + j]);
        end
        table.insert(stringTb, string.format("row[%d]: {%s}", i, table.concat(rowData, ", ")));
    end
    return table.concat(stringTb, "\n");
end

--[[--
    matrix(row, col)
    功能：获取matrix中，对应row, col位置的值
]]
mt.__call = function(m, row, col)
    return m:get(row, col);
end


--- 校验构建矩阵的参数
local function _checkMatrixTable(data, m, n)
    -- 校验是否有空值
    local count = #data;
    if not m then
        m = (count > 0) and 1 or 0;
        n = count;
    elseif not n then
        n = math.ceil(count / m);
    end
    -- 校验数据是否合法
    if count ~= m * n then
        error("It has error to create matrix !");
    end
    if data[1] then
        local elemType = type(data[1]);
        if elemType ~= "number" then
            return {}, 0, 0;
        end
        for i = 1, #data do
            if type(data[i]) ~= elemType then
                return {}, 0, 0;
            end
        end
    end
    return data, m, n;
end

--- 获取求矩阵行列式的相关参数
local function _getDetRelevantParam(m, n)
    if m == n then
        local params = {
            inverseOrdinalNumbers = {}, -- 逆序数
        };
        params.exCheckFunc = function(tb, curParams, groups, group)
            local curIdx = #groups;
            local iONs = params.inverseOrdinalNumbers;
            iONs[curIdx] = iONs[curIdx] or 0;
            for i = #group, 1, -1 do
                for j = (i-1), 1, -1 do
                    if group[j] and group[j] > group[i] then
                        iONs[curIdx] = iONs[curIdx] + 1;
                    end
                end
            end
        end
        local tb = utils.getArrayByNum(n);
        local groups = utils.getFullArrangement(tb, params);
        return groups, params.inverseOrdinalNumbers;
    end
end

--- 调整逆序数
local function _adjustInverseOrdinalNumber(iON, group, k)
    for i = #group, k, -1 do
        if group[i] < group[k] then
            iON = iON - 1;
        end
    end
    for i = k, 1, -1 do
        if group[i] > group[k] then
            iON = iON - 1;
        end
    end
    return iON;
end

--[[-- 
    获取矩阵行列式的值
    这里考虑了求逆矩阵的时的余子式计算，所以加了excludeRow, excludeCol这两个参数，用来过滤掉余子式中被排除的行列。
    其中有个调整逆序数的次数判断，限制至多为一次的原因是：
    1. 当没有过滤某一行列时，调整次数为零【一般的求行列式】；
    2. 当过滤某一行列时，由于考虑性能问题，所以还是使用了原来的groups，所以会出现一个group中，同时出现对应行列都过滤的情况，这时的group不能被作为余子式的计算当中的。
]]
local function _getDetVal(data, m, n, groups, iONs, excludeRow, excludeCol)
    local det = 0;
    local iON = iONs[i];
    local val = 1;
    local isChangeVal = false;
    local adjustCount = 0;
    for i,group in ipairs(groups) do
        iON = iONs[i];
        val = 1;
        isChangeVal = false;
        adjustCount = 0;
        for k,v in ipairs(group) do
            if k == excludeRow or v == excludeCol then
                -- 在求逆矩阵的时候，需要求余子式，所以要调整逆序数
                iON = _adjustInverseOrdinalNumber(iON, group, k);
                adjustCount = adjustCount + 1;
            else
                val = val * data[(k - 1) * n + v];
                isChangeVal = true;
            end
        end
        -- 必须改变了val，且在求逆矩阵的时候，需要的余子式计算中，最多只能调整一次逆序数
        if isChangeVal and adjustCount <= 1 then
            det = det + math.pow(-1, iON) * val;
        end
    end
    return det;
end

-- 矩阵类
local Matrix = class();

function Matrix:ctor(data, row, col)  
    -- 校验并初始化数据
    self.data_, self.m_, self.n_ = _checkMatrixTable(data, row, col);
end

function Matrix:dtor()
    
end

-- new 新矩阵
function Matrix.new(data, row, col)
    local matrix = new(Matrix, data, row, col);
    local meta = getmetatable(matrix);
    if meta then
        table.merge(meta, mt);
    else
        setmetatable(matrix, mt);
    end
    return matrix;
end

--[[
    获取矩阵对应行列的数据
]]
function Matrix:get(row, col)
    if row and col then
        return self.data_[(row - 1) * self.n_ + col];
    elseif row and (not col) then
        if row <= self.m_ then
            local data = {};
            for i = 1, self.n_ do
                table.insert(data, self.data_[(row - 1) * self.n_ + i]);
            end
            return data;
        end
    elseif (not row) and col then
        if col <= self.n_ then
            local data = {};
            for i = 1, self.m_ do
                table.insert(data, self.data_[(i - 1) * self.n_ + col]);
            end
            return data;
        end
    end
end

--[[
    获取矩阵的行列数
]]
function Matrix:getSize()
    return self.m_, self.n_;
end

--[[
    获取矩阵的行数
]]
function Matrix:getRow()
    return self.m_;
end

--[[
    获取矩阵的列数
]]
function Matrix:getCol()
    return self.n_;
end

--[[
    矩阵的转置矩阵
]]
function Matrix:T()
    local data = {};
    for i = 1, self.n_ do
        for j = 1, self.m_ do
            table.insert(data, self.data_[(j - 1) * self.n_ + i]);
        end
    end
    return self.new(data, self.n_, self.m_);
end

--[[
    矩阵的行列式
]]
function Matrix:D()
    local groups, iONs = _getDetRelevantParam(self.m_, self.n_);
    if groups and iONs then
        return _getDetVal(self.data_, self.m_, self.n_, groups, iONs);
    end;
end

--[[
    矩阵的逆矩阵
]]
function Matrix:I()
    local groups, iONs = _getDetRelevantParam(self.m_, self.n_);
    if groups and iONs then
        local detVal = _getDetVal(self.data_, self.m_, self.n_, groups, iONs);
        if detVal ~= 0 then
            local AData = {};
            for i = 1, self.m_ do
                for j = 1, self.n_ do
                    local MDetVal = _getDetVal(self.data_, self.m_, self.n_, groups, iONs, i, j);
                    MDetVal = math.pow(-1, i+j) * MDetVal / detVal;
                    AData[(j - 1) * self.m_ + i] = MDetVal;
                end
            end
            return self.new(AData, self.m_, self.n_);
        end
    end;
end

return Matrix;