-- server.lua

require("Luakit._load");
local socket = require("socket")
require "alien"
require "alien.struct"
require("json")
local struct = alien.struct

local host = "127.0.0.1"
local port = 8888
local server = assert(socket.bind(host, port, 1024))
server:settimeout(0)
local client_tab = {}
local conn_count = 0
 
print("Server Start " .. host .. ":" .. port) 

local OutLuaPacket = require("OutLuaPacket")
local InLuaPacket = require("InLuaPacket")

local onRecv = function(sock)
    ---处理包头
    local headBuf, receive_status = sock:receive(9)
    if receive_status == "closed" then
        return receive_status;
    end
    local len,cmd,type,position
    position = 1
    len,cmd,type,position = struct.unpack('>I4I4I1',headBuf,position)
    dump(string.format("0x%x",cmd),len)

    local bodyLen = len - 9;
    local buf, receive_status = sock:receive(bodyLen)
    if receive_status == "closed" then
        return receive_status;
    end
  
    local data = headBuf .. buf;
    return receive_status,data

end

while 1 do

    local conn = server:accept()
    if conn then
        conn_count = conn_count + 1
        client_tab[conn_count] = conn
        print("A client successfully connect!") 
    end
  
    for conn_count, client in pairs(client_tab) do
        local recvt, sendt, status = socket.select({client}, nil, 1)
        if #recvt > 0 then
            local receive_status,receive = onRecv(client)
            if receive_status ~= "closed" then
                client:send(receive);
                print("receive1: ", #receive)
            else
                table.remove(client_tab, conn_count) 
                client:close() 
                print("Client " .. conn_count .. " disconnect!") 
            end
        end
         
    end
end