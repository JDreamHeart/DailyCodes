

local BehaviorBase = import(".BehaviorBase");

---组件工厂类
local behaviorsClass = {
    
}

local BehaviorFactory = {}


function BehaviorFactory.createBehavior(behaviorName,params)
    local classObj = behaviorsClass[behaviorName] 
    assert(classObj ~= nil, string.format("BehaviorFactory.createBehavior() - Invalid behavior name \"%s\"", tostring(behaviorName)))
    if typeof(classObj,BehaviorBase) then
        return new(classObj,params)
    elseif type(classObj) == "table" and classObj.pkgrequire and classObj.path then
        classObj = classObj.pkgrequire(classObj.path);
        return new(classObj)
    else
        classObj = require(classObj);
        return new(classObj)
    end
    
end

function BehaviorFactory.createBehaviorByPath(behaviorPath)
    if not behaviorsClass[behaviorPath] then
        local cur = System:getStorageAppRoot();
        local rela;
        if string.contains(behaviorPath,'\\Resource\\') then
            local arr = string.split(behaviorPath,'\\Resource\\');
            rela = string.replace(arr[#arr],'\\','/')
        else
            local arr = string.split(behaviorPath,'/Resource/');
            rela = arr[#arr];
        end
        if IDECache then
            local real_path = IDECache.curProject.projectPath.."/Resource/"..rela
            behaviorsClass[behaviorPath] = loadfile(real_path)();
        else
            local real_path = cur..rela;
            behaviorsClass[behaviorPath] = loadfile(real_path)();
        end
    end
    local classObj = behaviorsClass[behaviorPath];
    assert(classObj ~= nil, string.format("BehaviorFactory.createBehavior() - Invalid behavior path \"%s\"", tostring(behaviorPath)));
    return new(classObj);
end

function BehaviorFactory.combineBehaviorsClass(newBehaviorsClass)
    for k, v in pairs(newBehaviorsClass) do
        assert(behaviorsClass[k] == nil, string.format("BehaviorFactory.combineBehaviorsClass() - Exists behavior name \"%s\"", tostring(k)))
        behaviorsClass[k] = v   
    end
end

function BehaviorFactory.merge(newBehaviorsClass)
    for k, v in pairs(newBehaviorsClass) do
        behaviorsClass[k] = v   
    end
end


function BehaviorFactory.removeBehaviorsClass(removeBehaviorsClass)
    for k, v in pairs(removeBehaviorsClass) do
        behaviorsClass[k] = nil;      
    end
end

return BehaviorFactory