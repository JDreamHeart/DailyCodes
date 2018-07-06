
---扩展引擎ui
local BehaviorEx = function(ClassExtend)
	---是否有组件
	function ClassExtend:hasBehavior(behaviorName)
	    return self.behaviorObjects_ and self.behaviorObjects_[behaviorName] ~= nil
	end

	function ClassExtend:getBehavior(behaviorName)
	    return self.behaviorObjects_[behaviorName]
	end

	---绑定组件
	--@string behaviorName 组件名称
	function ClassExtend:bindBehavior(behaviorName, params)
	    if not self.behaviorObjects_ then self.behaviorObjects_ = {} end
	    if self.behaviorObjects_[behaviorName] then return end

	    local behavior = BehaviorFactory.createBehavior(behaviorName,params)
	    for i, dependBehaviorName in pairs(behavior:getDepends()) do
	        self:bindBehavior(dependBehaviorName)

	        if not self.behaviorDepends_ then
	            self.behaviorDepends_ = {}
	        end
	        if not self.behaviorDepends_[dependBehaviorName] then
	            self.behaviorDepends_[dependBehaviorName] = {}
	        end
	        table.insert(self.behaviorDepends_[dependBehaviorName], behaviorName)
	    end

	    behavior:bind(self)
	    self.behaviorObjects_[behaviorName] = behavior
	    self:resetAllBehaviors()
	end

	---解绑组件
	--@string behaviorName 组件名称
	function ClassExtend:unBindBehavior(behaviorName)
	    assert(self.behaviorObjects_ and self.behaviorObjects_[behaviorName] ~= nil,
	           string.format("GameObject:unBindBehavior() - behavior %s not binding", behaviorName))
	    assert(not self.behaviorDepends_ or not self.behaviorDepends_[behaviorName],
	           string.format("GameObject:unBindBehavior() - behavior %s depends by other binding", behaviorName))

	    local behavior = self.behaviorObjects_[behaviorName]
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

	    behavior:unBind(self)
	    self.behaviorObjects_[behaviorName] = nil

	    ---强制调用dtor
	    if true then
	       delete(behavior);
	    end
	end

	---解绑所有组件
	function ClassExtend:unBindAllBehavior()
	    if self.behaviorObjects_ == nil then
	        return;
	    end
	    for k,behavior in pairs(self.behaviorObjects_) do
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
	        behavior:unBind(self)
	        ---强制调用dtor
	        if true then
	           delete(behavior);
	        end
	    end
	    self.behaviorObjects_ = {};
	end

	function ClassExtend:resetAllBehaviors()
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

	--[[--
	绑定一个组件的方法
	@param behavior 组件实例
	@string methodName 导出的接口名称
	@param method 绑定的接口
	@param deprecatedOriginMethod  是否废弃之前的函数，只用当前
	@bool callOriginMethodLast 是否最后调用上一个组件函数
	@usage
	object:bindMethod(self, "setHeadImg",   handler(self, self.setHeadImg)); --导出组件setHeadImg接口
	]]
	function ClassExtend:bindMethod(behavior, methodName, method,deprecatedOriginMethod,callOriginMethodLast)
	    local originMethod = self[methodName] --取出之前的方法
	    if not originMethod then
	        self[methodName] = method
	        return
	    end

	    if not self.bindingMethods_ then self.bindingMethods_ = {} end
	    if not self.bindingMethods_[methodName] then self.bindingMethods_[methodName] = {} end

	    local chain = {behavior, originMethod}
	    local newMethod
	    if deprecatedOriginMethod == true then
	        newMethod = function(...)
	            return method(...)
	        end
	    elseif callOriginMethodLast == true then
	        newMethod = function(...)
	            method(...)
	            return chain[2](...);
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

	function ClassExtend:unBindMethod(behavior, methodName)
	    if not self.bindingMethods_ or not self.bindingMethods_[methodName] then
	        self[methodName] = nil
	        return
	    end

	    local methods = self.bindingMethods_[methodName]
	    local count = #methods
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

	---通过路径绑定组件
	--@string behaviorPath 组件路径
	function ClassExtend:bindBehaviorByPath(behaviorPath)
	    if not self.behaviorObjects_ then self.behaviorObjects_ = {} end
	    if self.behaviorObjects_[behaviorPath] then return end

	    local behavior = BYKit.BehaviorFactory.createBehaviorByPath(behaviorPath)
	    for i, dependBehaviorName in pairs(behavior:getDepends()) do
	        self:bindBehavior(dependBehaviorName)

	        if not self.behaviorDepends_ then
	            self.behaviorDepends_ = {}
	        end
	        if not self.behaviorDepends_[dependBehaviorName] then
	            self.behaviorDepends_[dependBehaviorName] = {}
	        end
	        table.insert(self.behaviorDepends_[dependBehaviorName], behaviorPath)
	    end

	    behavior:bind(self)
	    self.behaviorObjects_[behaviorPath] = behavior
	    self:resetAllBehaviors()
	end

	function ClassExtend:unBindBehaviorByPath(behaviorPath)
		assert(self.behaviorObjects_ and self.behaviorObjects_[behaviorPath] ~= nil,
	           string.format("GameObject:unBindBehavior() - behavior %s not binding", behaviorPath))
	    assert(not self.behaviorDepends_ or not self.behaviorDepends_[behaviorPath],
	           string.format("GameObject:unBindBehavior() - behavior %s depends by other binding", behaviorPath))

	    local behavior = self.behaviorObjects_[behaviorPath]
	    for i, dependBehaviorName in pairs(behavior:getDepends()) do
	        for j, name in ipairs(self.behaviorDepends_[dependBehaviorName]) do
	            if name == behaviorPath then
	                table.remove(self.behaviorDepends_[dependBehaviorName], j)
	                if #self.behaviorDepends_[dependBehaviorName] < 1 then
	                    self.behaviorDepends_[dependBehaviorName] = nil
	                end
	                break
	            end
	        end
	    end

	    behavior:unBind(self)
	    self.behaviorObjects_[behaviorPath] = nil

	    ---强制调用dtor
	    if true then
	       delete(behavior);
	    end
	end
end;


return BehaviorEx;