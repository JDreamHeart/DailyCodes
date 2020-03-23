--[[--核心socket模块，主要处理收发包
@module BaseSocket
@author YuchengMo

Date   2017-12-26 14:15:05
Last Modified by   YuchengMo
Last Modified time 2018-04-26 20:00:48
]]


require "alien"
require "alien.struct"
local struct = alien.struct
local socket = require("socket")
local BaseSocket = class();

function BaseSocket:ctor()
	self.mBodyWriters = {};
	self.mBodyReaders = {};
end

function BaseSocket:dtor( ... )
	-- body
end

--[[--
初始化包头配置
]]
function BaseSocket:initHeadConfig(config)
	self.headConfig = config;
end


function BaseSocket:setSocket(socket)
	self.mSock = socket;
end

function BaseSocket:getSocket()
	return self.mSock;
end

function BaseSocket:connect(ip,port,func)
	local sock = socket.connect(ip, port);
	sock:settimeout(60)
	if sock == nil then
		self:onConnecteFailed();
		return;
	end
	self:setSocket(sock);
	func(self);
	self:onConnected(sock)

	return sock;
end


function BaseSocket:onConnecteFailed()
	dump("连接失败......")
	
end

function BaseSocket:onConnected(sock)
	
	-- self:startRecv();
	-- -- self:sendMsg(101,{a=1234}) -- 测试代码

 --    if self.connectCB then
	-- 	self.connectCB(sock)
	-- end
	-- dump(sock)
	while true do
	    local recvt, sendt, status = socket.select({sock}, nil, 1)
	    while #recvt > 0 do
	    	-- print(status,recvt,sendt)
	        local receive_status,cmd,len = self:onReadHead(sock);
	        if receive_status ~= "closed" then
	        	local data = nil;
	           	if len > 0 then
	           		print(len)
	           		local bodyBuf, receive_status = sock:receive(len)
	           		if receive_status ~= "closed" then
	           			data = self:readBody(cmd,bodyBuf);
	           		else
	           			break;
	           		end
	           	end
	           	self:onRecv(cmd,data)
	        else
	            break
	        end
	    end
	end
end

function BaseSocket:startRecv(sock)
	local recvSock = sock or self.mSock;
	self.m_RecvedHandle = tasklet.spawn(handler(self, self.received),recvSock)
end

--[[--
发送消息
@param cmd 消息命令字
@param data 消息体，一般对应PB表结构
@op  可选操作，比如处理超时等

]]
function BaseSocket:sendMsg(cmd,data,op)
	assert(self.mSock,"socket 没连接上")
	local bodyBuf = self:writeBody(cmd,data);
	dump(#bodyBuf,"bodyBuf")
	local headBuf = self:onWriteHead(cmd,#bodyBuf)
	local buf = nil
	if bodyBuf then
		buf = headBuf .. bodyBuf;
	else
		buf = headBuf;
	end
	self.mSock:send(buf)

end


--[[--
接收到消息的处理
]]
function BaseSocket:received(sock)
	-- body
	while sock and sock:status() == "normal" do
		local headBuf = sock:read(self.headConfig.len)
		if headBuf == nil and sock and sock:status() ~= "normal" then
       		return;
    	end
		local len,cmd = self:onReadHead(headBuf,self.headConfig)
		local bodyLen = len - self.headConfig.len;
		-- dump(bodyLen,"bodyLen")
		-- print(getSubBuf(buf,self.headConfig.len+1),"myc")
		local bodyData = nil;
		if bodyLen > 0 then
			local bodyBuf = sock:read(bodyLen)
			if bodyBuf == nil and sock and sock:status() ~= "normal" then
       			return;
    		end
			bodyData = self:readBody(cmd,bodyBuf);
		end
		self.mMsgQueen:onRecv(cmd,bodyData);
		-- dump(cmd);
	end
end


function BaseSocket:onRecv(cmd,data)
	-- dump(data,cmd)
	if self.onRecvMsg then
		dump(cmd,data)
		self:onRecvMsg(cmd,data)
	end
end

--[[--
	设置包头处理
]]
function BaseSocket:onWriteHead(cmd,bodyLen)
	-- error("需要自行实现读包头接口")
	local len  = 7 + bodyLen;
	local head = struct.pack('>I2',100);
	return head;
end


function BaseSocket:onReadHead(sock)
	local headBuf, receive_status = sock:receive(9)
    if receive_status == "closed"  then
        return receive_status;
    end
    local len,cmd,type,position
    position = 1

    len,cmd,type,position = struct.unpack('>I4I4I1',headBuf,position)
    -- print("receive_status",receive_status,len,cmd)
    local bodyLen = len - 9;
	return receive_status,cmd,bodyLen;
end

function BaseSocket:writeBody(cmd,data)
	for i,writer in ipairs(self.mBodyWriters) do
		local BodyBuf = writer:writePacket(cmd,data);
		if BodyBuf then
			return BodyBuf;
		end
	end
end

function BaseSocket:readBody(cmd,bodyBuf)
	for i,reader in ipairs(self.mBodyReaders) do
		local BodyData = reader:readPacket(cmd,bodyBuf);
		if BodyData then
			return BodyData;
		end
	end
end



function BaseSocket:addBodyWriter(bodyWriter)
	table.insert(self.mBodyWriters,1,bodyWriter)
end


function BaseSocket:addBodyReader(bodyReader)
	table.insert(self.mBodyReaders,1,bodyReader)
end




return BaseSocket;



-- local GameWriter = {}

-- function GameWriter:writePacket(cmd,data)
-- 	if self:checkCmd(cmd) == true then
-- 		return cjson.encode(data);
-- 	end
	
-- end

-- function GameWriter:checkCmd(cmd)
-- 	return true;
-- end


-- local GameReader = {}

-- function GameReader:readPacket(cmd,bodyBuf)

-- 	if self:checkCmd(cmd) == true then
-- 		print(bodyBuf)
-- 		return bodyBuf;
-- 	end
	
-- end

-- function GameReader:checkCmd(cmd)
-- 	return true;
-- end


-- local sock = new(BaseSocket)


-- sock:initHeadConfig({gameId = 1,len = 13})

-- sock:addBodyWriter(GameWriter);

-- sock:addBodyReader(GameReader);

-- sock.onWriteHead = function(self,cmd,bodyLen,headConfig)
-- 	local len = headConfig.len + bodyLen;
-- 	print(len)
-- 	local gameId = headConfig.gameId;
-- 	local head = struct.pack('>I4I4I4I1',len,cmd,gameId,0);
-- 	return head;
-- end


-- sock.onReadHead = function(self,headBuf,headConfig)
-- 	local len,cmd,msgType 
-- 	local position = 1;
--     len,cmd,msgType,position = struct.unpack('>I4I4I4I1',headBuf,position)
-- 	return len,cmd;
-- end


-- local sendBuf = sock:sendMsg(101,{a=2});

-- sock:received(sendBuf)

