# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-11-27 13:07:09
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-06-20 15:18:10

import os;
import re;
import copy;

class ConfigExtraction(object):
	"""docstring for ConfigExtraction"""
	def __init__(self, params = {}):
		super(ConfigExtraction, self).__init__();
		self.initParams(params);

	def initParams(self, params):
		self.m_params_ = {
			"ExportFileName" : "AudioConfig", # 导出的文件名
			"suffixNames" : None, # [] 查找文件的后缀名列表
			"keyDepth" : 0, # 生成配置key值的深度
			"joinKeysStr" : "_", # 生成配置key值的连接字符
			"isMergeSameToTable" : False, # 是否合并相同的语音到table中
			"isSaveFilePath" : False, # 是否保存文件路径【包括文件后缀名】
			"joinValuesStr" : "/", # 生成配置value值的连接字符
			"rootPath" : "", # 相对于包加载的根路径
			"isOutputStr" : True, # 是否输出单个config的value为字符串
			"cfgKeyCallback" : None, # 每生成一个config的key时的回调函数
			"cfgValCallback" : None, # 每生成一个config的value时的回调函数
			"extractCallback" : None, # 导出配置后且输出文件前的回调函数
		};
		for k,v in params.items():
			self.m_params_[k] = v;
		
	def getFileList(self, path, fileList = [], pathList = [], func = None):
		files = os.listdir(path);
		for file in files:
			filePath = path + "/" + file;
			if os.path.isdir(filePath):
				pathList.append(file);
				self.getFileList(filePath, fileList = fileList, pathList = pathList, func  =func);
				pathList.pop();
			elif not self.m_params_["suffixNames"] or self.getFileSuffixName(file) in self.m_params_["suffixNames"]:
				fileList.append(filePath);
				if callable(func):
					func(filePath, pathList);
		return fileList;

	def getFileName(self, path, isIncludesuffix = False):
		PathList = path.split("/");
		if not isIncludesuffix:
			return PathList[-1].split(".")[0];
		return PathList[-1];

	def getFileSuffixName(self, path):
		PathList = path.split(".");
		return PathList[-1];

	def getTmpConfigByPathList(self, config, pathList):
		tmpConfig = config;
		keyDepth = self.m_params_["keyDepth"];
		curDepth = 0;
		for v in pathList:
			curDepth += 1;
			if keyDepth < 0 or keyDepth >= curDepth:
				if v not in tmpConfig:
					tmpConfig[v] = {};
				tmpConfig = tmpConfig[v];
			else:
				break;
		return tmpConfig;

	def addConfig(self, config, key, val):
		# 配置的key值
		if key not in config:
			config[key] = [];
		# 配置的value值
		if val not in config[key]:
			config[key].append(val);

	def getConfigByPath(self, path):
		config = {};
		def checkFilePath(filePath, pathList):
			# 获取对应keyList的配置数据
			tmpConfig = self.getTmpConfigByPathList(config, pathList);
			# 保存配置
			fileName = self.getFileName(filePath);
			# 添加配置
			value = self.m_params_["joinValuesStr"].join(pathList) + self.m_params_["joinValuesStr"]; # 保存到配置文件中的value值
			if self.m_params_["isSaveFilePath"]:
				value += self.getFileName(filePath, True);
			else:
				value += fileName;
			if self.m_params_["cfgValCallback"]:
				value = self.m_params_["cfgValCallback"](self.m_params_["rootPath"], value, self.m_params_["joinValuesStr"]);
			if self.m_params_["isMergeSameToTable"]:
				res = re.match("^(\w+)_(\d+)$", fileName);
				if res:
					name = self.filterFileName(res.group(1));
					key = self.getConfigKey(pathList, name);
					self.addConfig(tmpConfig, key, value);
				else:
					key = self.getConfigKey(pathList, fileName);
					self.addConfig(tmpConfig, key, value);
			else:
				key = self.getConfigKey(pathList, fileName);
				tmpConfig[key] = value;
		self.getFileList(path, func = checkFilePath);
		return config;

	def getConfigKey(self, pathList, fileName):
		if self.m_params_["joinKeysStr"]:
			newPathList = copy.deepcopy(pathList);
			if self.m_params_["keyDepth"] > 0:
				for i in range(self.m_params_["keyDepth"]):
					if len(newPathList) == 0:
						break;
					newPathList.pop(0);
			if callable(self.m_params_["cfgKeyCallback"]):
				return self.m_params_["cfgKeyCallback"](newPathList, fileName, self.m_params_["joinKeysStr"]);
			if len(newPathList) == 0:
				return fileName;
			return self.m_params_["joinKeysStr"].join(newPathList) + self.m_params_["joinKeysStr"] + fileName;
		return fileName

	def dumpConfigToFile(self, targetPath, config = {}):
		content = "-- 音效配置\nlocal " + self.m_params_["ExportFileName"] + " = {0};\n\nreturn " + self.m_params_["ExportFileName"] + ";";
		configContent = self.getDumpContent(config);
		# 去掉最后一个","
		if configContent[-1] == ",":
			configContent = configContent[:-1]
		content = content.format(configContent);
		with open(targetPath + "/" + self.m_params_["ExportFileName"] + ".lua", "w") as f:
			f.write(content);
			f.close();

	def getIndentation(self, indent = 0):
		indentation = "";
		for i in range(indent):
			indentation += "\t";
		return indentation;

	def getDumpContent(self, value = {}, index = 0):
		# 获取缩进
		indentation = self.getIndentation(index);
		contentIndentation = indentation;
		strList = [];
		# 对于表结构，添加{字符
		if isinstance(value, (list, tuple, dict)):
			contentIndentation = self.getIndentation(index + 1);
			strList.append("{");
		# 获取内容字符串列表
		if isinstance(value, dict):
			for k in sorted(value.keys()):
				valStr = self.getDumpContent(value[k], index + 1);
				strList.append("{0}{1} = {2}".format(contentIndentation, k, valStr));
		elif isinstance(value, (list, tuple)):
			for v in value:
				strList.append(self.getDumpContent(v, index + 1));
		elif isinstance(value, str) and self.m_params_["isOutputStr"]:
			strList.append("{0}{1},".format(contentIndentation, "\"{}\"".format(value)));
		else:
			strList.append("{0}{1},".format(contentIndentation, str(value)));
		# 对于表结构，添加}字符
		if isinstance(value, (list, tuple, dict)):
			strList.append("{0}}},".format(indentation));
		return "\n".join(strList);

	def filterFileName(self, fileName):
		nameArr = fileName.split("_");
		if nameArr[0] == "m" or nameArr[0] == "w":
			nameArr.pop(0);
			return "_".join(nameArr);
		return fileName;

	def extract(self, path, targetPath):
		config = self.getConfigByPath(path);
		if callable(self.m_params_["extractCallback"]):
			self.m_params_["extractCallback"](config);
		self.dumpConfigToFile(targetPath, config);
		return config;


# 重命名文件
def RenameFile(callback, relativePathList, cwd = os.getcwd()):
	print("=== Rename start ===")
	path = cwd.replace("\\", "/");
	for relativePath in relativePathList:
		checkPath = path + relativePath;
		files = os.listdir(checkPath);
		for file in files:
			if callable(callback):
				callback(checkPath + "/", file);
	print("=== Rename end ===");

# 配置key值的回调
def cfgKeyCallback(pathList, fileName, joinKeysStr):
	newPList = [];
	for k in ["common", "man", "woman"]:
		if k not in pathList:
			continue;
		newPList = pathList[pathList.index(k)+1:];
		break;
	newPList.append(fileName);
	key = joinKeysStr.join(newPList);
	if len(pathList) > 0 and pathList[0] == "music":
		key = "music_" + key;
	return key

# 配置value值的回调
def cfgValCallback(rootPath, value, joinValuesStr):
	value = re.sub(".*music/", "", value);
	value = re.sub(".*effect/", "", value);
	value = re.sub(".*woman/", "?/", value);
	value = re.sub(".*man/", "?/", value);
	return value;

# 导出配置后且输出文件前的回调
def extractCallback(cfg):
	for k,v in cfg.items():
		if isinstance(v, list) and len(v) == 1:
			cfg[k] = v[0]
	pass;

# 导出配置
def ExportConfig(configPath = os.getcwd(), targetPath = os.getcwd(), pkgRelativePath = ""):
	print("=== Extract start ===");

	# 查找及导出路径
	configPath = configPath.replace("\\", "/");
	targetPath = targetPath.replace("\\", "/");
	pkgRelativePath = pkgRelativePath.replace("\\", "/");
	if len(pkgRelativePath) > 0 and pkgRelativePath[-1] != "/":
		pkgRelativePath += "/"

	# 导出配置类实例化
	ConfigExt1 = ConfigExtraction(params = {
		"suffixNames" : ["ogg"],
		"isMergeSameToTable": True,
		"keyDepth" : 0,
		"rootPath" : pkgRelativePath,
		"cfgKeyCallback" : cfgKeyCallback,
		"cfgValCallback" : cfgValCallback,
		"extractCallback" : extractCallback,
	});
	# 根据导出模式导出配置
	ConfigExt1.extract(configPath, targetPath);

	print("Extract success!");
	print("The path of extraction is:", targetPath);


if __name__ == '__main__':

	CURRENT_PATH = os.getcwd()

	# 导出配置的路径【使用绝对路径】
	targetPath =  os.path.abspath(os.path.join(CURRENT_PATH, "../sounds")); # 导出路径
	exPath = "res" # 保存音效的目录【相对于导出路径】

	# 合成路径
	soundsPath = targetPath
	if exPath:
		soundsPath += "/" + exPath


	# ========== 麻将音效文件特殊处理 · 开始 ==========

	# 重命名配音文件夹
	print("=== Rename audio folder start ===")
	# 重命名effects为effect
	if os.path.exists(soundsPath + "/effects"):
		os.rename(soundsPath + "/effects", soundsPath + "/effect");
	# 重命名effect/mahjong为effect/common
	if os.path.exists(soundsPath + "/effect/mahjong"):
		os.rename(soundsPath + "/effect/mahjong", soundsPath + "/effect/common");
	# 重命名effect/man/majiangzi为effect/man/card
	if os.path.exists(soundsPath + "/effect/man/majiangzi"):
		os.rename(soundsPath + "/effect/man/majiangzi", soundsPath + "/effect/man/card");
	# 重命名effect/woman/majiangzi为effect/woman/card
	if os.path.exists(soundsPath + "/effect/woman/majiangzi"):
		os.rename(soundsPath + "/effect/woman/majiangzi", soundsPath + "/effect/woman/card");
	print("=== Rename audio folder end ===")

	# 重命名聊天文件
	def callback(dirPath, fileName):
		newFileName = fileName.replace("chat", "");
		os.rename(dirPath + fileName, dirPath + newFileName);
	# 调用函数
	RenameFile(callback, ["/effect/man/chat", "/effect/woman/chat"], cwd = soundsPath);

	# 重命名麻将子文件
	def callback(dirPath, fileName):
		keyList = fileName.split("_");
		if keyList[0] == "m" or keyList[0] == "w":
			keyList.pop(0);
			newFileName = "_".join(keyList);
			os.rename(dirPath + fileName, dirPath + newFileName);
	# 调用函数
	RenameFile(callback, ["/effect/man/card", "/effect/woman/card"], cwd = soundsPath);

	# ========== 麻将音效文件特殊处理 · 结束 ==========
	
	
	# 导出配置
	ExportConfig(configPath = soundsPath, targetPath = targetPath, pkgRelativePath = exPath);

