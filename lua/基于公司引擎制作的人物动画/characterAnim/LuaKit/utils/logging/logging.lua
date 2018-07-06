-------------------------------------------------------------------------------
-- includes a new tostring function that handles tables recursively
--
-- @author Danilo Tuler (tuler@ideais.com.br)
-- @author Andre Carregal (info@keplerproject.org)
-- @author Thiago Costa Ponte (thiago@ideais.com.br)
--
-- @copyright 2004-2011 Kepler Project
-------------------------------------------------------------------------------

local type, table, string, _tostring, tonumber = type, table, string, tostring, tonumber
local select = select
local error = error
local format = string.format
local print = print;
local ipairs = ipairs;
local pairs = pairs;
local getmetatable = getmetatable;
local table_format = string.format
local string_len = string.len
local string_rep = string.rep


local logging = {};

-- Meta information
local _COPYRIGHT = "Copyright (C) 2004-2011 Kepler Project"
local _DESCRIPTION = "A simple API to use logging features in Lua"
local _VERSION = "LuaLogging 1.2.0"

-- The DEBUG Level designates fine-grained instring.formational events that are most
-- useful to debug an application
local DEBUG = "DEBUG"

-- The INFO level designates instring.formational messages that highlight the
-- progress of the application at coarse-grained level
local INFO = "INFO"


local VERBOSE = "VERBOSE"

-- The WARN level designates potentially harmful situations
local WARN = "WARN"


-- The ERROR level designates error events that might still allow the
-- application to continue running
local ERROR = "ERROR"

-- -- The FATAL level designates very severe error events that will presumably
-- -- lead the application to abort
-- FATAL = "FATAL"

---日志优先级 1            2     3       4        5
local LEVEL = {"VERBOSE","DEBUG","INFO", "WARN", "ERROR"}
-----其优先级分别为：ERROR>WARN>INFO>DEBUG>VERBOSE

local MAX_LEVELS = #LEVEL
-- make level names to order
for i=1,MAX_LEVELS do
    LEVEL[LEVEL[i]] = i
end

-- private log function, with support for formating a complex log message.
-- local function LOG_MSG(self, level, fmt, ...)
-- 	local f_type = type(fmt)
-- 	if f_type == 'string' then
-- 		if select('#', ...) > 0 then
-- 			return self:append(level, format(fmt, ...))
-- 		else
-- 			-- only a single string, no formating needed.
-- 			return self:append(level, fmt)
-- 		end
-- 	elseif f_type == 'function' then
-- 		-- fmt should be a callable function which returns the message to log
-- 		return self:append(level, fmt(...))
-- 	end
-- 	-- fmt is not a string and not a function, just call tostring() on it.
-- 	return self:append(level, tostring(fmt))
-- end

local function getString( ... )
    local strList = {};
    local arg = {...}
    for i,v in ipairs(arg) do
        if type(v) == "table" then
            strList[#strList+1] = tostring(v)
        elseif type(v) == "UserData" then
            strList[#strList+1] = "UserData";
        else
            strList[#strList+1] = _tostring(v);
        end
    end
    local msgStr = table.concat(strList, ",");
    return msgStr
end


local function LOG_MSG(self, level,...)
    local msg = getString(...)
    return self:append(level, msg)
end



-- create the proxy functions for each log level.
local LEVEL_FUNCS = {}
for i=1,MAX_LEVELS do
    local level = LEVEL[i]
    LEVEL_FUNCS[i] = function(self, ...)
        -- no level checking needed here, this function will only be called if it's level is active.
        return LOG_MSG(self, level, ...)
    end
end

-- do nothing function for disabled levels.
local function disable_level() end

-- improved assertion funciton.
local function assert(exp, ...)
    -- if exp is true, we are finished so don't do any processing of the parameters
    if exp then return exp, ... end
    -- assertion failed, raise error
    error(format(...), 2)
end

-------------------------------------------------------------------------------
-- Creates a new logger object
-- @param append Function used by the logger to append a message with a
--	log-level to the log stream.
-- @return Table representing the new logger object.
-------------------------------------------------------------------------------
function logging.new(append)

    if type(append) ~= "function" then
        return nil, "Appender must be a function."
    end

    local logger = {}
    logger.append = append

    logger.setLevel = function (self, level)
        local order = LEVEL[level]
        assert(order, "undefined level `%s'", _tostring(level))
        self.level = level
        self.level_order = order
        -- enable/disable levels
        for i=1,MAX_LEVELS do
            local name = LEVEL[i]:lower()
            if i >= order then
                self[name] = LEVEL_FUNCS[i]
            else
                self[name] = disable_level
            end
        end
    end

    -- generic log function.
    logger.log = function (self, level, ...)
        local order = LEVEL[level]
        assert(order, "undefined level `%s'", _tostring(level))
        if order < self.level_order then
            return
        end
        return LOG_MSG(self, level, ...)
    end

    -- initialize log level.
    logger:setLevel(VERBOSE)

    logger.getLevel = function(self,level)
        local lv = LEVEL[level:upper()]
        return lv;
    end

    return logger
end


-------------------------------------------------------------------------------
-- Prepares the log message
-------------------------------------------------------------------------------
function logging.prepareLogMsg(pattern, dt, level, message)

    local logMsg = pattern or "%date %level %message\n"
    message = string.gsub(message, "%%", "%%%%")
    logMsg = string.gsub(logMsg, "%%date", dt)
    logMsg = string.gsub(logMsg, "%%level", level)
    logMsg = string.gsub(logMsg, "%%message", message)
    return logMsg
end




---数列化table 报错到文件
--@string t 表
--@string tabName 表名
--@retrurn tableStr
function logging.tostring(t)
    local function dump(value, desciption, nesting)
        local lookup = {}
        local result = {}
        if type(nesting) ~= "number" then nesting = 10 end

        local function _dump_value(v)
            if type(v) == "string" then
                v = string.format("%q", v)
            end
            if type(v) == "function" then
                v = string.format("%q", _tostring(v))
            end
            return _tostring(v)
        end
        local function _dump_key(v)
            -- if type(v) == "number" then
            --     v = "[" .. v .. "]"
            -- end
            return v
        end
        local function _dump(value, desciption, indent, nest, keylen)
            desciption = desciption or "<var>"
            local spc = ""
            if type(keylen) == "number" then
                spc = string_rep(" ", keylen - string_len(_dump_value(desciption)))
            end

            if type(value) ~= "table" then
                result[#result +1 ] = table_format("%s%s%s = %s,", indent, _dump_key(desciption), spc, _dump_value(value))
            elseif lookup[_tostring(value)] then
                result[#result +1 ] = table_format("%s%s%s = *REF*", indent, desciption, spc)
            else
                lookup[_tostring(value)] = true
                if nest > nesting then
                    result[#result +1 ] = table_format("%s%s = *MAX NESTING*", indent, desciption)
                else
                    result[#result +1 ] = table_format("%s%s = {", indent, _dump_key(desciption))
                    local indent2 = indent.."    "
                    local keys = {}
                    local keylen = 0
                    local values = {}
                    for k, v in pairs(value) do
                        if k~="___message" then
                            keys[#keys + 1] = k
                            local vk = _dump_value(k)
                            local vkl = string_len(vk)
                            if vkl > keylen then keylen = vkl end
                            values[k] = v
                        end
                    end
                    table.sort(keys, function(a, b)
                        if type(a) == "number" and type(b) == "number" then
                            return a < b
                        else
                            return tostring(a) < tostring(b)
                        end
                    end)
                    for i, k in ipairs(keys) do
                        _dump(values[k], k, indent2, nest + 1, keylen)
                    end
                    result[#result +1] = table_format("%s}", indent)
                end
            end
        end

        _dump(value, desciption, "", 1)
        -- result[1]       = "{";
        -- result[#result] = "}";

        local ret = {};
        for i, line in ipairs(result) do
            -- ret = ret .. line .. "\n";
            table.insert(ret,line)
        end
        return table.concat(ret,"\n");
    end

    return dump(t);
end


-----------------------------------------------------------------------------
-- Converts a Lua value to a string

-- Converts Table fields in alphabetical order
-----------------------------------------------------------------------------


-- function tostring(value)


--     local str = ''
--     if (type(value) ~= 'table') then
--         if (type(value) == 'string') then
--             str = string.format("%q", value)
--         else
--             str = _tostring(value)
--         end
--     else
--     	if not value then return "nil"; end
-- 	    local mt = getmetatable(value);
-- 	    if mt and mt.__tostring then
-- 	        return _tostring(value);
-- 	    end


--         local auxTable = {}
--         table.foreach(value, function(i, v)
--             if (tonumber(i) ~= i) then
--                 table.insert(auxTable, i)
--             else
--                 table.insert(auxTable, tostring(i))
--             end
--         end)
--         table.sort(auxTable)

--         str = str..'{'
--         local separator = ""
--         local entry = ""
--         table.foreachi (auxTable, function (i, fieldName)
--             if ((tonumber(fieldName)) and (tonumber(fieldName) > 0)) then
--                 entry = tostring(value[tonumber(fieldName)])
--             else
--                 entry = fieldName.." = "..tostring(value[fieldName])
--             end
--             str = str..separator..entry
--             separator = ", "
--         end)
--         str = str..'}'
--     end
--     return str
-- end

return logging;