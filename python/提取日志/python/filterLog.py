# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-03-21 11:23:44
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-03-29 19:44:26

# 默认配置
defaultIsRemoveFile = False; # 是否需要删除正在过滤的log文件【注意删除的不是gz文件】
defaultFilterContent = "g_BYF.globals.totalMoneyInfo"; # 需要过滤出来的内容

# 过滤日志文件类
import sys
import os
import re
import linecache

class FilterLogFile:
	def __init__(self, filePath, isRemoveFile):
		self.filePath = filePath;
		self.isRemoveFile = isRemoveFile;
		
	def changeContentToReg(self, content):
		#将普通字符串转换为正则表达式的字符串（貌似使用了r''就不用特意去转换了）
		pass

	def getFilterPath(self):
		pathArr = self.filePath.split("\\");
		filterName = "filter_" + pathArr[-1];

		pathArr[-1] = "filter";
		filterPath = "\\".join(pathArr);
		if not os.path.exists(filterPath):
			os.makedirs(filterPath);
		filterPath += "\\" + filterName;
		return filterPath;

	def filter(self, filterContent = defaultFilterContent):
		# print("\nFile path is: " + self.filePath);
		# print("\nFilter content is: " + filterContent)

		data = '';
		# with open(self.filePath, 'r') as f:
		# 	for line in f.readlines():
		# 		line = line.strip();
		# 		line = line.lstrip();
		# 		if re.search(r''+filterContent, line):
		# 			data += line + "\n";

		for line in linecache.getlines(self.filePath):
			line = line.strip();
			line = line.lstrip();
			if re.search(r''+filterContent, line):
				data += line + "\n";

		if self.isRemoveFile:
			# print("\nRemove file: " + self.filePath);
			os.remove(self.filePath);

		if data != "":
			filterPath = self.getFilterPath(); # 获取过滤后的文件名
			with open(filterPath, 'w+') as f:
				f.writelines(data);
		else:
			print("\nCan not find filterContent from the Path of "+self.filePath);

if __name__ == "__main__":
	# filePath = "test.log"; # 测试用

	filePath = sys.argv[1]; # 将命令行中的参数传入FilterLogFile中
	FilterLogFile = FilterLogFile(filePath, defaultIsRemoveFile);
	FilterLogFile.filter();
