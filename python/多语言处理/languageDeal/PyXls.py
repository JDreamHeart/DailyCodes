# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-08-14 11:37:23
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-08-17 19:48:22

import os;
import re;
import xlrd;
import xlwt;
import json;

import sys;
reload(sys)
sys.setdefaultencoding('utf8')

class PyXlsObj(object):
	"""docstring for PyXlsObj"""
	def __init__(self, arg = None):
		super(PyXlsObj, self).__init__()
		self.arg = arg;

	def openWorkbook(self, filePath):
		return xlrd.open_workbook(filePath);

	def getColDataByBook(self, book, sheetName = None, colIdx = None):
		if not sheetName:
			sheet = book.sheet_by_index(0);
		else:
			sheet = book.sheet_by_name(sheetName);
		if colIdx:
			return sheet.col_values(colIdx);
		return sheet;

	def setColDataToXlsByName(self, colData, sheetName, fullFilePath, titleKName = "键值", titleVName = "映射值"):
		book = xlwt.Workbook(encoding='utf-8', style_compression=0);
		sheet = book.add_sheet(sheetName, cell_overwrite_ok=True);
		sheet.write(0, 0, titleKName);
		sheet.write(0, 1, titleVName);
		idx = 1;
		for k,v in colData.items():
			if isinstance(v, dict):
				theIdx = idx;
				if "idx" in v:
					theIdx = v["idx"];
				sheet.write(theIdx, 0, k);
				if "val" in v:
					sheet.write(theIdx, 1, v["val"]);
			else:
				sheet.write(idx, 0, k);
				sheet.write(idx, 1, v);
			idx += 1;
		book.save(fullFilePath);

	def getWriteBook(self, xlsFilePath = ""):
		return xlwt.Workbook(encoding='utf-8', style_compression=0);

	def setExColDataToSheet(self, sheet, colData = None):
		idx = 0;
		if colData:
			for k,v in colData.items():
				sheet.write(idx, 0, k);
				sheet.write(idx, 1, v);
				idx += 1;
		return idx;

	def setTitleNameToSheet(self, sheet, idx, titleKName, titleVName, titleLName):
		idx += 1;
		if titleKName:
			sheet.write(idx, 0, "%_" + titleKName + "_%");
		if titleVName:
			sheet.write(idx, 1, "%_" + titleVName + "_%");
		if titleLName:
			sheet.write(idx, 2, "%_" + titleLName + "_%");
		# 扩展列表中的映射值
		if titleVName and not titleLName:
			col = 2;
			for i in range(3):
				sheet.write(idx, col, "%_" + titleVName + "(tag:" + str(i + 1) + ")_%");
				col += 1;
		return idx;

	def setColDataToXlsByBook(self, colData, sheetName, book, titleKName = "键值", titleVName = "映射值", titleLName = "链接值", exColData = None):
		sheet = book.add_sheet(sheetName, cell_overwrite_ok=True);
		startIdx = self.setExColDataToSheet(sheet, colData = exColData);
		startIdx = self.setTitleNameToSheet(sheet, startIdx, titleKName, titleVName, titleLName);
		idx = startIdx + 1;
		for k,v in colData.items():
			theIdx = idx;
			if isinstance(v, dict):
				if "idx" in v:
					theIdx = v["idx"] + startIdx;
				sheet.write(theIdx, 0, k);
				if "val" in v:
					sheet.write(theIdx, 1, v["val"]);
				if titleLName:
					if "linkList" in v:
						linkIdx = 2;
						for link in v["linkList"]:
							sheet.write(theIdx, linkIdx, link);
			else:
				if k == "_stringTotalCount_":
					theIdx = v + 1;
					continue; # 不保存统计值
				sheet.write(theIdx, 0, k);
				sheet.write(theIdx, 1, v);
			idx += 1;

	def saveBook(self, book, fullFilePath):
		book.save(fullFilePath);

	def changeText(self, text, isReverse = None):
		if isReverse:
			newText = text.replace("\"%_%", "", len(text));
			return newText.replace("%_%\"", "", len(newText));
		else:
			return "%_%[\"" + text + "\"]%_%";

	def changeXlsToJson(self, xlsFilePath):
		data = {};
		book = self.openWorkbook(xlsFilePath);
		sheetNames = book.sheet_names();
		for sheetName in sheetNames:
			sheet = self.getColDataByBook(book, sheetName = sheetName);
			key = self.changeText(sheetName);
			data[key] = {};
			sheetData = data[key];
			for i in range(sheet.nrows):
				val0 = sheet.cell_value(i,0);
				if re.search(r"^%_.*_%$", val0):
					continue;
				for j in range(sheet.ncols):
					if j == 0:
						continue;
					valj = sheet.cell_value(i,j);
					if valj and valj != "":
						if j - 1 == 0:
							key = self.changeText(val0);
							sheetData[key] = valj;
						else:
							key = self.changeText(val0 + str(j-1));
							print(key)
							sheetData[key] = valj;
					else:
						break;
				pass
		return json.dumps(data, indent= 4, sort_keys=True).decode('unicode_escape');


def dumpToLuaFile(jsonData, luaFilePath):
	content = jsonData.replace("]:", "] =", len(jsonData)); # 替换":"为"="
	content = "local data = " + content + "\nreturn data"; # 添加 lua的定义格式
	with open(luaFilePath,"wb") as f:
		f.write(content);
		f.close();


from xlutils.copy import copy
if __name__ == '__main__':
	PyXls = PyXlsObj();
	# book = PyXls.openWorkbook(os.getcwd() + "\\ChineseSearchResult_89.xls");
	# workbook = copy(book);
	# workbook.add_sheet("sheetName", cell_overwrite_ok=True);
	# # sheet = PyXls.getColDataByBook(book, sheetName = u"aa")
	# PyXls.saveBook(workbook, os.getcwd() + "\\SearchResult_89.xls");

	jsonData = PyXls.changeXlsToJson(os.getcwd() + "\\SearchResult10.xls");
	# 转换json中的特殊文本
	content = PyXls.changeText(jsonData, isReverse = True);
	# 保存数据为lua文件
	dumpToLuaFile(content, os.getcwd() + "\\jsonData.lua");

	# re.search(r"\"%_%", line);		

	# test = u'"%_%["输入占用文本"]%_%": "placeholder",'
	# print(test)
	# print(test.replace("\"%_%", "", len(test)))
