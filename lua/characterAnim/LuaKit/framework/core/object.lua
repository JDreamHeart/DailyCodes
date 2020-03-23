--[[--ldoc desc
@module object
@author YuchengMo

Date   2018-04-25 15:13:29
Last Modified by   YuchengMo
Last Modified time 2018-04-25 15:14:16
]]


--通过判断类型
--返回值顺序 table, boolean, string
--总的有如下N种情况
--1) super, autoConstructSuper, name
--1) super, name, autoConstructSuper
--2) name, super, autoConstructSuper
--3) name, autoConstructSuper,super
local function changeParamsName( p1, p2, p3 )
    if type(p1) == "table" then
        if type(p2) == "boolean" or p2 == nil  then
            return p1,p2,p3;
        end
        if type(p2) == "string" then
            return p1,p3,p2
        end
    end

    if type(p1) == "string" then
        if type(p2) == "table" then
            return p2,p3,p1
        end

        if type(p2) == "boolean" then
            return p3,p2,p1
        end
    end
end


-- Note for the object model here:
--      1.The feature like C++ static members is not support so perfect.
--      What that means is that if u need something like c++ static members,
--      U can access it as a rvalue like C++, but if u need access it
--      as a lvalue u must use [class.member] to access,but not [object.member].
--      2.The function delete cannot release the object, because the gc is based on 
--      reference count in lua.If u want to relase all the object memory, u have to 
--      set the obj to nil to enable lua gc to recover the memory after calling delete.


---------------------Global functon class ---------------------------------------------------
--Parameters:   super               -- The super class
--              autoConstructSuper   -- If it is true, it will call super ctor automatic,when 
--                                      new a class obj. Vice versa.
--Return    :   return an new class type
--Note      :   This function make single inheritance possible.
---------------------------------------------------------------------------------------------

-- if class then
--     oldClass = class
-- end
function class(super, autoConstructSuper,name)
    -- error(1)

    super, autoConstructSuper, name = changeParamsName(super, autoConstructSuper, name)
    -- if super == Node then
    --     error(1)
    -- end
    local classType = {};
    classType.autoConstructSuper = autoConstructSuper or (autoConstructSuper == nil);
    if super then
        classType.super = super;
        local mt = getmetatable(super);
        setmetatable(classType, { __index = super; __newindex = mt and mt.__newindex;});
    else
        classType.setDelegate = function(self,delegate)
            self.m_delegate = delegate;
        end
    end
    if name then
        classType.className__ = name;
    end

    return classType;
end

-- function class(super, autoConstructSuper)
--   local classType = {};
--   classType.autoConstructSuper = autoConstructSuper or (autoConstructSuper == nil);

--   if super then
--     classType.super = super;
--     local mt = getmetatable(super);
--     setmetatable(classType, { __index = super; __newindex = mt and mt.__newindex;});
--   else
--     classType.setDelegate = function(self,delegate)
--       self.m_delegate = delegate;
--     end
--   end

--   return classType;
-- end
---------------------Global functon super ----------------------------------------------
--Parameters:   obj         -- The current class which not contruct completely.
--              ...         -- The super class ctor params.
--Return    :   return an class obj.
--Note      :   This function should be called when newClass = class(super,false).
-----------------------------------------------------------------------------------------

if super == nil then
    function super(obj, ...)
        do 
            local create;
            create =
                function(c, ...)
                    if c.super and c.autoConstructSuper then
                        create(c.super, ...);
                    end
                    if rawget(c,"ctor") then
                        obj.currentSuper = c.super;
                        c.ctor(obj, ...);
                    end
                end

            create(obj.currentSuper, ...);
        end
    end
end


---------------------Global functon new -------------------------------------------------
--Parameters:   classType -- Table(As Class in C++)
--              ...        -- All other parameters requisted in constructor
--Return    :   return an object
--Note      :   This function is defined to simulate C++ new function.
--              First it called the constructor of base class then to be derived class's.
-----------------------------------------------------------------------------------------
if new == nil then

    function new(classType, ...)
        local obj = {};
        local mt = getmetatable(classType);
        setmetatable(obj, { __index = classType; __newindex = mt and mt.__newindex;});
        do
            local create;
            create =
                function(c, ...)
                    if c.super and c.autoConstructSuper then
                        create(c.super, ...);
                    end
                    if rawget(c,"ctor") then
                        obj.currentSuper = c.super;
                        c.ctor(obj, ...);
                    end
                end

            create(classType, ...);
        end
        obj.currentSuper = nil;
        return obj;
    end

end
---------------------Global functon delete ----------------------------------------------
--Parameters:   obj -- the object to be deleted
--Return    :   no return
--Note      :   This function is defined to simulate C++ delete function.
--              First it called the destructor of derived class then to be base class's.
-----------------------------------------------------------------------------------------
if delete == nil then
    function delete(obj)
        do
            local destory =
                function(c)
                    while c do
                        if rawget(c,"dtor") then
                            c.dtor(obj);
                        end
                  
                        c = getmetatable(c);
                        c = c and c.__index;                   
                    end
                end
            destory(obj);
        end
    end
end
---------------------Global functon delete ----------------------------------------------
--Parameters:   class       -- The class type to add property
--              varName     -- The class member name to be get or set
--              propName    -- The name to be added after get or set to organize a function name.
--              createGetter-- if need getter, true,otherwise false.
--              createSetter-- if need setter, true,otherwise false.
--Return    :   no return
--Note      :   This function is going to add get[PropName] / set[PropName] to [class].
-----------------------------------------------------------------------------------------

if property == nil then

function property(class, varName, propName, createGetter, createSetter)
    createGetter = createGetter or (createGetter == nil);
    createSetter = createSetter or (createSetter == nil);
    
    if createGetter then
        class[string.format("get%s",propName)] = function(self)
            return self[varName];
        end
    end
    
    if createSetter then
        class[string.format("set%s",propName)] = function(self,var)
            self[varName] = var;
        end
    end
end


end
---------------------Global functon delete ----------------------------------------------
--Parameters:   obj         -- A class object
--              classType   -- A class
--Return    :   return true, if the obj is a object of the classType or a object of the 
--              classType's derive class. otherwise ,return false;
-----------------------------------------------------------------------------------------

if typeof == nil then
function typeof(obj, classType)
    if type(obj) ~= type(table) or type(classType) ~= type(table) then
        return type(obj) == type(classType);
    end
    
    while obj do
        if obj == classType then
            return true;
        end
        obj = getmetatable(obj) and getmetatable(obj).__index;
    end
    return false;
end
end
---------------------Global functon delete ----------------------------------------------
--Parameters:   obj         -- A class object
--Return    :   return the object's type class.
-----------------------------------------------------------------------------------------

if decltype == nil then
function decltype(obj)
    if type(obj) ~= type(table) or obj.autoConstructSuper == nil then
        --error("Not a class obj");
        return nil;
    end
    
    if rawget(obj,"autoConstructSuper") ~= nil then
        --error("It is a class but not a class obj");
        return nil;
    end
        
    local class = getmetatable(obj) and getmetatable(obj).__index;
    if not class then
        --error("No class reference");
        return nil;
    end
    
    return class;
end

end