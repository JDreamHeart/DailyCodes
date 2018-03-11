----------------------------------------------------------------
-- 附加题
-- 做一个字符串解析四则运算计算器
function fun2(str)
    local file = io.open("ww.lua", "w+"); -- 新创建一个文件 w+ 表示写入
    file:write("return ")    -- 你懂的
    file:write(str)         -- 既然有LUA虚拟机.为什么要自己解析
    file:close();           --
    return dofile("ww.lua") -- 加载一下就好
end

-- 运行结果
print( fun2( " 1 + 2 ")); -- 3
print( fun2( "(1+2)*3")); -- 9
print( fun2( " 1+2 *3")); -- 7
print( fun2( "(3*2+3)/3+(9/3*2)*(1+3-9)")); -- -27
