---根据系统时间初始化随机数种子，让后续的 math.random() 返回更随机的值
function math.newrandomseed()
	local seed = tostring(os.time()):reverse():sub(1, 7)
    math.randomseed(seed)
    math.random()
    math.random()
    math.random()
    math.random()
    return seed;
end


---
---对数值进行四舍五入，如果不是数值则返回 0
-- @param value 输入值
-- @return number
function math.round(value)
    value = checknumber(value)
    return math.floor(value + 0.5)
end

---
-- 角度转弧度
-- @param angle 角度值
-- @return number 弧度值
function math.angle2radian(angle)
    return angle*math.pi/180
end

---
-- 弧度转角度
-- @param angle 弧度
-- @return number 角度
function math.radian2angle(radian)
    return radian/math.pi*180
end