---
--跟踪数据变化，比如moeny在某个地方被修改了 可以用工具检测出来
--@module DataTracker
--@author myc

local DataTracker = {};

local function init(obj, keys)
    local mKeys, keys_str = {}, {}
    for k,v in pairs(keys) do 
        local kType = type(k);
        if kType == "number" then
            mKeys[v] = 1;
            table.insert(keys_str, v);
        elseif kType == "string" then
            mKeys[k] = v;
            table.insert(keys_str, k);
        end
    end
    
    if Log and Log.i then
    	Log.i("开始监控：" .. table.concat(keys_str, ", "));
    else
    	print("开始监控：" .. table.concat(keys_str, ", "));
    end

    local oldMeta = getmetatable(obj)
    if oldMeta == nil then
        oldMeta = {};
    end

    if oldMeta.__index == nil then
        oldMeta.__index = {};
    end

    setmetatable(obj, oldMeta);
    return oldMeta, mKeys;
end

--[[--
    监控数值创建或修改
    @param obj 需要监控的目标
    @param keys 需要监控的字段
                值为1表示非中断监控，输出修改次数与对应位置栈信息；
                值为2表示中断监控，修改马上抛出error中断运行；
                没有值默认为1；

    例如：（mid，money非中断，nick中断）
    local data = { moeny =1000, mid =100, nick = "111" }
    keys = {money = 1, nick = 2, "mid"}

    DataTracker.trackingDataModify(data, keys)
    data.money = 1; ---如果尝试修改 则根据监控模式做出相应处理 抛错误或者打印堆栈
]]
function DataTracker.trackingDataModify(obj, keys)
    local mt, keys = init(obj, keys);

    local counter = {};
    local object = mt.__index;
    for k,v in pairs(keys) do
        object[k] = obj[k];
        obj[k] = nil;
        counter[k] = 0;
    end

    mt.__newindex = function(t, k, v)
        if keys[k] ~= nil then
            if keys[k] == 1 then
                counter[k] = counter[k] + 1;
                local p_str = string.format("第%d次修改%s，上次值：%s，当前值：%s", counter[k], k, tostring(object[k]), tostring(v));
                if dump then
                    dump(debug.traceback(p_str));
                else
                    print(debug.traceback(p_str));
                end
                object[k] = v;
            elseif keys[k] == 2 then
                error("你没权限创建或修改 -> " .. k);
            else
                error("监控配置参数有问题，键值模式参数必须为1，2或不填（默认为1）");
            end
        else
            object[k] = v;
        end
    end
end

return DataTracker;