--[[--题目要求:
1.解决错误，能正确输出日志 “执行成功继续执行”，“执行正确”
2.不能修改别的地方，只能在InitSoInfo函数内调整
3.SendGameData 必须在 self.mainCo协程内调用
4.以注释写出问题原因，已经如何解决的过程
@module Lua协程进阶
@author YuchengMo

Date   2017-11-16 15:14:43
Last Modified by   JinZhang
Last Modified time 2017-11-21 10:27:16
]]


local iGame = {};
local iTableWrap = {};
local log_level = 1;

---创建桌子
function createTable(iTableWrap, iGame, log_level)

    local pTable = {name = "1"};
    local register = function(iGame)
        function iGame:InitSoInfo(gameInfo)
            self.mainCo =  coroutine.create(function(...)
                g_Table.iGame_.iTableWrap_lua:SendGameData({data = "yms"})
                print("执行正确")
            end
            )
            local code, data = coroutine.resume(self.mainCo, {});
            --[[--
                一、问题原因：
                    1.协程的挂起，只在g_Table.iGame_.iTableWrap_lua:SendGameData中出现了一次，
                    而在iGame:InitSoInfo的后面，运行了两次handler();
                    其中第一次运行，由于此函数没返回值，导致报错。
                二、解决的过程：
                    1.先了解整个文件的函数调用关系，然后看最后的调用函数方式，其中共调用三次handler()函数；
                    第一次调用createTable函数，将iGame.iTableWrap_lua, iGame.rpc_iGame, log_level参数传进createTable，初始化此InitSoInfo函数；
                    第二次则是调用此InitSoInfo(gameInfo)函数，结果没返回值，而后面使用了该返回值，结果程序报错了；
                      于是在下面调用了coroutine.yield(data)，将data作为第二次调用handler()的结果返回，并挂起协程；
                    第三次调用的同样是InitSoInfo(gameInfo)函数，从挂起处继续执行，恢复self.mainCo函数，则进行以上字符串的打印；
                      此次由于后面没调用返回的数据，因而不会报错。

            ]]
            coroutine.yield(data);
        	coroutine.resume(self.mainCo, {});
        end
    end

    register(iGame);

    return pTable;
end

function rpc_createTable(iTableWrap, iGame, log_level)
    print("CoroutineDemo")

    local co = coroutine.create(createTable)

    iGame.rpc_iGame = {};


    iGame.InitSoInfo = function(self,param)
        -- print("rpc_createTable InitSoInfo");
        local co = coroutine.create(self.rpc_iGame.InitSoInfo)
        return function(...)
            return coroutine.resume(co, iGame.rpc_iGame, param)
        end
    end

    --lua调用C++的接口
    local iTableWrap_lua = {};

    iGame.iTableWrap_lua = iTableWrap_lua;
    iTableWrap_lua.iTableWrap = iTableWrap;

    iTableWrap_lua.SendGameData = function(self,luaParam)
        print("rpc_SendGameData");
        local lua_event = {};
        lua_event.func_name = "SendGameData";
        lua_event.func_lua_param = luaParam ;
        coroutine.yield(lua_event);

    end

    return function(...)
        return coroutine.resume(co, iGame.iTableWrap_lua, iGame.rpc_iGame, log_level)
    end
end

local handler = rpc_createTable(iTableWrap,iGame,log_level)
local ret,data = handler()
g_Table = data
g_Table.iGame_ = iGame;
local handler = iGame:InitSoInfo({tableID = 1001})
ret,data = handler()
if data.func_name == "SendGameData" then
    print("执行成功继续执行")
end
ret,data = handler()