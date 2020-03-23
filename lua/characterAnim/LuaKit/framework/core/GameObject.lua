--[[
	游戏基类
]]

local id_ = 100000;

local allocateID = function( ... )
	id_ = id_ + 1;
	return id_;
end

local GameObject = class();

function GameObject:ctor()
	---对象ID
	self.id__ = allocateID();

	---对象生成时候的时间戳,可以通过这观察整个对象的活动时长
	self.time__ = os.time();
end

function GameObject:dtor()
	
end

function GameObject:getId()
    return self.id__
end

function GameObject:hasBehavior(behaviorName)
    return self.behaviorObjects_ and self.behaviorObjects_[behaviorName] ~= nil
end


---绑定行为（注：Behavior 翻译成 行为）
function GameObject:bindBehavior(behaviorName)
    ---检查是否已经绑定该行为
    if not self.behaviorObjects_ then self.behaviorObjects_ = {} end
    if self.behaviorObjects_[behaviorName] then return end

    ---根据配置表创建行为
    local behavior = BehaviorFactory.createBehavior(behaviorName)

    ---获取行为依赖
    for i, dependBehaviorName in pairs(behavior:getDepends()) do
        --绑定依赖行为
        self:bindBehavior(dependBehaviorName)

        ---以依赖行为名为key，以需要此依赖的行为名做list，记录下来
        if not self.behaviorDepends_ then
            self.behaviorDepends_ = {}
        end
        if not self.behaviorDepends_[dependBehaviorName] then
            self.behaviorDepends_[dependBehaviorName] = {}
        end
        table.insert(self.behaviorDepends_[dependBehaviorName], behaviorName)
    end

    ---将行为上的方法绑定至此object类上
    behavior:bind(self)
    ---以行为名为key，行为的操作对像为vaule记录下来
    self.behaviorObjects_[behaviorName] = behavior
    ---按优先级重置行为
    self:resetAllBehaviors()
end

---反绑定行为
function GameObject:unbindBehavior(behaviorName)
    ---安全措施
    assert(self.behaviorObjects_ and self.behaviorObjects_[behaviorName] ~= nil,
           string.format("GameObject:unbindBehavior() - behavior %s not binding", behaviorName))
    assert(not self.behaviorDepends_ or not self.behaviorDepends_[behaviorName],
           string.format("GameObject:unbindBehavior() - behavior %s depends by other binding", behaviorName))

    ---获取绑定的行为对像
    local behavior = self.behaviorObjects_[behaviorName]
    
    ---从依赖列表里移除需要解绑定行为
    for i, dependBehaviorName in pairs(behavior:getDepends()) do
        for j, name in ipairs(self.behaviorDepends_[dependBehaviorName]) do
            if name == behaviorName then
                table.remove(self.behaviorDepends_[dependBehaviorName], j)
                if #self.behaviorDepends_[dependBehaviorName] < 1 then
                    self.behaviorDepends_[dependBehaviorName] = nil
                end
                break
            end
        end
    end

    ---解绑定方法 
    behavior:unbind(self)
    self.behaviorObjects_[behaviorName] = nil

    ---强制调用dtor
    if true then
       delete(behavior);
    end
end

---按优先级重置行为
function GameObject:resetAllBehaviors()
    if not self.behaviorObjects_ then return end

    local behaviors = {}
    for i, behavior in pairs(self.behaviorObjects_) do
        behaviors[#behaviors + 1] = behavior
    end
    table.sort(behaviors, function(a, b)
        return a:getPriority() > b:getPriority()
    end)
    for i, behavior in ipairs(behaviors) do
        behavior:reset(self)
    end
end

---绑定方法，在行为里使用
function GameObject:bindMethod(behavior, methodName, method, callOriginMethodLast)
    --取出之前的方法
    local originMethod = self[methodName] 
    if not originMethod then
        self[methodName] = method
        return
    end

    if not self.bindingMethods_ then self.bindingMethods_ = {} end
    if not self.bindingMethods_[methodName] then self.bindingMethods_[methodName] = {} end

    local chain = {behavior, originMethod}
    local newMethod
    if callOriginMethodLast then
        newMethod = function(...)
            method(...)
            chain[2](...)
        end
    else
        newMethod = function(...)
            local ret = chain[2](...)
            if ret then
                local args = {...}
                args[#args + 1] = ret
                return method(unpack(args))
            else
                return method(...)
            end
        end
    end

    self[methodName] = newMethod --新的方面 会调用之前的同名方法
    chain[3] = newMethod
    table.insert(self.bindingMethods_[methodName], chain)

    -- print(string.format("[%s]:bindMethod(%s, %s)", tostring(self), behavior:getName(), methodName))
    -- for i, chain in ipairs(self.bindingMethods_[methodName]) do
    --     print(string.format("  index: %d, origin: %s, new: %s", i, tostring(chain[2]), tostring(chain[3])))
    -- end
    -- print(string.format("  current: %s", tostring(self[methodName])))
end

---解绑定方法，在行为里使用
function GameObject:unbindMethod(behavior, methodName)
    if not self.bindingMethods_ or not self.bindingMethods_[methodName] then
        self[methodName] = nil
        return
    end

    local methods = self.bindingMethods_[methodName]
    local count = #methods
    ---从后住前解定
    for i = count, 1, -1 do
        local chain = methods[i]

        if chain[1] == behavior then
            -- print(string.format("[%s]:unbindMethod(%s, %s)", tostring(self), behavior:getName(), methodName))
            if i < count then
                -- 如果移除了中间的节点，则将后一个节点的 origin 指向前一个节点的 origin
                -- 并且对象的方法引用的函数不变
                -- print(string.format("  remove method from index %d", i))
                methods[i + 1][2] = chain[2]
            elseif count > 1 then
                -- 如果移除尾部的节点，则对象的方法引用的函数指向前一个节点的 new
                self[methodName] = methods[i - 1][3]
            elseif count == 1 then
                -- 如果移除了最后一个节点，则将对象的方法指向节点的 origin
                self[methodName] = chain[2]
                self.bindingMethods_[methodName] = nil
            end

            -- 移除节点
            table.remove(methods, i)

            -- if self.bindingMethods_[methodName] then
            --     for i, chain in ipairs(self.bindingMethods_[methodName]) do
            --         print(string.format("  index: %d, origin: %s, new: %s", i, tostring(chain[2]), tostring(chain[3])))
            --     end
            -- end
            -- print(string.format("  current: %s", tostring(self[methodName])))

            break
        end
    end
end


return GameObject;