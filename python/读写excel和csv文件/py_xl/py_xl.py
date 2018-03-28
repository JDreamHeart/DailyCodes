# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-03-26 23:25:12
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-03-28 09:29:42

import os;
import xlrd;
import xlwt;

class PyXlsObj(object):
	"""docstring for PyXlsObj"""
	def __init__(self, basePath, xlsFileNames):
		super(PyXlsObj, self).__init__()
		self.basePath = basePath;
		self.xlsFileNames = xlsFileNames;
		self.xlsFileDict = {};
		self.initXlsFileDict();
		pass;

	def initXlsFileDict(self):
		for fullFileName in self.xlsFileNames:
			fileName = fullFileName.split(".").pop(0);
			self.xlsFileDict[fileName] = xlrd.open_workbook(self.basePath + fullFileName);

	def getColDataByNameAndColIdx(self, sheetName = None, colIdx = 0, fileName = None):
		if fileName:
			if fileName in self.xlsFileDict: # self.xlsFileDict.has_key(fileName)
				if not sheetName:
					sheet = self.xlsFileDict[fileName].sheet_by_index(0);
				else:
					sheet = self.xlsFileDict[fileName].sheet_by_name(sheetName);
				return sheet.col_values(colIdx);
			else:
				print("The file named \"{0}\" is not exist in xlsFileDict!".format(fileName));
		else:
			for name,book in self.xlsFileDict.items():
				if not sheetName:
					sheet = book.sheet_by_index(0);
				else:
					sheet = book.sheet_by_name(sheetName);
				return sheet.col_values(colIdx);

	def sumColDataByNameAndColIdx(self, sheetName, colIdx, otherColIdx, isIncludeZero = True, theSumColData = None, fileName = None):
		colData = self.getColDataByNameAndColIdx(sheetName, colIdx, fileName);
		otherColData = self.getColDataByNameAndColIdx(sheetName, otherColIdx, fileName);
		sumColData = theSumColData or {};
		for k in range(len(colData)):
			if not isinstance(otherColData[k], str):
				if str(colData[k]) in sumColData:
					sumColData[str(colData[k])] += otherColData[k];
				else:
					sumColData[str(colData[k])] = otherColData[k];
				if sumColData[str(colData[k])] == 0 and isIncludeZero != True:
					del sumColData[str(colData[k])];
		return sumColData;

	def setColDataToXlsByName(self, sumColData, titleName, sheetName, fullFileName):
		book = xlwt.Workbook(encoding='utf-8', style_compression=0);
		sheet = book.add_sheet(sheetName, cell_overwrite_ok=True);
		sheet.write(0, 0, titleName);
		sheet.write(0, 1, "sum");
		idx = 1;
		for k,v in sumColData.items():
			sheet.write(idx, 0, k);
			sheet.write(idx, 1, v);
			idx += 1;
		book.save(self.basePath + fullFileName);
		pass;

if __name__ == "__main__":
	basePath = os.getcwd()+"\\xls\\";
	xlsPaths = ["robot_20180322.csv", "player_20180322.csv"];
	PyXls = PyXlsObj(basePath, xlsPaths);
	robotSumColData = PyXls.sumColDataByNameAndColIdx("robot_20180322", 3, 4, isIncludeZero = False, theSumColData = None, fileName = "player_20180322");
	PyXls.setColDataToXlsByName(allSumColData, "PJId", "sumResult", "playerSumResult.csv");
	# print(sumColData);
	# sumColData1 = PyXls.sumColDataByNameAndColIdx("testSheet1", 3, 4, isIncludeZero = False);
	# print(sumColData1);
	allSumColData = PyXls.sumColDataByNameAndColIdx("testSheet1", 3, 4, isIncludeZero = False, theSumColData = robotSumColData);
	# print(allSumColData);
	PyXls.setColDataToXlsByName(allSumColData, "PJId", "sumResult", "sumResult.xlsx");