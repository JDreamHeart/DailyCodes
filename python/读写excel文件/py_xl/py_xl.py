# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-03-26 23:25:12
# @Last Modified by:   Administrator
# @Last Modified time: 2018-03-27 00:10:58

import os;
import xlrd;
import xlwt;

class PyXlsObj(object):
	"""docstring for PyXlsObj"""
	def __init__(self, xlsFilePaths):
		super(PyXlsObj, self).__init__()
		self.xlsFilePaths = xlsFilePaths;
		self.xlsFileDict = {};
		self.initXlsFileDict();
		pass;

	def initXlsFileDicet(self):
		for k in self.xlsFilePaths:
			filePath = self.xlsFilePaths[k];
			fileName = filePath.split("\\").pop().split(".").pop(0);
			self.xlsFileDict[fileName] = xlrd.open_workbook(filePath);

	def getColDataByNameAndColIdx(self, sheetName = None, colIdx = 0, fileName = None):
		if fileName:
			if self.xlsFileDict.has_key(fileName):
				if not sheetName:
					sheet = book.sheet_by_index(0);
				else:
					sheet = self.xlsFileDict[fileName].sheet_by_name(sheetName);
				return sheet and sheet.col_values(colIdx);
			else:
				print("The file named \"{0}\" is not exist in xlsFileDict!".format(fileName));
		else:
			for name,book in self.xlsFileDict.items():
				sheet = self.xlsFileDict[fileName].sheet_by_name(sheetName);
				return sheet.col_values(colIdx);

	def sumColDataByNameAndColIdx(self, sheetName, colIdx, otherColIdx, isIncludeZero = True, fileName = None):
		colData = self.getColDataByNameAndColIdx(sheetName, colIdx, fileName);
		otherColData = self.getColDataByNameAndColIdx(sheetName, otherColIdx, fileName);
		sumColData = {};
		for k in colData:
			if not isinstance(colData[k], str):
				if sumColData.has_key(str(colData[k])):
					sumColData[str(colData[k])] += otherColData[k];
				else:
					sumColData[str(colData[k])] = otherColData[k];
				if sumColData[str(colData[k])] == 0 and isIncludeZero != True:
					del sumColData[str(colData[k])];
		return sumColData;

	def setColDataToXlsByName(self, sumColData, titleName, sheetName, fileName):
		book = xlwt.Workbook(encoding='utf-8', style_compression=0);
		sheet = book.add_sheet(sheetName.decode('utf-8'), cell_overwrite_ok=True);
		sheet.write(0, 0, titleName.decode('utf-8'));
		sheet.write(0, 1, "sum");
		idx = 1;
		for k in sumColData:
			sheet.write(idx, 0, k);
			sheet.write(idx, 1, sumColData[k]);
		book.save(os.getcwd()+fileName);
		pass;

if __name__ == "__main__":
	xlsPaths = [];
	PyXls = PyXlsObj(xlsPaths);
	sumColData = PyXls.sumColDataByNameAndColIdx(sheetName = None, 7, 8, isIncludeZero = False);
	self.setColDataToXlsByName(sumColData, "pjId", "sumResult", "sumResult");