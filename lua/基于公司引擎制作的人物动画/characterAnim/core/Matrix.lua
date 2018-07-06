--[[--ldoc desc
@module Matrix
@author JinZhang

Date   2018-07-06 15:46:54
Last Modified by   JinZhang
Last Modified time 2018-07-06 16:07:34
]]

local mt = {};
--[[--
   对应表达式 a == b
]]
 mt.__eq = function (c1, c2) 
    return c1.byte == c2.byte
 end


--[[--
   对应表达式 a < b
]]
mt.__lt = function (c1, c2) 
    if c1.value == c2.value then
        local t1 = c1.type;
        local t2 = c2.type;
        return t1 < t2; 
    end
    return c1.value < c2.value; 
end

--[[--
  对应表达式 a <= b
]]
mt.__le = function (c1, c2) 
    if c1.value == c2.value then
        local t1 = c1.type;
        local t2 = c2.type;
        return t2 > t1; 
    end
    return c2.value > c1.value; 
end

--[[--
对应表达式 a - b
]]
mt.__sub = function (c1, c2) 
    return c1.value - c2.value; 
end

--[[--
对应表达式 a + b
]]
mt.__add = function (c1, c2) 
    return c1.value + c2.value; 
end

--[[--
tostirng(e)
功能：将参数e转换为字符串，此函数将会触发元表的__tostring事件
]]
mt.__tostring = function (t)
    if t.type < 3 then
        return  t.value ..  _typeMap[t.type];
    else
        if huaMap[t.byte] then
           return huaMap[t.byte];
        else
            return (string.format("0x%02x",t.byte))
        end  
    end
end