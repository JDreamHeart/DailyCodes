# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-11-27 13:07:09
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-12-07 15:20:42

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
			"keyDepth" : 0, # 生成配置key值的连接字符
			"joinKeysStr" : "_", # 生成配置key值的连接字符
			"isMergeSameToTable" : False, # 是否合并相同的语音到table中
			"isSaveFilePath" : False, # 是否保存文件路径【包括文件后缀名】
			"joinValuesStr" : "/", # 生成配置value值的连接字符

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
		elif isinstance(value, str):
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
		self.dumpConfigToFile(targetPath, config);
		return config;


# 导出配置
def ExportConfig(cwd = os.getcwd()):
	print("=== Extract start ===");

	ExtMode = -1; # 导出模式：0->加载audio的配置；1->播放audio的配置

	# 查找及导出路径
	path = cwd.replace("\\", "/");
	path += "/audio/res/lndalianmj/mp3/effects";

	# 导出配置类实例化
	ConfigExt1 = ConfigExtraction(params = {
		"ExportFileName": "loadEffectsConfig",
		"suffixNames" : ["mp3", "ogg"],
		"isMergeSameToTable": False,
		"isSaveFilePath": True,
		# "keyDepth" : 1,
	});
	ConfigExt2 = ConfigExtraction(params = {
		"ExportFileName": "playEffectsConfig",
		"suffixNames" : ["mp3", "ogg"],
		"isMergeSameToTable": True,
		"isSaveFilePath": False,
		"joinValuesStr" : "_",
		"keyDepth" : 1,
	});
	# 根据导出模式导出配置
	if ExtMode == 0:
		ConfigExt1.extract(path, path);
	elif ExtMode == 1:
		ConfigExt2.extract(path, path);
	else:
		ConfigExt1.extract(path, path);
		ConfigExt2.extract(path, path);
	print("Extract success!");
	print("The path of extraction is:", path);


# 重命名文件
def RenameFile(callback, relativePath, cwd = os.getcwd()):
	print("=== Rename start ===")
	checkPath = cwd.replace("\\", "/");
	print(cwd)
	checkPath += relativePath;
	files = os.listdir(checkPath);
	for file in files:
		if callable(callback):
			callback(checkPath + "/", file);
	print("=== Rename end ===");


if __name__ == '__main__':

	# # 重命名麻将配音文件
	# # 重命名麻将子文件
	# def callback(dirPath, fileName):
	# 	keyList = fileName.split("_");
	# 	keyList.pop(0);
	# 	newFileName = "_".join(keyList);
	# 	os.rename(dirPath + fileName, dirPath + newFileName);
	# RenameFile(callback, "/audio/res/lndalianmj/mp3/effects/man/majiangzi");
	# 重命名effects/mahjong为effects/common
	os.rename(os.getcwd() + "/audio/res/lndalianmj/mp3/effects/mahjong", os.getcwd() + "/audio/res/lndalianmj/mp3/effects/common");


	# # 导出配置
	# ExportConfig();
