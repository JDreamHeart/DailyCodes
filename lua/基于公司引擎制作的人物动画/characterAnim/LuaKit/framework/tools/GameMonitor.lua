---
--lua内存泄漏检测工具
--@module GameMonitor
--@author myc

--监控间隔配置（单位：秒） 
local print = print_string; 
local MonitorConfig =   
{  
    --内存泄露监控间隔  
    memLeaksInterval    = 1,  
}  
  
local GameMonitor = {};  
 
function GameMonitor:ctor()  
   --内存泄露弱引用表  
    self.__memLeakTbl   = {}
    setmetatable(self.__memLeakTbl, {__mode='kv'})
    --内存泄露监控器  
    self.__memLeakMonitor   = nil  
end  
 
---开始检测
--@usage g_GameMonitor:start();  
function GameMonitor:start()  
    self.__memLeakMonitor = self:__memLeaksMonitoring()  
end  
  
function GameMonitor:update(dt)  
    if self.__memLeakMonitor then
        self.__memLeakMonitor(dt)  
    end
end  
  
  
---------------------------------------------  
--公有方法  
--功能：       增加一个受监视的表  
--参数tblName:    该表的名字（字符串类型），名字的用途是方便人来记忆，字符串值总比OX002D0EFF之类的好记  
--参数tbl:        该表的引用  
--返回：       无  
--增加一个受监视的表 
--@usage g_GameMonitor:addTblToUnderMemLeakMonitor("test",tex);
function GameMonitor:addTblToUnderMemLeakMonitor(tblName, tbl)  
    if not self.__memLeakMonitor then
        return;
    end
    assert('string' == type(tblName), "Invalid parameters")  
    --必须以名字+地址的方式作为键值  
    --内存泄露经常是一句代码多次分配出内存而忘了回收，因此tblName经常是相同的
    local name = string.format("%s@%s", tblName, tostring(tbl))  
    if nil == self.__memLeakTbl[name] then  
        self.__memLeakTbl[name] = tbl
    end  
end


  
--内存泄露监控逻辑  
function GameMonitor:__memLeaksMonitoring()  
    local monitorTime   = MonitorConfig.memLeaksInterval  
    local interval      = MonitorConfig.memLeaksInterval  
    local str           = nil  
    return function(dt)  
        interval = interval + dt  
        if interval >= monitorTime then  
            interval = interval - monitorTime  
            --强制性调用gc  
            collectgarbage("collect")  
            collectgarbage("collect")
            local flag = false;  
            --打印当前内存泄露监控表中依然存在（没有被释放）的对象信息  
            str = "存在以下内存泄漏:"  
            for k, v in pairs(self.__memLeakTbl) do  
                str = str..string.format("  \n%s = %s", tostring(k), tostring(v))  
            	flag = true;
            end  
            str = str.."\n请仔细检查代码！！！"  
            if flag then
            	print(str);
            end
       end  
    end  
end


function GameMonitor:findObject(obj, findDest,kk)  
    if findDest == nil then  
        return false  
    end 

    if self.findedObjMap[findDest] ~= nil then  
        return false  
    else
        local ret = xpcall(function( ... )
            self.findedObjMap[findDest] = true  
        end, err)
        if not ret  then
            return false;
        end
    end
    
    
  
    local destType = type(findDest)
    if destType == "userdata" then
        local mete = getmetatable(findDest)
        if mete == nil then
        else
            xpcall(function( ... )
                local uservalue = findDest.uservalue
                findDest = uservalue
                destType = type(findDest)
            end, err)
        end
    end
    if destType == "table" then
        for key, value in pairs(findDest) do

            if key == obj or value == obj then 
                if findDest == _G then
                    print("全局引用referenced by _G key:["..tostring(key).."]") 
                else
                    if obj and  obj.class and 
                        type(obj.class) == "table" and obj.class.___name then
                        print("Finded Object " .. tostring(obj.class.___name))
                        print(tostring(obj.class.___name) .. " referenced by :["..tostring(key).."]")
                    else
                        print("Finded Object " .. tostring(obj))
                        print(tostring(value) .. " referenced by :["..tostring(key).."]")
                    end
                end    
                return true, key 
            end


            local ret, k = self:findObject(obj, key);
            if ret == true then  
                print("table key "  .. tostring(key))  
                return true, key
            end


            ---不查自身的若弱引用
            if value ~= self then
                local ret, k = self:findObject(obj, value, key);
                if ret == true then
                    k = k or ""; 
                    if value and type(value) == "table" and value.class and 
                        type(value.class) == "table" and value.class.___name then
                        print(tostring(k) .. " referenced by :["..tostring(value.class.___name).."]")
                    else
                        print(tostring(k) .. " referenced by :["..tostring(key).."]")
                    end
                    
                    ---如果在递归回到全局表 继续遍历 因为存在多层引用 比如被A 引用 同时又被B引用
                    if findDest ~= _G then
                        return true, key 
                    end
                end 
            end
        end  
    elseif destType == "function" then  
        local uvIndex = 1  
        while true do  
            local name, value = debug.getupvalue(findDest, uvIndex)  
            if name == nil then  
                break  
            end  
            if self:findObject(obj, value) == true then  
                print("upvalue name:["..tostring(name).."]")  
                return true  
            end  
            uvIndex = uvIndex + 1  
        end  
    end  
    return false  
end

function GameMonitor:showReferences()
    if  self.__memLeakTbl == nil then
        return;
    end

    if Clock and Clock.instance() then
        Clock.instance():schedule_once(function( ... )
            collectgarbage("collect")  
            collectgarbage("collect")
            for k,v in pairs(self.__memLeakTbl) do
                if v then
                    self:findObjectInGlobal(v,k)
                end
            end
        end)
    else
        collectgarbage("collect")  
        collectgarbage("collect")
        for k,v in pairs(self.__memLeakTbl) do
            if v then
                self:findObjectInGlobal(v,k)
            end
        end
    end
end   
  
function GameMonitor:findObjectInGlobal(obj,name)

    sys_set_int("win32_console_color", 71)
    print("");
    print(string.format("#-----------------------%s-------------------------#",name or ""))
    self.findedObjMap = self:createTable()  
    self:findObject(obj, _G)
    print(string.format("#-----------------------%s-------------------------#",name or ""))
    print("");
    sys_set_int("win32_console_color", 10)
end

function GameMonitor:createTable()
    local proxy = {}
    local mt = {__mode = "k"}
    setmetatable(proxy,mt)
    return proxy
end


return GameMonitor;