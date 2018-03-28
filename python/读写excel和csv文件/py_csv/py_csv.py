# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-03-26 23:25:12
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-03-28 15:46:51

import os;
import re;
import csv;

class PyCsvObj(object):
	"""docstring for PyCsvObj"""
	def __init__(self, basePath, xlsFileNames):
		super(PyCsvObj, self).__init__()
		self.basePath = basePath;
		self.xlsFileNames = xlsFileNames;
		self.csvFileDict = {};
		self.initCsvFileDict();
		pass;

	def initCsvFileDict(self):
		for fullFileName in self.xlsFileNames:
			fileName = fullFileName.split(".").pop(0);
			csvfile = file(self.basePath + fullFileName, "rb");
			self.csvFileDict[fileName] = csv.reader(csvfile);

	def setColDataByNameAndColIdx(self, colIdx = 0, otherColIdx = 1, colData = [], otherColData = [], fileName = None, exData = {}):
		if fileName:
			if fileName in self.csvFileDict: # self.csvFileDict.has_key(fileName)
				try:
					for line in self.csvFileDict[fileName]:
						colData.append(line[colIdx]);
						otherColData.append(line[otherColIdx]);
						if "colIdx" in exData:
							exData["colData"].append(line[exData["colIdx"]]);
					pass;
				except Exception:
					pass;
			else:
				print("The file named \"{0}\" is not exist in csvFileDict!".format(fileName));
		else:
			for name,csvReader in self.csvFileDict.items():
				try:
					for line in csvReader:
						colData.append(line[colIdx]);
						otherColData.append(line[otherColIdx]);
					pass;
				except Exception:
					pass;

	def sumColDataByNameAndColIdx(self, colIdx, otherColIdx, isIncludeZero = True, fileName = None, exData = {}):
		colData = [];
		otherColData = [];
		self.setColDataByNameAndColIdx(colIdx, otherColIdx, colData, otherColData, fileName, exData);
		sumColData = {};
		exSumColData = {};
		for k in range(len(colData)):
			if re.match(r"\-?\d+\.?\d*$", otherColData[k]):
				keyStr = str(colData[k]);
				if keyStr in sumColData:
					sumColData[keyStr] += float(otherColData[k]);
				else:
					sumColData[keyStr] = float(otherColData[k]);
					pass;
				if "colIdx" in exData:
					exDataKey = exData["colData"][k];
					if exDataKey in exSumColData:
						exSumColData[exDataKey][keyStr] = 1;
					else:
						exSumColData[exDataKey] = {keyStr : 1};
						pass;
				if sumColData[keyStr] == 0 and isIncludeZero != True:
					del sumColData[keyStr];
					if "colIdx" in exData:
						exDataKey = exData["colData"][k];
						del exSumColData[exDataKey][keyStr];
						pass;
		exData["exSumColData"] = exSumColData;
		return sumColData;

	def getMergeColDataByColDataList(self, colDataList, isIncludeZero = True):
		mergeColData = {};
		for colData in colDataList:
			for k,v in colData.items():
				if k in mergeColData:
					mergeColData[k] += v;
				else:
					mergeColData[k] = v;
				if mergeColData[k] == 0 and isIncludeZero != True:
					del mergeColData[k];
		return mergeColData;

	def setColDataToCsvByName(self, sumColData, titleName, fullFileName, subSumColData = None, subTitle = ""):
		csvfile = file(self.basePath + fullFileName, "wb");
		writer = csv.writer(csvfile);
		writer.writerow([titleName, "sum", subTitle]);
		wData = [];
		for k,v in sumColData.items():
			if subSumColData and (k in subSumColData):
				wData.append((k, v, subSumColData[k]));
			else:
				wData.append((k, v, 0));
				pass;
		self.writeDataToCsv(fullFileName, [titleName, "sum", subTitle], wData);
		pass;

	def setSumColDataToCsvByKeyColData(self, colIdx, otherColIdx, keyColData, fullFileName, isIncludeZero = True, fileName = None, exData = {}):
		sumColData = PyCsv.sumColDataByNameAndColIdx(colIdx, otherColIdx, isIncludeZero = isIncludeZero, fileName = fileName, exData = exData);
		exSumColData = exData["exSumColData"];
		retSumData = [];
		for k,v in keyColData.items():
			for kk,vv in exSumColData[k].items():
				retSumData.append([k, kk, sumColData[kk]]);
				pass;
		self.writeDataToCsv(fullFileName, ["tableID", "paiJuId", "gameCoins"], retSumData);
		pass;

	def writeDataToCsv(self, fullFileName, titleList, retData):
		csvfile = file(self.basePath + fullFileName, "wb");
		writer = csv.writer(csvfile);
		writer.writerow(titleList);
		writer.writerows(retData);
		csvfile.close();
		pass;



if __name__ == "__main__":
	# 要加载的文件名配置
	xlsPaths = ["allSumResult.csv", "player_20180322.csv"]; #,"robot_20180322.csv"

	# 基本路径
	basePath = os.getcwd()+"\\csv\\";
	# 创建对象
	PyCsv = PyCsvObj(basePath, xlsPaths);

	## 根据桌子Id，获取玩家/机器人的输赢数据
	# robotSumColData = PyCsv.sumColDataByNameAndColIdx(17, 5, isIncludeZero = False, fileName = "robot_20180322");
	# PyCsv.setColDataToCsvByName(robotSumColData, "PJId", "robotSumResult.csv");
	# playerSumColData = PyCsv.sumColDataByNameAndColIdx(3, 8, isIncludeZero = False, fileName = "player_20180322");
	# PyCsv.setColDataToCsvByName(playerSumColData, "PJId", "playerSumResult.csv");

	## Merge玩家和机器人的输赢数据
	# allSumColData = PyCsv.getMergeColDataByColDataList([robotSumColData, playerSumColData], isIncludeZero = False);
	# PyCsv.setColDataToCsvByName(allSumColData, "PJId", "allSumResult.csv", subSumColData = playerSumColData, subTitle = "playerSumNum");

	## 根据Merge玩家和机器人后的数据，获取对应的牌局Id的玩家输赢数据
	keyColData = PyCsv.sumColDataByNameAndColIdx(0, 1, isIncludeZero = False, fileName = "allSumResult");
	exData = {
		"colIdx" : 3,
		"colData" : [],
	};
	retSumData = PyCsv.setSumColDataToCsvByKeyColData(4, 8, keyColData, "checkSumColData.csv", isIncludeZero = False, fileName = "player_20180322", exData = exData);