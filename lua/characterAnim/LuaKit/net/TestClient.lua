-- client.lua
local socket = require("socket")
require("pbc.protobuf")
require("Luakit._load");
local cjson = require("json")

local BaseSocket = require("BaseSocket");

-- local host = "127.0.0.1"
-- local port = 8888

local host = "47.106.87.33"
local port = 9558

local GameSocket = new(BaseSocket)

local OutLuaPacket = require("OutLuaPacket")
local InLuaPacket = require("InLuaPacket")


-- local out = new(OutLuaPacket);
-- out:writeString("11111111111111");
-- local buf = out:packetToBuf();
-- local inPack = new(InLuaPacket,buf);
-- local a = inPack:readString()
-- dump(a)



local GameWriter = {}

function GameWriter:writePacket(cmd,data)
	if self:checkCmd(cmd) == true then
		local out = new(OutLuaPacket)
		out:writeString(cjson.encode(data))
		return out:packetToBuf();
	end
end

function GameWriter:checkCmd(cmd)
	return true;
end


local GameReader = {}

function GameReader:readPacket(cmd,bodyBuf)

	if self:checkCmd(cmd) == true then
		print(bodyBuf)
		return bodyBuf;
	end
	
end

function GameReader:checkCmd(cmd)
	return true;
end



local GameReader = {}

function GameReader:readPacket(cmd,bodyBuf)

	if self:checkCmd(cmd) == true then
		local inPack = new(InLuaPacket,bodyBuf);
		local a = inPack:readString()
		return a;
	end
	
end

function GameReader:checkCmd(cmd)
	return true;
end

GameSocket:addBodyReader(GameReader);

GameSocket:addBodyWriter(GameWriter)

function GameSocket:onRecvMsg(cmd,data)
	if cmd == 10 then
		input = io.read()
	    if #input > 0 then
	        self:sendMsg(10,{msg = input})
	    else
	    	self:sendMsg(10,{msg = "myc"})
	    end
	end
end


GameSocket:connect(host, port,function(sock)
	sock:sendMsg(10,{msg = 1})
end)




-- print("conneting")
-- local sock = assert(socket.connect(host, port))
-- sock:settimeout(1)


-- print("conneting1111111111111111")
-- local lasttime = os.time();
-- time = os.time();
-- local handle = nil;



-- local flag = true;

-- local input, recvt, sendt, status
-- while true do

--     input = io.read()
--     if #input > 0 then
--         assert(sock:send(input .. "\n"))
--     end

--     recvt, sendt, status = socket.select({sock}, nil, 1)
--     while #recvt > 0 do
--         local response, receive_status = sock:receive()
--         if receive_status ~= "closed" then
--             if response then
--                 print("echo response",response)
--                 recvt, sendt, status = socket.select({sock}, nil, 1)
--             end
--         else
--             break
--         end
--     end

-- end

