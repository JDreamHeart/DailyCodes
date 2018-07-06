

local System = BYEngine.System;

local logging = import(".logging");
import(".file");




function io.exists(path)
	local file,err = io.open(path, "r")
	if file then
		io.close(file)
		-- print("path " .. path);
		return true
	end
	-- print("err " .. err);
	return false
end


---把上次的日子按时间重命名保存下来
local lastLogTime = nil;
local oldname = sys_get_string("storage_log")  .. "0_log.log"
if io.exists(oldname) then
	local file = io.open(oldname, "r")  
	for line in file:lines() do
	    if string.contains(line,"INFO startTime=") then
	    	local list = string.split(line,"=")
	    	lastLogTime = tonumber(list[2]);
	    	break;
	    end
	end
	io.close(file)
	if lastLogTime ~= nil then
		local fileName = os.date("%Y_%m_%d_%H_%M_%S",lastLogTime);
		local newname = sys_get_string("storage_log")  .. fileName .. ".log"
		os.rename(oldname, newname)
	end
	-- error(1)
end

local logFile = sys_get_string("storage_log") .. "0_log.log"
local logger = logging.file(logFile)

local Log = {};

local tracebackLevel = 3;--堆栈深度

---日志优先级 1            2     3       4        5
local LEVEL = {"VERBOSE","DEBUG","INFO", "WARN", "ERROR"}
-----其优先级分别为：ERROR>WARN>INFO>DEBUG>VERBOSE

local g_LogLevel = 0;
function Log.base(func,tracebackLevel,...)
	local msg,logLevel
	logLevel = logger:getLevel(func);
	if logLevel < g_LogLevel then
		return
	end
	local str = "log from: "
	local traceback = string.split(debug.traceback("", tracebackLevel), "\n")
	if traceback[3] then
		str = str .. string.trim(traceback[3]) .. "\n";
	end
	msg = logger[func](logger,...)
	str = str .. tostring(msg);
	Log.writeToRemote(str,logLevel)
end

function Log.writeToRemote(msg,logLevel)
	print_string(msg)
	if logging and logging.writeToFile then
		logging.writeToFile(logFile, msg)
	end
end

function Log.v(...)
	-- sys_set_int("win32_console_color", 7)
	Log.base("verbose",tracebackLevel,...)
	-- sys_set_int("win32_console_color", 7)
end

function Log.d(...)
	Log.base("debug",tracebackLevel,...)
end

function Log.i(...)
	sys_set_int("win32_console_color", 10)
	Log.base("info",tracebackLevel,...)
	sys_set_int("win32_console_color", 7)
end

function Log.w(...)
	Log.base("warn",tracebackLevel,...)
end

function Log.e(...)
	Log.base("error",tracebackLevel,...)
end

function Log.clearLogFiles()
	local logDir = sys_get_string("storage_log")
	local files = os.lsfiles(logDir)
	local curTimestamp = os.time();
	for i,v in pairs(files) do
	    if io.exists(v) and not string.contains(v,"0_log.log") then
			local file = io.open(v, "r") 
			local isRemove = false; 
			for line in file:lines() do
			    if string.contains(line,"INFO startTime=") then
			    	local list = string.split(line,"=")
			    	lastLogTime = tonumber(list[2]);
			    	if curTimestamp - lastLogTime >= BYKit.BYKitConfig.logTimestamp   then  		
			    		isRemove = true;
			    		break;
			    	end	
			    end
			end
			file:close();
			if isRemove then
				System.removeFile(v);
			end	
	    end
	end
end

Log.i(string.format("startTime=%d",os.time())) --记录日志时间

return Log