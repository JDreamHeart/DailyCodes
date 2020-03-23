---lua文件系统 主要处理文件操作
--@module LuaFileSystem
--@author myc
--@license myc
--@version 1.0.0
--@copyright boyaa.cy


local LuaFileSystem = {};

local function fix(path)
    if System.getPlatform() == System.PlatformWin32 then
        local fullpath = path;
        fullpath = string.replaceAll(fullpath,"\\","/")
        local pos = string.endsWith(path,"/")
        if not pos then
            fullpath = path .. "/";
        end
        fullpath = string.replaceAll(fullpath,"//","/")
        return fullpath;
    else
        local fullpath = path;
        local pos = string.endsWith(path,"/")
        if not pos then
           fullpath = path .. "/";
        end
        return fullpath;
    end
end

function LuaFileSystem:ctor()
    self.isUnZiping = false; --是否正在解压
end

function LuaFileSystem:mkdir_(parent,subDir)
    local fullpath = "";
    if parent and subDir then
        fullpath = self:appendPath(parent,subDir);
        if os.isexist(fullpath) then
            return fullpath;
        else
            if self:makeFolder(fullpath) == true then
                return fullpath
            end
        end
    end
    return nil;
end


---创建目录 成功返回完整路径 错误返回nil
--@string parent 父路劲
--@param ... 更多参数,可以嵌套
--@usage g_LuaFileSystem:mkdir(System.getStorageOuterRoot(),"updateTV","luaUpdate")
function LuaFileSystem:mkdir(parent,...)
    local args = {...};
    local fullPath = parent;

    if #args > 0 then
    	for i,v in ipairs(args) do
	        local subdir = v;
	        -- dump(v);
	        fullPath = self:mkdir_(fullPath, subdir);
	        if fullPath == nil then
	            return nil;
	        end
    	end
    	return  fullPath;
    else
    	if os.isexist(fullPath) then
            return fullPath;
        else
            if self:makeFolder(fullPath) == true then
                return fullPath
            end
        end
    end

    return nil;
end

function LuaFileSystem:makeFolder(fullPath)
    if System.getPlatform() == System.PlatformWin32 then
        return os.mkdir(fullPath);
    else
        ---Android创建目录的是需要加上读写权限....  
    end
end

---追加路径 尾部会补上/
--@string parent 父路劲
--@param ... 更多参数,可以嵌套
--@usage local path   =  g_LuaFileSystem:appendPath(System.getStorageOuterRoot(),"updateTV","luaUpdate")
function LuaFileSystem:appendPath(parent,...)
	local fullpath = parent;
	local args = {...};
	for i,v in ipairs(args) do
		fullpath = fix(fullpath);
        fullpath = fullpath .. v;
	end
	fullpath = fix(fullpath);
	return fullpath;
end

---文件是否存在
--@string fullPath 全路径
--@return true or false
function LuaFileSystem:isExist(fullPath)
    if fullPath == nil then
        return false;
    end
    return os.isexist(fullPath);
end

---计算文件md5值
--@string fullPath 全路径
--@return md5
function LuaFileSystem:md5File(fullPath)
    if fullPath == nil then
        error("file is nil");
    end
    return md5_file(fullPath);
end

---删除一个目录（win32同步操作,android 异步删除）
--@string fullPath 全路径
function LuaFileSystem:deleteFolder(fullPath)
    if System.getPlatform() == System.PlatformWin32 then
        self:deleteFolderOnWin32(fullPath)
    else
        local NativeCMD = import(g_CommonPath.."native.NativeCMD");
        luaj.callNative(NativeCMD.L2J.DeleteFolder,{dir=fullPath});
    end

end

function LuaFileSystem:deleteFolderOnWin32(fullPath)
    if os.isdir(fullPath) then
        local files = os.lsdirs(fullPath)
        for k,v in pairs(files) do
            self:deleteFolderOnWin32(v);
        end
        local files = os.lsfiles(fullPath)
        for i,v in pairs(files) do
            System.removeFile(v);
        end
        os.rmdir(fullPath);
    end
end

---获取文件名
function LuaFileSystem:getName(path)
    local name = "";
    local temPath = string.replaceAll(path,"\\","/");
    -- if os.isdir(temPath) then
    --     local list = string.split(temPath,"/")
    --     if #list > 1 then
    --         name = list[#list - 1];
    --         return name;
    --     end
    -- else
        local list = string.split(temPath,"/")
        if #list > 0 then
            name = list[#list];
            return name;
        end
    -- end
end

---拷贝文件
--@string srcDir 源路劲
--@string dstDir 目标路径
--@table  filter 过滤指定的文件后缀名
--@param  saveFailList 是否保存失败列表,调用getFailList可以得到
function LuaFileSystem:copyFiles(srcDir,dstDir, filter,saveFailList)
    if saveFailList then
        -- 每次清空
        self.m_failList = {}
    end
    filter = checktable(filter)
    if os.isdir(srcDir) then
        self:mkdir(dstDir)
        local dir = os.lsdirs(srcDir)
        for k,v in pairs(dir) do
            local name = self:getName(v)
            local file = self:appendPath(dstDir,name);
            self:copyFiles(v,file, filter);
        end
        local files = os.lsfiles(srcDir)
        for _,v in pairs(files) do
            local name = self:getName(v)
            local file = dstDir .. name
            local legal = true

            for _,f in ipairs(filter) do
                if string.sub(v, #v - #f + 1, #v) == f then
                    legal = false
                end
            end
            if legal then
                local ret = os.cp(v,file)
                if not ret and self.m_failList then
                    self.m_failList[#self.m_failList +1] = v
                end
            end
        end
    end
end

function LuaFileSystem:getFailList()
    return self.m_failList
end

function LuaFileSystem:readFile( path )
    local file = io.open(path, "r")
    if file then
        local content = file:read("*a")
        io.close(file)
        return content
    end
    return nil
end

---写文件
--@string path 全路径
--@string content 文件内容
--@string mode 模式 覆盖 追加等
function LuaFileSystem:writeFile(path, content, mode)
    mode = mode or "w+"
    local file = io.open(path, mode)
    if file then
        if file:write(content) == nil then
            return false 
        end
        io.close(file)
        return true
    else
        return false
    end
end

---移动文件
--@string srcFile 源文件
--@string dstFile 目标文件
--@boolean cover 如果源文件存在是否覆盖
--@return 是否移动成功
function LuaFileSystem:moveFile(srcFile, dstFile, cover)
    if os.isexist(dstFile) then
        if cover then
            -- 删除目标文件
            System.removeFile(dstFile);
        else
            return false
        end
    end
    os.rename(srcFile, dstFile)
    return true
end
return LuaFileSystem;
