--[[--ldoc desc
@module QEHeadBehavior
@author 莫玉成

Date   2017-12-27
Last Modified by   YuchengMo
Last Modified time 2017-12-28 14:44:27
]]


local QEHeadBehavior = class(BehaviorBase)
QEHeadBehavior.className_  = "QEHeadBehavior";

function QEHeadBehavior:ctor()
    QEHeadBehavior.super.ctor(self, "QEHeadBehavior", nil, 1)
end


function QEHeadBehavior:dtor()
	
end

---对外导出接口
local exportInterface = {
    "onWriteHead",
    "onReadHead",
    "hello",
}

---对外暴露的接口
function QEHeadBehavior:onWriteHead(object,cmd,bodyLen,headConfig)
	local len = headConfig.len + bodyLen;
	local gameId = headConfig.gameId;
	local head = struct.pack('>I4I4I4I1',len,cmd,gameId,0);
	return head;
end




function QEHeadBehavior:hello(object,cmd,bodyLen,headConfig)
    -- error(1)
end


---对外暴露的接口
function QEHeadBehavior:onReadHead(object,headBuf,headConfig)
    local len,cmd,gameid,msgType
    local position = 1;
    len,cmd,gameid,msgType,position = struct.unpack('>I4I4I4I1',headBuf,position)
    return len,cmd;
end


function QEHeadBehavior:bind(object)
    for i,v in ipairs(exportInterface) do
        object:bindMethod(self, v, handler(self, self[v]),true);
    end
end



function QEHeadBehavior:unBind(object)
    for i,v in ipairs(exportInterface) do
        object:unbindMethod(self, v);
    end 
end

function QEHeadBehavior:reset(object)

end

return QEHeadBehavior;