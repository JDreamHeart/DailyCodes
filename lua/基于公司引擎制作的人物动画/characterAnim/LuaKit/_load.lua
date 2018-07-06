--[[--ldoc 框架加载入口
@module _load
@author YuchengMo

Date   2017-12-20 11:47:08
Last Modified by   YuchengMo
Last Modified time 2018-05-28 15:18:51
]]
local startMem = collectgarbage("count")
LuaKit = {}
local __g = _G
-- __g.__uv = 1;
local exports = {lua_error_msg = 1,__uv = 1, DebuggeeTempVar = 1}


LuaKit.globals = {}
LuaKit.exports = exports;

---禁用全局变量
function LuaKit:disableGobal()
    setmetatable(__g, {
        __newindex = function(_, name, value)
            if exports[name] then ---引擎导入的全局变量
               rawset(LuaKit.globals, name, value)
               return;
            end
            local str = debug.traceback();
            dump(str)
            error(str .. "n" .. string.format("USE \" LuaKit.globals.%s = value \" INSTEAD OF SET GLOBAL VARIABLE", name))

            rawset(LuaKit.globals, name, value)

        end,
        __index = function(_,name)
            return rawget(LuaKit.globals, name)
        end
    })
end


function LuaKit:enableGlobal()
    setmetatable(__g, {
            __index = function(_, name)
                return rawget(LuaKit.globals, name)
            end
        })
end

function LuaKit:freeGlobal()
    setmetatable(__g, {})
    LuaKit = {};
    LuaKit.globals = {}

end

function LuaKit:getCurModulePath()
    local _,path = debug.getlocal(2,1);
    return path;
end

local root = "LuaKit."



LuaKit.LuaKitConfig = require("LuaKit.config.LuaKitConfig");

local framework = require("LuaKit.framework._load")
framework:load(root);

-- LuaKit:disableGobal()


local endMem = collectgarbage("count")

print(string.format("加载LuaKit结束，内存变化 开始：%s, 结束: %s，差值: %s",startMem,endMem,endMem - startMem));

