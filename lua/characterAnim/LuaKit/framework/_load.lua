---
--framework 初始化工作
--@module _load
--@author myc

--
-- Author: Your NameDate: 2016-05-25 15:03:42
-- 
--
--http://www.network-science.de/ascii/

local version = "4.0";
local strLogo = [[


 __       __    __       ___       __  ___  __  .___________.
|  |     |  |  |  |     /   \     |  |/  / |  | |           |
|  |     |  |  |  |    /  ^  \    |  '  /  |  | `---|  |----`
|  |     |  |  |  |   /  /_\  \   |    <   |  |     |  |     
|  `----.|  `--'  |  /  _____  \  |  .  \  |  |     |  |     
|_______| \______/  /__/     \__\ |__|\__\ |__|     |__|     


]]


-- print(strLogo)
local freeGlobal = true;

local function merge(dest, src)
    for k, v in pairs(src) do
        dest[k] = v
    end
end
local function nums(t)
    local temp = t or {};
    local count = 0
    for k, v in pairs(temp) do
        count = count + 1
    end
    return count
end


local record = {}

local __g = _G


local framework = {};

local globals = {};




---lua系统自带库 以下扩展会在扩展之前检查是否有被扩展过 如果有则报错
local luaGlobalModule = {
    table   = 1;
    math    = 1;
    io      = 1;
};


function framework:load(root)

    -- print("global " .. nums(globals))
    local StringLib = require(root .. "framework.lib.StringLib");

    local Base64 = require(root .. "framework.lib.Base64")
    local M = {};
    M.Base64 = Base64;
    framework:mergeToGlobal(M)

    require(root .. "framework.core.object");


    
    local TableLib = require(root .. "framework.lib.TableLib");
    local M = {};
    M.table = TableLib;
    framework:mergeToGlobal(M)

    require(root .. "framework.lib.MathLib");



    ---合并functions 中的扩展
    local funcs = require(root .. "framework.functions");
    framework:mergeToGlobal(funcs)


    ---加载dump 模块
    local dump = require(root .. "framework.tools.dump");
    local M = {};
    M.dump = dump;
    -- BYKit.dump = dump;
    framework:mergeToGlobal(M)


    ---加载内存检测工具
    -- local GameMonitor = require(root .. "framework.tools.GameMonitor");
    -- -- local M = {};
    -- if g_GameMonitor == nil then
    --     BYKit.GameMonitor = new(GameMonitor);
    --     BYKit.GameMonitor:start()

    -- end

    ---加载数据变化跟踪
    -- local DataTracker = require(root .. "framework.tools.DataTracker");
    -- local M = {};
    -- M.DataTracker = DataTracker;
    -- framework:mergeToGlobal(M);

    -- require(root .. "framework.tools.profiler");

    -- framework:mergeToGlobal(M)

    ---添加dumpToFile 接口
    local dumpToFile = require(root .. "framework.tools.dumpToFile");
    local M = {}
    M.dumpToFile = dumpToFile.dumpToFile;
    framework:mergeToGlobal(M)


   
    ---加载组件基类
    local BehaviorBase = require(root .. "framework.behaviors.BehaviorBase");
    local M = {};
    M.BehaviorBase = BehaviorBase;
    framework:mergeToGlobal(M)


    local BehaviorExtend = require(root .. "framework.behaviors.BehaviorExtend");
    local M = {};
    M.BehaviorExtend = BehaviorExtend;
    framework:mergeToGlobal(M)


    local BehaviorFactory = require(root .. "framework.behaviors.BehaviorFactory");
    local M = {};
    M.BehaviorFactory = BehaviorFactory;
    framework:mergeToGlobal(M)





    print("add new global " .. nums(globals))

end

function framework:release()
    print("framework全局变量" .. nums(globals))
    -- if freeGlobal == true then
        for k,v in pairs(globals) do
            if luaGlobalModule[k] == 1 then
                local key = k
                local obj = __g[key];
                local M =  v;
                print("free Module " .. key)
                for k,v in pairs(M) do
                    if obj[k] then
                        print("free " .. k)
                        obj[k] = nil;
                    end
                end
                globals[key] = nil;
            else
                print("释放全局的 " .. k)
                __g[k] = nil;
                globals[k] = nil;
            end
        end

        if nums(globals) > 0 then
            for k,v in pairs(globals) do
                print("还存在 Module " .. k)
            end
            error("没释放干净")
        else
            print("framework全局变量已经释放")
        end
        -- globals = {};
    -- end

    for i,data in ipairs(record) do
        if data.objKey then
            local obj = __g[data.objKey];
            obj[data.key] = data.value;
        else
            local obj = __g[data.key];
            __g[data.key] = data.value;
        end
    end
    record = {};

end



---合并到全局表
function framework:mergeToGlobal(module)
    for k,v in pairs(module) do
        ---扩展系统自带库 如table math io 库
        if luaGlobalModule[k] == 1 then
            local M =  v;
            local key = k;
            local obj = __g[key];
            for k,v in pairs(M) do
                if obj[k] then
                    local data = {objKey = key,key = k,value = obj[k]}
                    table.insert(record,data);
                    print_string( k .." 已经存在" .. key .. " 表中")
                    obj[k] = v;
                    -- if freeGlobal == true then
                    --     error(k .." 已经存在" .. key .. " 表中")
                    -- else
                    --     obj[k] = v;
                    -- end
                else
                    obj[k] = v;
                end
            end
            globals[k] = M;
        else
            ---添加到全局表
            if __g[k] then
                print_string( k .." 已经存在全局表中")
                local data = {key = k,value = __g[k]}
                table.insert(record,data);
                __g[k] = v;
                globals[k] = v; 

                -- if freeGlobal == true then
                --     error(k .." 已经存在全局表中")
                -- else
                --     __g[k] = v;
                --     globals[k] = v; 
                -- end     
            else
                __g[k] = v;
                globals[k] = v;
            end
        end
    end
end

return framework;