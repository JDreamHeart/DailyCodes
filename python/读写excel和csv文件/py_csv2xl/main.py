# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-07-10 11:16:06
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-07-10 15:17:34
import os;
import xlwt;
import csv;
import json;

# 获取结果数据
def getResultData(filePath, keys):
	titles, data = [], [];
	if not os.path.exists(filePath):
		return titles, data;
	with open(filePath, "r") as f:
		csvReader, maxULogCnt = csv.reader(f), 0;
		for line in csvReader:
			try:
				uLogs = json.loads(line[4]);
				# 更新最大uLog数量
				if len(uLogs) > maxULogCnt:
					maxULogCnt = len(uLogs);
				# 添加数据
				data.append([]);
				for uLog in uLogs:
					for k in keys:
						data[-1].append(getValByUlog(uLog, k));
			except Exception as e:
				print(e, line);
		# 更新标题
		for i in range(maxULogCnt):
			titles.extend(keys);
	return titles, data;

# 根据uLog及key获取对应值
def getValByUlog(uLog, key):
	if key not in uLog:
		return "";
	if "$numberLong" in uLog[key]:
		if key == "result":
			return getResultByULog(uLog);
		return uLog[key]["$numberLong"];
	return uLog[key];

# 根据uLog获取输赢类型
def getResultByULog(uLog):
	ret = uLog["result"]["$numberLong"];
	if ret == "1":
		return "赢";
	elif ret == "2":
		return "输";
	elif ret == "3":
		return "平局";
	return "未知类型（"+ret+"）";

# 保存为xl
def saveAsXl(titles, data, sheetName, filePath):
	book = xlwt.Workbook(encoding='utf-8', style_compression=0);
	sheet = book.add_sheet(sheetName, cell_overwrite_ok=True);
	# 设置标题
	for i,title in enumerate(titles):
		sheet.write(0, i, title);
	# 保存数据值
	for i,item in enumerate(data, start=1):
		for j,val in enumerate(item):
			sheet.write(i, j, val);
	book.save(filePath);


if __name__ == '__main__':
	# 读取文件路径，及输出文件路径
	srcPath = "mahjong.cvs";
	tgtPath = "result.xlsx";

	# 读取并输出数据
	print("正在查找数据...");
	titles, data = getResultData(srcPath, ["result", "score", ""]);
	print("查找数据成功，目录为[{}]。".format(srcPath));
	print("正在输出xl文件...");
	saveAsXl(titles, data, "查找结果", "result.xls");
	print("输出xl文件成功，目录为[{}]。".format(tgtPath));