--
-- Author: Your Name
-- Date: 2017-06-09 10:12:51
--
import("logging");
import("console");
local logger = logging.console("%date %level %message")

local Log = {};

g_LogLevel = 1

function string.split(str, delimiter)
	if (delimiter == '') then return false end
	local pos, arr = 0, {}
	-- for each divider found
	for st, sp in function() return string.find(str, delimiter, pos, true) end do
		table.insert(arr, string.sub(str, pos, st - 1))
		pos = sp + 1
	end
	table.insert(arr, string.sub(str, pos))
	return arr
end

function string.trim(str, char)
	if (char == '' or char == nil) then
		char = '%s'
	end

	local trimmed = string.gsub(str, '^' .. char .. '*(.-)' .. char .. '*$', '%1')
	return trimmed
end


---日志优先级    1          2        3       4        5
local LEVEL = {"VERBOSE", "DEBUG", "INFO", "WARN", "ERROR"}
-----其优先级分别为：ERROR>WARN>INFO>DEBUG>VERBOSE


function Log.init(iTableWrap)
	Log.protobuf = import ("protobuf");
	Log.iTableWrap = iTableWrap;
end

function Log.base(func,...)
	local msg,logLevel
	logLevel = logger:getLevel(func);
	if logLevel < g_LogLevel then
		return
	end

	local traceback = string.split(debug.traceback("", 2), "\n")
    local str = "log from: " .. string.trim(traceback[3]) .. "\n";
	msg = logger[func](logger,...)
	str = str .. msg;
	Log.writeToRemote(str,level)

end

function Log.writeToRemote(msg,level)
	if Log.protobuf and Log.iTableWrap then
		--日志转protobuf
		local logTable = {
			pBuf 		= msg;
			iModInt 	= level;
			iWriteType 	= 1;
		}
		local encodeBuf = Log.protobuf.encode("so_lua_param.LogData",logTable);				
		--参数设置，传入与传出都是此参数
		local param = LuaParam();
		param:setParam(encodeBuf);
				
		--调用C++接口写日志
		Log.iTableWrap:WriteLog(param);
	else
		print(msg)
	end
end

function Log.v(...)
	Log.base("verbose",...)
end

function Log.d(...)
	Log.base("debug",...)
end

function Log.i(...)
	Log.base("info",...)
end

function Log.w(...)
	Log.base("warm",...)
end

function Log.e(...)
	Log.base("error",...)
end


-- local t = {}
-- t.a = "2"

-- local data = {a=1}
-- setmetatable(data, {__tostring = function( ... )
-- 	return "a"
-- end})
-- t.data = data
-- -- print(tostring(data))
Log.v("TableDB:initSoInfo", "12")
-- print(os.date())