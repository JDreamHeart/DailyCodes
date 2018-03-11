-- 最终打印
local nFinalCount = 0;
local function print_final(m)
    local strFormat = "第%d种:\n%2d %2d %2d %2d\n%2d %2d %2d %2d\n%2d %2d %2d %2d\n%2d %2d %2d %2d\n";

    nFinalCount = nFinalCount + 1;
    print(string.format(strFormat,
        nFinalCount,
        m[1],  m[2],  m[3],  m[4],
        m[5],  m[6],  m[7],  m[8],
        m[9],  m[10],  m[11], m[12],
        m[13], m[14], m[15], m[16]
    ))

    nFinalCount = nFinalCount + 1;
    print(string.format(strFormat,
        nFinalCount,
        m[1],  m[5],  m[9],  m[13],
        m[2],  m[6],  m[10],  m[14],
        m[3],  m[7],  m[11], m[15],
        m[4],  m[8],  m[12], m[16]
    ))

    nFinalCount = nFinalCount + 1;
    print(string.format(strFormat,
        nFinalCount,
        m[4],  m[8],  m[12],  m[16],
        m[3],  m[7],  m[11],  m[15],
        m[2],  m[6],  m[10],   m[14],
        m[1],  m[5],  m[9],   m[13]
    ))

    nFinalCount = nFinalCount + 1;
    print(string.format(strFormat,
        nFinalCount,
        m[4],  m[3],  m[2],   m[1],
        m[8],  m[7],  m[6],   m[5],
        m[12], m[11], m[10],  m[9],
        m[16], m[15], m[14],  m[13]
    ))

    nFinalCount = nFinalCount + 1;
    print(string.format(strFormat,
        nFinalCount,
        m[16], m[15], m[14], m[13],
        m[12], m[11], m[10],  m[9],
        m[8],  m[7],  m[6],  m[5],
        m[4],  m[3],  m[2],  m[1]
    ))

    nFinalCount = nFinalCount + 1;
    print(string.format(strFormat,
        nFinalCount,
        m[16], m[12], m[8],  m[4],
        m[15], m[11], m[7],  m[3],
        m[14], m[10],  m[6],  m[2],
        m[13], m[9],  m[5],  m[1]
    ))

    nFinalCount = nFinalCount + 1;
    print(string.format(strFormat,
        nFinalCount,
        m[13], m[9],  m[5],  m[1],
        m[14], m[10],  m[6],  m[2],
        m[15], m[11], m[7],  m[3],
        m[16], m[12], m[8],  m[4]
    ))

    nFinalCount = nFinalCount + 1;
    print(string.format(strFormat,
        nFinalCount,
        m[13], m[14], m[15], m[16],
        m[9],  m[10],  m[11], m[12],
        m[5],  m[6],  m[7],  m[8],
        m[1],  m[2],  m[3],  m[4]
    ))
end

function main()
    -- 判断2表重复, 如果重复返回false 不一样返回true
    local function diff2(t1, t2)
        if t1.a == t2.a or t1.a == t2.b or t1.a == t2.c or t1.a == t2.d then
            return false
        end;
        if t1.b == t2.a or t1.b == t2.b or t1.b == t2.c or t1.b == t2.d then
            return false
        end;
        if t1.c == t2.a or t1.c == t2.b or t1.c == t2.c or t1.c == t2.d then
            return false
        end;
        if t1.d == t2.a or t1.d == t2.b or t1.d == t2.c or t1.d == t2.d then
            return false
        end;
        return true;
    end;

    -- 判断4数重复
    local function diff4(a,b,c,d)
        if a == b or a == c or a == d or b == c or b == d or c == d then
            return false;
        end;
        return true;
    end;

    -- 判断4数累加等于4
    local function add4(a,b,c,d)
        return a + b + c + d  == 34
    end;

    -- 判断4数是否有效
    local function valid4(a,b,c,d)
        -- 不能重复
        if not diff4(a,b,c,d) then
            return false
        end;

        if a < 1 or a > 16 or b < 1 or b > 16 or c < 1 or c > 16 or d < 1 or d > 16 then
            return false;
        end;
        return true;
    end;


    local PreEquation = {};

    for a = 1, 16 do
        for b = a + 1, 16 do
            for c = b + 1, 16 do
                for d = c + 1, 16 do
                    if add4(a, b, c, d) then
                        table.insert(PreEquation, {a=a,b=b,c=c,d=d});
                    end;
                end;
            end;
        end;
    end;

    for i = 1, #PreEquation do
        local v = PreEquation[i];
        table.insert(PreEquation, {a=v.a,b=v.b,c=v.d,d=v.c})
        table.insert(PreEquation, {a=v.a,b=v.c,c=v.b,d=v.d})
        table.insert(PreEquation, {a=v.a,b=v.c,c=v.d,d=v.b})
        table.insert(PreEquation, {a=v.a,b=v.d,c=v.b,d=v.c})
        table.insert(PreEquation, {a=v.a,b=v.d,c=v.c,d=v.b})

        table.insert(PreEquation, {a=v.b,b=v.a,c=v.c,d=v.d})
        table.insert(PreEquation, {a=v.b,b=v.a,c=v.d,d=v.c})
        table.insert(PreEquation, {a=v.b,b=v.c,c=v.a,d=v.d})
        table.insert(PreEquation, {a=v.b,b=v.d,c=v.a,d=v.c})

        table.insert(PreEquation, {a=v.c,b=v.a,c=v.b,d=v.d})
        table.insert(PreEquation, {a=v.c,b=v.b,c=v.a,d=v.d})
    end;

    for i = 1, #PreEquation do
        local i_data = PreEquation[i];
        for j = i+1, #PreEquation do
            if diff2(PreEquation[i], PreEquation[j]) then
                local m = {};
                local j_data = PreEquation[j];

                m[1]  = i_data.a;
                m[6]  = i_data.b;
                m[11] = i_data.c;
                m[16] = i_data.d;
                m[4]  = j_data.a;
                m[7]  = j_data.b;
                m[10] = j_data.c;
                m[13] = j_data.d;

                for k = 1, 16 do
                    m[5]  = k;
                    m[8]  = 34 - m[5] - m[6] - m[7];
                    m[12] = 34 - m[4] - m[8] - m[16];
                    m[9]  = 34 - m[10] - m[11] - m[12];
                    -- 关键判断
                    if valid4(m[5], m[8], m[9], m[12]) and add4(m[1], m[5], m[9], m[13]) then
                        -- 位置填充完毕, 判断 5 8 9 12 是否和前面两个交叉有重复
                        local k_data = {a = m[5], b = m[8], c = m[9], d = m[12]};
                        if diff2(k_data, i_data) and diff2(k_data, j_data) then
                            for l = 1, 16 do
                                m[2]  = l;
                                m[3]  = 34 - m[1] - m[2] - m[4];
                                m[15] = 34 - m[3] - m[7] - m[11];
                                m[14] = 34 - m[13] - m[15] - m[16];

                                if valid4(m[2], m[3], m[15], m[14]) and add4(m[2], m[6], m[10], m[14]) then
                                    local l_data = {a = m[2], b = m[3], c = m[15], d = m[14]}

                                    if diff2(l_data, i_data) and diff2(l_data, j_data) and diff2(l_data, k_data) then
                                        -- 这里就是我们需要的 需要的代码
                                        if add4
                                        print_final(m);
                                    end;
                                end;
                            end;
                        end;
                    end;
                end;
            end;
        end;
    end;
end;

-- 运行结果
local o = os.time();
main();
print("时间开销" .. (os.time() - o) .. "秒");



