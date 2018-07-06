--[[--ldoc 测试用,只能一对一 ，换句话说只能连接一个客户端
@module QPServerTestSocket
@author YuchengMo

Date   2017-12-27 16:27:45
Last Modified by   YuchengMo
Last Modified time 2018-04-04 14:29:10
]]


local tasklet = import('tasklet')
local socket = import("network.socket2");

local BaseSocket = import(".BaseSocket")
local QPServerTestSocket = class(BaseSocket);


function QPServerTestSocket:ctor( ... )
-- body
    self.packetId = 0;
end

function QPServerTestSocket:dtor( ... )
-- body
end


function QPServerTestSocket:startServer(ip,port)
    socket.spawn_server(ip, port, function(sock)
        print_string('server new connection')
        sock:set_on_closed(function(reason)

       	end)
        -- recv packet
        self:setSocket(sock)
        while true do
            local cmd, data = self:serverReceived(sock)
            dump(data,cmd)
            if cmd == 101 then
                self:sendMsg(102, data)
            end
        end
    end)
end

--[[--
接收到消息的处理
]]
function QPServerTestSocket:serverReceived(sock)
	-- body
	local headBuf = assert(sock:read(self.headConfig.len))
	local len,cmd = self:onReadHead(headBuf,self.headConfig)
	local bodyLen = len - self.headConfig.len;
	-- print(getSubBuf(buf,self.headConfig.len+1),"myc")
	local bodyBuf = assert(sock:read(bodyLen))
	
	local bodyData = self:readBody(cmd,bodyBuf);

	self.packetId = self.packetId + 1;

	return cmd,bodyData
end


return QPServerTestSocket;
