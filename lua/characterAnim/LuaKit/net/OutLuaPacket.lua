require "alien"
require "alien.struct"
local struct = alien.struct
local OutLuaPacket = {};

function OutLuaPacket:ctor()
	self:reset();
end

function OutLuaPacket:getCmdType()
	-- body
end

function OutLuaPacket:writeInt(value)
	value = value or 0
	local buf = struct.pack(">i4",value)
	table.insert(self.body_buf,buf)
	self.len = self.len + 4
end

function OutLuaPacket:writeUnsignInt(value)
	local buf = struct.pack(">I4",value)
	table.insert(self.body_buf,buf)
	self.len = self.len + 4
end

function OutLuaPacket:writeInt64(value)
	local buf = struct.pack(">i8",value)
	table.insert(self.body_buf,buf)
	self.len = self.len + 8
end

function OutLuaPacket:writeUnsignInt64(value)
	local buf = struct.pack(">I8",value)
	table.insert(self.body_buf,buf)
	self.len = self.len + 8
end

function OutLuaPacket:writeByte(value)
	local buf = struct.pack(">B",value)
	table.insert(self.body_buf,buf)
	self.len = self.len + 1
end

function OutLuaPacket:writeShort(value)
	local buf = struct.pack(">h",value)
	table.insert(self.body_buf,buf)
	self.len = self.len + 2
end

function OutLuaPacket:writeUnsignShort(value)
	local buf = struct.pack(">H",value)
	table.insert(self.body_buf,buf)
	self.len = self.len + 2
end

function OutLuaPacket:writeString(value)
	local len = #value
	local buf = struct.pack('>I4s', len+1, value)
	table.insert(self.body_buf,buf)
	self.len = self.len + len + 5
end

function OutLuaPacket:writeBinary(value)
	local len = #value
	local buf = struct.pack('>I4', len) .. value
	table.insert(self.body_buf,buf)
	self.len = self.len + len + 4
end

function OutLuaPacket:copy(buf)
	self.buf = buf
end

function OutLuaPacket:packetToBuf()
	local buffer = self.body_buf;
	if #buffer ~= 1 then
        buffer = table.concat(buffer)
    else
        buffer = buffer[1]
    end
	return buffer;
end

function OutLuaPacket:packetToSkynet()
	local Buf = self:packetToBuf()
	local skyNetBuf = struct.pack(">I2s",#Buf+1,Buf)
	return skyNetBuf;
end

function OutLuaPacket:reset()
	self.buf = ""
	self.len = 0
	self.body_buf = {}
end


function OutLuaPacket:dtor()
	-- body
end

return OutLuaPacket