# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-11-27 13:07:09
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-11-27 18:51:03

import os;
import re;

class ConfigExtraction(object):
	"""docstring for ConfigExtraction"""
	def __init__(self, suffixNames = None):
		super(ConfigExtraction, self).__init__()
		self.m_suffixNames = suffixNames;
		
	def getFileList(self, path, fileList = [], pathList = [], func = None):
		files = os.listdir(path);
		for file in files:
			filePath = path + "/" + file;
			if os.path.isdir(filePath):
				pathList.append(file);
				self.getFileList(filePath, fileList = fileList, pathList = pathList, func  =func);
			elif not self.m_suffixNames or self.getFileSuffixName(file) in self.m_suffixNames:
				fileList.append(filePath);
				if callable(func):
					func(filePath, pathList);
		return fileList;

	def getFileName(self, path):
		PathList = path.split("/");
		return PathList[-1].split(".")[0];

	def getFileSuffixName(self, path):
		PathList = path.split(".");
		return PathList[-1];

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
			tmpConfig = config;
			for v in pathList:
				if v not in tmpConfig:
					tmpConfig[v] = {};
				tmpConfig = tmpConfig[v];
			# 保存配置
			fileName = self.getFileName(filePath);
			res = re.match("^(\w+)_(\d+)$", fileName);
			if res:
				name = self.filterFileName(res.group(1));
				self.addConfig(tmpConfig, name, "/".join(pathList) + "/" + fileName);
			else:
				self.addConfig(tmpConfig, fileName, "/".join(pathList) + "/" + fileName);
		self.getFileList(path, func = checkFilePath);
		return config;

	def dumpConfigToFile(self, targetPath, config = {}):
		content = """-- 音效配置
local AudioConfig = {0};

return AudioConfig;""";
		content = content.format(self.getDumpContent(config));
		with open(targetPath + "/AudioConfig.lua", "w") as f:
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
				strList.append("{0}[\"{1}\"] = {2}".format(contentIndentation, k, valStr));
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

if __name__ == '__main__':
	print("=== Extract start ===");

	# 查找及导出路径
	path = os.getcwd().replace("\\", "/");
	path += "/audio/res/lndalianmj";

	ConfigExt = ConfigExtraction(["mp3", "ogg"]); # 只获取MP3或OGG格式的文件
	config = ConfigExt.extract(path, path); # 导出配置
	# print(ConfigExt.getDumpContent(config))

	print("Extract success!");
	print("The path of extraction is:", path);
