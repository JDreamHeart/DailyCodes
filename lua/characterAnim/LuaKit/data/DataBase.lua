--[[--核心数据基类，提供观察者模式监听数据变化
@module DataBase
@author YuchengMo

Date   2017-12-26 11:17:33
Last Modified by   YuchengMo
Last Modified time 2018-04-04 14:29:54

@usage

local test = new(DataBase);
test:init();

local t = {};
t.onNotifyDataChange = function(self,key,value,oldValue)
	dump(value,key)
end

test:addObserver(t) --添加数据变化观察者
test.a = 100;

]]


-- import("framework._load");

local ObserverBehavior = function(self)
 	self.propertyMap_ = {};

    local oldMeta = getmetatable(self)
    if oldMeta == nil then
        oldMeta = {};
    end

    if oldMeta.__index == nil then
        oldMeta.__index = function(t,k,v)
        	return self.propertyMap_[k]
        end;
    else
    	local parent = oldMeta.__index;
    	oldMeta.__index = function(t,k,v)
    		if self.propertyMap_[k] then
    			return self.propertyMap_[k]
    		end
        	if parent[k] then
        		return parent[k];
        	end
        end;
    end
    

    oldMeta.__newindex = function(t,k,v)
    	local oldV = self[k];
    	if self.isLock == true then
    		if oldV == nil then
    			error("不允许新写入数据，如果要写入数据，必须绑定自定义数据组件，调用initData初始化数据")
    		end
    	end
    	self.propertyMap_[k] = v;  
    	self:notify(k,v,oldV)	
    end
    setmetatable(self,oldMeta)    
end

local DataBase = class()

function DataBase:ctor()
	---清理需要移除的对象
	self.willRemove_ = false;
	---正在进行观察回调，为了避免在回调李动态修改观察者数量
	self.isNotifying_ = false;
	self.isLockData = false;
	self.mObservers = {};
end

---初始化观察者模式
function DataBase:init()
	ObserverBehavior(self)
end

function DataBase:initData(data)
	data = checktable(data);
	local oldMeta = getmetatable(self)
    if oldMeta == nil then
        oldMeta = {};
    end
    if oldMeta.__index == nil then
        oldMeta.__index = {};
    end
    local object = oldMeta.__index;
    table.deepMerge(object,data)
end

---是否加锁，默认不加锁，加锁之后不允许新增字段,如果要写入数据,必须绑定自定义数据组件，调用initData初始化数据
function DataBase:lock(flag)
	self.isLock = flag
end


--[[--
添加观察者
@param obj 观察者对象，必须实现onNotifyDataChange接口

]]
function DataBase:addObserver(obj)
	assert(obj.onNotifyDataChange,"必须实现onNotifyDataChange该函数")
	table.insert(self.mObservers,obj);
end

--[[--
移除观察者
@param obj 观察者对象

]]
function DataBase:removeObserver(obj)
	if self.isNotifying_ == true then
		for i,v in ipairs(self.mObservers) do
			v.isMaskRemove_ = true;
			self.willRemove_ = true;
		end
	else
		table.removeByValue(self.mObservers,obj);
	end
end

--[[--
清理所有被标记要移除的对象
]]
function DataBase:clean()
	if self.willRemove_ == true then
		self.willRemove_ = false;
		for i,v in pairs(self.mObservers) do
			if v.isMaskRemove_ == true then
				-- dump(v)
				self:removeObserver(v)

			end
		end

	end
end

--[[--
进行消息通知派发
]]
function DataBase:notify(key,value,oldValue)
	self.isNotifying_ = true;
	for i,v in ipairs(self.mObservers) do
    	if v.onNotifyDataChange and v.isMaskRemove_ ~= true then
    		v:onNotifyDataChange(key,value,oldValue,self)
    	end
    end
    self.isNotifying_ = false;
    self:clean();
end


-- local Player = class(DataBase);

-- function Player:ctor( ... )

-- end

-- function Player:reset()
--     self.localSeat       = -1;   ---本地座位号，初始化的时候就确定
--     self.serverSeat      = -1;   ---server座位号

--     self.mid        = -1;       ---玩家id
--     self.sex        = -1;       ---玩家性别
--     self.level      = -1;       ---玩家等级
--     self.exp        = -1;       ---玩家经验
--     self.nick       = "9527_默认名称";      ---玩家昵称

--     self.money          = -1;       ---玩家银币(对于德州来说，这就是房间内银币)
--     self.isAI           = false;    ---玩家ai状态
--     self.isReady        = false;    ---玩家准备状态
--     self.winCount       = -1;       ---玩家赢的局数
--     self.loseCount      = -1;       ---玩家输的局数
--     self.pingJuCount    = -1;   ---平局数量
--     self.diamond        = -1;   --玩家兑换券
--     self.userId         = -1;   --玩家userid
--     self.jsonInfo       = ""; -- 玩家json数据
-- end


-- local p1 = new(Player)
-- p1:init()
-- p1:reset()
-- p1.money = 100;
-- dump(p1)



-- local p2 = new(Player)
-- p2:init()
-- p2:reset()
-- p1.money = 102;
-- dump(p1)


return DataBase;