require "alien"
require "alien.struct"
local struct = alien.struct

local InLuaPacket = {};
function InLuaPacket:ctor(buf)
	self.buf = ""
	self.position = 1

	if buf then
		self:copy(buf);
	end
end

function InLuaPacket:getCmdType()
	return self.m_cmd
end

function InLuaPacket:readInt()
	local ret = 0
	if self.position + 3 <= #self.buf then
		ret,self.position = struct.unpack('>I4',self.buf,self.position)
	end
	return ret
end

function InLuaPacket:readUnsignInt()
	local ret
	ret,self.position = struct.unpack('>I4',self.buf,self.position)
	return ret
end

function InLuaPacket:readInt64()
	local ret
	ret,self.position = struct.unpack('>i8',self.buf,self.position)
	return ret
end

function InLuaPacket:readUnsignInt64()
	local ret
	ret,self.position = struct.unpack('>I8',self.buf,self.position)
	return ret
end

function InLuaPacket:readShort()
	local ret
	ret,self.position = struct.unpack('>h',self.buf,self.position)
	return ret
end

function InLuaPacket:readUnsignShort()
	local ret
	ret,self.position = struct.unpack('>H',self.buf,self.position)
	return ret
end

function InLuaPacket:readByte()
	local ret
	ret,self.position = struct.unpack('>B',self.buf,self.position)
	return ret
end

function InLuaPacket:readString()
	-- do return self:readBinary() end  --兼容线上环境的读包方式
	local len = self:readInt()
	local ret
	ret,self.position = struct.unpack('c' .. tostring(len-1),self.buf,self.position)
	self.position = self.position + 1
	return ret
end

function InLuaPacket:readString()
	local len = self:readInt()
	if len == 1 then
		do
			local ret
			ret,self.position = struct.unpack('c' .. tostring(len),self.buf,self.position)
			self.position = self.position
			return ret
		end
	end
	local ret
	ret,self.position = struct.unpack('c' .. tostring(len-1),self.buf,self.position)
	self.position = self.position + 1
	return ret
end

function InLuaPacket:readBinary()
	local len = self:readInt()
	local ret
	ret,self.position = struct.unpack('c' .. tostring(len),self.buf,self.position)
	self.position = self.position
	return ret
end

function InLuaPacket:reset()
	self.buf = ""
	self.position = 1
	self.m_cmd = 0
	self.len = 0
end

function InLuaPacket:copy(buf)
	if type(buf) == "string" then
		self.buf = buf
		self.position = 1
		-- error(#self.buf)
		return;
	end
	-- 兼容线上环境的读包方式
	if type(buf) == "table" then
		self.buf = buf.buf;
		self.position = buf.position;
		self.m_cmd = buf.m_cmd;
		self.len = buf.len;
		return;
	end
end



function InLuaPacket:dtor()
	-- body
end

return InLuaPacket