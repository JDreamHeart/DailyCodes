# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-08-13 17:56:48
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-08-17 19:47:29

import os;
import re;
import PyXls;
import PyXlsxWriter;
import sys;
reload(sys)
sys.setdefaultencoding('utf8')

class TargetFileSearcher(object):
	"""docstring for TargetFileSearcher"""
	def __init__(self, srcPath, searchPattern = None):
		super(TargetFileSearcher, self).__init__()
		self.srcPath = srcPath;
		self.searchPattern = searchPattern;
		self.isInComment = False; # 是否在注释中的标记

	def resetSrcPath(self, path):
		self.srcPath = path;

	def resetSearchPattern(self, searchPattern):
		self.searchPattern = searchPattern;

	def getPathDir(self, path = None):
		if path:
			return os.listdir(path);
		return os.listdir(self.srcPath);

	def checkIsLayoutFile(self, fileName):
		if re.search(r".*_layout\.lua", fileName, re.I):
			return True;
		return False;

	def checkIsSearchFile(self, fileName):
		return self.checkIsLayoutFile(fileName);

	def getSearchChineseResultList(self, line):
		retList = [];
		charList = [];
		for char in line.decode('utf-8'):
			if u'\u4e00' <= char <= u'\u9fff':
				charList.append(char);
			else:
				if charList:
					chStr = "".join(charList);
					retList.append(chStr);
					charList = [];
		if charList:
			chStr = "".join(charList);
			retList.append(chStr);
			charList = [];
		return retList;

	def getSearchResultList(self, line):
		if self.searchPattern:
			return re.findall(self.searchPattern, line);
		return self.getSearchChineseResultList(line);

	def addStringDict(self, stringDict, line, pkgStringDictMap = {}):
		checkLine = self.filterString(line);
		resultList = self.getSearchResultList(checkLine);
		for string in resultList:
			stringDict["_stringTotalCount_"] += 1;
			stringDict[string] = {"val" : "", "idx" : stringDict["_stringTotalCount_"]};
			self.toSetPkgStringDict(stringDict, pkgStringDictMap, string);

	def toSetPkgStringDict(self, stringDict, pkgStringDictMap, string, val = ""):
		if hasattr(self, "onSetPkgStringDict"):
			getattr(self, "onSetPkgStringDict")(self, stringDict, pkgStringDictMap, string, val);

	def addStringDictByReadFile(self, stringDict, filePath, pkgStringDictMap = {}):
		self.isInComment = False; # 是否在注释中的标记
		f = open(filePath, "r"); # 返回一个文件对象
		line = f.readline(); # 调用文件的 readline()方法
		while line:
			self.addStringDict(stringDict, line, pkgStringDictMap = pkgStringDictMap);
			line = f.readline();
		f.close();

	def _getChStrDict(self, stringDict, parentPath = None, pkgStringDictMap = {}):
		pathList = self.getPathDir(path = parentPath);
		if not parentPath:
			if self.srcPath:
				parentPath = self.srcPath;
			else:
				parentPath = "";
		for path in pathList:
			fullPath = parentPath + "\\" + path;
			if os.path.isdir(fullPath):
				# 检测是否包
				if self.checkIsPkg(fullPath):
					pkgStringDictMap[fullPath] = {"_stringTotalCount_" : 0};
				self._getChStrDict(stringDict, parentPath = fullPath, pkgStringDictMap = pkgStringDictMap);
				if fullPath in pkgStringDictMap:
					if pkgStringDictMap[fullPath]["_stringTotalCount_"] > 0:
						self.toDealWithPkgStringDict(pkgStringDictMap, fullPath);
					# 删除当前包数据
					del pkgStringDictMap[fullPath];
			else:
				if self.checkIsSearchFile(path):
					self.addStringDictByReadFile(stringDict, fullPath, pkgStringDictMap = pkgStringDictMap);
		pass;

	def getChineseStringDict(self, parentPath = None):
		stringDict = {"_stringTotalCount_" : 0};
		self._getChStrDict(stringDict, parentPath = parentPath);
		return stringDict;

	def checkIsPkg(self, path, isCheckResPkg = False):
		if os.path.exists(path + "/init.lua"):
			if isCheckResPkg:
				isRes = False;
				f = open(path + "/init.lua", "r"); # 返回一个文件对象
				line = f.readline(); # 调用文件的 readline()方法
				while line:
					if string.find(line, "__isRes.*=.*true") and (not string.find(line, "%-%-.*__isRes")):
						isRes = True;
						break;
					line = f.readline();
				f.close();
				return isRes;
			else:
				return True;
		return False;

	def toDealWithPkgStringDict(self, pkgStringDictMap, path):
		if hasattr(self, "onDealWithPkgStringDict"):
			getattr(self, "onDealWithPkgStringDict")(self, pkgStringDictMap, path)

	# 过滤字符串
	def filterString(self, line):
		newLine = self.filterComment(line);
		newLine = self.filterUnShowText(newLine);
		return newLine;

	# 过滤注释内容
	def filterComment(self, line):
		if self.isInComment:
			# 搜索]]
			so = re.search(r".*\]\](.*)", line);
			if so:
				self.isInComment = False; # 结束注释
				return so.group(1);
			return "";
		# 搜索----[[
		so = re.search(r"(.*)--.*--\[\[", line);
		if so:
			return so.group(1);
		# 搜索--[[
		so = re.search(r"(.*)--\[\[", line);
		if so:
			self.isInComment = True;  # 开始注释
			return so.group(1);
		# 搜索--
		so = re.search(r"(.*)--", line);
		if so:
			return so.group(1);
		return line; # 返回默认值

	def filterUnShowText(self, line):
		so = re.search(r"text\s*=\s*\"(.*)\"", line);
		if so:
			return so.group(1);
		so = re.search(r"label\s*=\s*\"(.*)\"", line);
		if so:
			return so.group(1);
		so = re.search(r"placeholder\s*=\s*\"(.*)\"", line);
		if so:
			return so.group(1);
		return "";


"""
	以下为搜索中文字符串，并生成xls文件的逻辑
"""
packageCount = 0;
pyXlsObj = PyXls.PyXlsObj();
# pyXlsObj = PyXlsxWriter.PyXlsxWriter();

def getPackagePath(path, basePath = None):
	if basePath:
		searchBasePath = basePath.replace("\\", r"\\");
		searchObj = re.search(searchBasePath + r"\\?(.*)$", path);
		if searchObj:
			return searchObj.group(1);
	return path.split("\\")[-1];

def getPackageName(path, basePath = None):
	global packageCount;
	packageCount = packageCount + 1;
	packageCountStr = str(packageCount)
	packagePath = getPackagePath(path, basePath = basePath);
	packagePathAllowLen = 28 - len(packageCountStr);
	if len(packagePath) > packagePathAllowLen:
		packagePath = packagePath[-packagePathAllowLen:];
	packagePathList = packagePath.split("\\");
	packageName = packagePathList[-1] + "(" + packageCountStr + ")"; #  + "%" + "_".join(packagePathList[:-1])
	return packageName;

def onSetPkgStringDict(obj, stringDict, pkgStringDictMap, string, val):
	summaryName = "汇总";
	stringVal = stringDict[string];
	linkVal = "$B$" + str(stringVal["idx"] + 1) + "," + summaryName;
	# 保存数据到对应包的数据中
	for key in pkgStringDictMap:
		pkgStringDictMap[key]["_stringTotalCount_"] += 1;
		pkgStringDictMap[key][string] = {"val" : val, "idx" : pkgStringDictMap[key]["_stringTotalCount_"], "linkList" : [linkVal]};

def onDealWithPkgStringDict(obj, pkgStringDictMap, path):
	if pkgStringDictMap[path] and hasattr(obj, "workbook"):
		basePath = None;
		if hasattr(obj, "srcPath"):
			basePath = getattr(obj, "srcPath");
		sheetName = getPackageName(path, basePath = basePath);
		try:
			exColData = {"_packagePath_" : getPackagePath(path, basePath = basePath)};
			pyXlsObj.setColDataToXlsByBook(pkgStringDictMap[path], sheetName, getattr(obj, "workbook"), exColData = exColData, titleLName = None);
		except Exception as e:
			print(e);

# 主函数
def main():

	# 搜索路径
	# searchPath = os.getcwd();
	searchPath = "E:\\BYIDEProjects\\newProject6\\assets\\package";

	# xls文件路径
	xlsFilePath = os.getcwd() + "\\SearchResult11.xls";

	# 初始化目标文件搜索类
	targetFileSearcher = TargetFileSearcher(searchPath);
	#初始化目标文件搜索类相关参数
	targetFileSearcher.onSetPkgStringDict = onSetPkgStringDict;
	targetFileSearcher.onDealWithPkgStringDict = onDealWithPkgStringDict;
	targetFileSearcher.workbook = pyXlsObj.getWriteBook(xlsFilePath);

	# 获取中文字符数据
	stringDict = targetFileSearcher.getChineseStringDict();
	pyXlsObj.setColDataToXlsByBook(stringDict, "汇总", targetFileSearcher.workbook, titleLName = None);

	# 生成xls文件
	pyXlsObj.saveBook(targetFileSearcher.workbook, xlsFilePath);


	# 宏文件路径
	# vbaProjectPath = os.getcwd() + "\\vbaProject.bin";
	# 设置宏【目前设置宏有问题】
	# pyXlsObj.setVbaProjectToXlsByBook(targetFileSearcher.workbook, vbaProjectPath = vbaProjectPath);
	# targetFileSearcher.workbook.set_vba_name("Worksheet_Change");

	# 关闭book
	# targetFileSearcher.workbook.close();


if __name__ == '__main__':
	main();

	# targetFileSearcher = TargetFileSearcher("C:\\BYIDEProjects");
	# print(targetFileSearcher.getPathDir(path = "C:\\BYIDEProjects"))

	# print(os.path.isdir("C:\\BYIDEProjects" + "\\" + "newProject1"))

	# pkgName = getPackageName("C:\\BYIDEProjects" + "\\" + "fisdfihdfjdsfkljadshfakdsfhljkd\\newProject1\\pak", "C:\\BYIDEProjects");
	# print(pkgName)
	# rc = re.compile("C:\\\\BYIDEProjects" + "\\\\?(.*)$")
	# sp = "C:\\BYIDEProjects";
	# newSp = sp.replace("\\", r"\\")
	# print(newSp)
	# so = re.search(newSp + r"\\?(.*)$", "C:\\BYIDEProjects" + "\\" + "newProject1\\pak") # r"C:\\BYIDEProjects\\?(.*)$"
	# if so:
	# 	print(so.group(1))

	# targetFileSearcher.isInComment = False;
	# f = open(os.getcwd() + "\\tf\\tfSub\\tfSub_layout.lua", "r"); # 返回一个文件对象
	# line = f.readline(); # 调用文件的 readline()方法
	# while line:
	# 	checkLine = targetFileSearcher.filterString(line);
	# 	print(checkLine)
	# 	line = f.readline();
	# f.close();

