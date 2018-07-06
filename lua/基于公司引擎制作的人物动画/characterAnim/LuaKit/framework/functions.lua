---
--提供一组常用函数，以及对 Lua 标准库的扩展
--@module functions
--@author myc

local tinsert = table.insert;
local tconcat = table.concat;
local M = {};

--[[--
载入一个模块

@usage
import() 与 import() 功能相同，但具有一定程度的自动化特性。
假设我们有如下的目录结构：
app/
app/classes/
app/classes/MyClass.lua
app/classes/MyClassBase.lua
app/classes/data/Data1.lua
app/classes/data/Data2.lua
MyClass 中需要载入 MyClassBase 和 MyClassData。如果用 import()，MyClass 内的代码如下:
local MyClassBase = import("app.classes.MyClassBase")
local MyClass = class("MyClass", MyClassBase)

local Data1 = import("app.classes.data.Data1")
local Data2 = import("app.classes.data.Data2")

--假如我们将 MyClass 及其相关文件换一个目录存放，那么就必须修改 MyClass 中的 import() 命令，否则将找不到模块文件。
--而使用 import()，我们只需要如下写：

local MyClassBase = import(".MyClassBase")
local MyClass = class("MyClass", MyClassBase)

local Data1 = import(".data.Data1")
local Data2 = import(".data.Data2")


当在模块名前面有一个"." 时，import() 会从当前模块所在目录中查找其他模块。因此 MyClass 及其相关文件不管存放到什么目录里，我们都不再需要修改 MyClass 中的 import() 命令。这在开发一些重复使用的功能组件时，会非常方便。

我们可以在模块名前添加多个"." ，这样 import() 会从更上层的目录开始查找模块。


不过 import() 只有在模块级别调用（也就是没有将 import() 写在任何函数中）时，才能够自动得到当前模块名。如果需要在函数中调用 import()，那么就需要指定当前模块名：

MyClass.lua

这里的 ...     是隐藏参数，包含了当前模块的名字，所以最好将这行代码写在模块的第一行

local CURRENT_MODULE_NAME = ...
local function testLoad()
    local MyClassBase = import(".MyClassBase", CURRENT_MODULE_NAME)
end

@param moduleName 要载入的模块的名字
@param currentModuleNameParts 当前模块名
@return module

]]

function M.import(moduleName, currentModuleName)
    local currentModuleNameParts
    local moduleFullName = moduleName
    local offset = 1
    while true do
        if string.byte(moduleName, offset) ~= 46 then -- .
            moduleFullName = string.sub(moduleName, offset)
            if currentModuleNameParts and #currentModuleNameParts > 0 then
                moduleFullName = table.concat(currentModuleNameParts, ".") .. "." .. moduleFullName
            end
            break
        end
        offset = offset + 1
        if not currentModuleNameParts then
            if not currentModuleName then
                local n,v = debug.getlocal(3, 1)
                currentModuleName = v
            end
            currentModuleNameParts = string.split(currentModuleName, ".")
            -- dump(currentModuleNameParts)
        end
        table.remove(currentModuleNameParts, #currentModuleNameParts)
    end
    -- print_string("moduleFullName",moduleFullName)
    local m = require(moduleFullName);
    return m
end


function M.g_reload(moduleName)
    if moduleName then
        package.loaded[moduleName] = nil
        return require(moduleName)
    end
end



---检查并尝试转换为数值，如果无法转换则返回 0
--@string value 要检查的值
--@param base 进制，默认为十进制
--@return number
function M.checknumber(value, base)
    return tonumber(value, base) or 0
end


---检查并尝试转换为数值，如果无法转换则返回 0
--@string value 要检查的值
--@return integer
function M.checkint(value)
    return math.round(checknumber(value))
end

---检查并尝试转换为布尔值，除了 nil 和 false，其他任何值都会返回 true
--@string value 要检查的值
--@return boolean
function M.checkbool(value)
    return (value ~= nil and value ~= false)
end


---检查值是否是一个表格，如果不是则返回一个空表格
--@string value 要检查的值
--@return table
function M.checktable(value)
    if type(value) ~= "table" then value = {} end
    return value
end


---如果表格中指定 key 的值为 nil，或者输入值不是表格，返回 false，否则返回 true
--@param hashtable 要检查的表格
--@param key 要检查的键名
--@return boolean
function M.isset(hashtable, key)
    local t = type(hashtable)
    return (t == "table" or t == "userdata") and hashtable[key] ~= nil
end

---深度克隆一个值
--@param object 要克隆的值
--@return copyObj
--@usage
-- --下面的代码，t2 是 t1 的引用，修改 t2 的属性时，t1 的内容也会发生变化
-- local t1 = {a = 1, b = 2}
-- local t2 = t1
-- t2.b = 3    -- t1 = {a = 1, b = 3} <-- t1.b 发生变化
-- clone() 返回 t1 的副本，修改 t2 不会影响 t1
-- local t1 = {a = 1, b = 2}
-- local t2 = clone(t1)
-- t2.b = 3    -- t1 = {a = 1, b = 2} <-- t1.b 不受影响
function M.clone(object)
    local lookup_table = {}
    local function _copy(object)
        if type(object) ~= "table" then
            return object
        elseif lookup_table[object] then
            return lookup_table[object]
        end
        local new_table = {}
        lookup_table[object] = new_table
        for key, value in pairs(object) do
            new_table[_copy(key)] = _copy(value)
        end
        return setmetatable(new_table, getmetatable(object))
    end
    return _copy(object)
end


--[[--
将 Lua 对象及其方法包装为一个匿名函数

@usage
~~~ lua

local MyScene = class()

function MyScene:ctor()
    self.frameTimeCount = 0
    -- 注册回调函数
    self:setCallBack(self,self.onEnterFrame)
end

--注册回调函数
function MyScene:setCallBack(obj, method)
    self.callBackObj = obj;
    self.callBackMethod = method;
end

--执行回调函数
function MyScene:doCallBack()
    self.callBackMethod(self.callBackObj);
end

~~~

上述代码执行时没有问题，但是却持有了回调函数的对象（obj）
此时开发者可以访问改对象，并且如果当前类(MyScene) 如果释放不干净
则导致obj也被引用这 释放不掉(lua 强引用)

~~~ lua handler

local MyScene = class()

function MyScene:ctor()
    self.frameTimeCount = 0
    -- 注册回调函数
    self:setCallBack(handler(self,self.onEnterFrame))
end

--注册回调函数
function MyScene:setCallBack(omethod)
    self.callBackMethod = method;
end

--执行回调函数
function MyScene:doCallBack()
    self.callBackMethod();
end

~~~

使用 handler() 的好处是回调的类不需要持有回调函数的类，可以减少引用。

@param obj Lua 对象
@param method 对象方法

@return function
]]
function M.handler(obj, method)
    return function(...)
        if method and obj then
           return method(obj, ...)
        end    
    end
end

return M;