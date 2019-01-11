# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-25 10:31:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-11 14:08:50
import wx;
import random, math;
from enum import Enum, unique;

@unique
class Direction(Enum):
	LEFT = 0;
	TOP = 1;
	RIGHT = 2;
	BOTTOM = 3;

def getMovingItemMtList(startPos, key = "I"):
	if key == "I":
		return [
			(startPos[0]-3, startPos[1]),
			(startPos[0]-2, startPos[1]),
			(startPos[0]-1, startPos[1]),
			(startPos[0], startPos[1])
		];
	elif key == "J":
		return [
			(startPos[0]-2, startPos[1]),
			(startPos[0]-1, startPos[1]),
			(startPos[0], startPos[1]),
			(startPos[0], startPos[1]-1),
		];
	elif key == "L":
		return [
			(startPos[0]-2, startPos[1]),
			(startPos[0]-1, startPos[1]),
			(startPos[0], startPos[1]),
			(startPos[0], startPos[1]+1),
		];
	elif key == "O":
		return [
			(startPos[0]-1, startPos[1]),
			(startPos[0]-1, startPos[1]+1),
			(startPos[0], startPos[1]),
			(startPos[0], startPos[1]+1),
		];
	elif key == "S":
		return [
			(startPos[0]-1, startPos[1]+1),
			(startPos[0]-1, startPos[1]),
			(startPos[0], startPos[1]),
			(startPos[0], startPos[1]-1),
		];
	elif key == "Z":
		return [
			(startPos[0]-1, startPos[1]-1),
			(startPos[0]-1, startPos[1]),
			(startPos[0], startPos[1]),
			(startPos[0], startPos[1]+1),
		];
	elif key == "T":
		return [
			(startPos[0]-1, startPos[1]-1),
			(startPos[0]-1, startPos[1]),
			(startPos[0]-1, startPos[1]+1),
			(startPos[0], startPos[1]),
		];
	raise Exception("Error key[{}]".format(key));


class TetrisView(wx.Panel):
	"""docstring for TetrisView"""
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(TetrisView, self).__init__(parent, id, pos = self.params_["pos"], size = self.params_["size"], style = self.params_["style"]);
		self.SetBackgroundColour(self.params_["bgColour"]);
		self.createTimer();
		self.m_playing = False; # 游戏进行中的标记
		# self.m_itemMatrix = []; # 像素背景矩阵
		self.m_fixedItemMatrix = []; # 已固定的方块矩阵
		self.m_movingItemInfo = { # 移动中的方块信息
			"list" : [],
			"rotation" : 0,
		};
		self.initFixedItemMatrix();

	def __del__(self):
		self.stopTimer();

	def initParams(self, params):
		self.params_ = {
			"pos" : (0,0),
			"size" : (360,360),
			"style" : wx.BORDER_NONE,
			"bgColour" : wx.Colour(255,255,255),
			"matrix" : (36,36),
			"squareColour" : wx.Colour(0,0,0),
		};
		for k,v in params.items():
			self.params_[k] = v;

	def createTimer(self):
		self.m_timer = wx.Timer(self);
		self.Bind(wx.EVT_TIMER, self.onTimer, self.m_timer);

	def startTimer(self):
		self.m_timer.Start(100);

	def stopTimer(self):
		if self.m_timer.IsRunning():
			self.m_timer.Stop();

	# def initView(self):
	# 	self.createControls();
	# 	self.initViewLayout();

	# def createControls(self):
	# 	self.createGridViews();

	# def initViewLayout(self):
	# 	gridSizer = wx.GridSizer(self.params_["matrix"][0], self.params_["matrix"][1], 0,0);
	# 	for itemList in self.m_itemMatrix:
	# 		gridSizer.AddMany(itemList);
	# 	self.SetSizerAndFit(gridSizer);

	# def createGridViews(self):
	# 	for i in range(self.params_["matrix"][0]):
	# 		itemList = [];
	# 		fixedItemList = [];
	# 		for j in range(self.params_["matrix"][1]):
	# 			itemList.append(self.createItem());
	# 			fixedItemList.append(0);
	# 		self.m_itemMatrix.append(itemList); # 像素背景矩阵
	# 		self.m_fixedItemMatrix.append(fixedItemList); # 已固定的方块矩阵

	def initFixedItemMatrix(self):
		for i in range(self.params_["matrix"][0]):
			fixedItemList = [];
			for j in range(self.params_["matrix"][1]):
				fixedItemList.append(None);
			self.m_fixedItemMatrix.append(fixedItemList); # 已固定的方块矩阵

	def getItemSize(self):
		rows, cols = self.params_["matrix"][0], self.params_["matrix"][1];
		return wx.Size(self.params_["size"][0]/cols, self.params_["size"][1]/rows);

	def createItem(self):
		return wx.Panel(self, size = self.getItemSize(), style = wx.BORDER_THEME);

	def moveItem(self, item, row, col):
		itemSize = self.getItemSize();
		item.Move(col*itemSize.x, row*itemSize.y);
		item.m_mt = (row, col);

	def moveItemList(self, direction = Direction.BOTTOM):
		if self.checkDirection(direction):
			for item in self.m_movingItemInfo["list"]:
				row, col = item.m_mt;
				if direction == Direction.BOTTOM:
					row+=1;
				elif direction == Direction.LEFT:
					col-=1;
				elif direction == Direction.RIGHT:
					col+=1;
				self.moveItem(item, row, col);
		elif direction == Direction.BOTTOM:
			if not self.checkGameOver():
				self.setFixedItemMatrix();
				self.eliminateSquares();
				self.createMovingItemList();

	def onTimer(self, event = None):
		self.moveItemList();

	def startGame(self, event = None):
		if not self.m_playing:
			self.m_playing = True;
			self.createMovingItemList();
			# self.startTimer();

	def createMovingItemList(self):
		self.m_movingItemInfo["list"] = [];
		col = int(self.params_["matrix"][1]/2);
		itemMtList = getMovingItemMtList((6, col));
		for itemMt in itemMtList:
			item = self.createItem();
			item.SetBackgroundColour(self.params_["squareColour"]);
			self.moveItem(item, *itemMt);
			self.m_movingItemInfo["list"].append(item);

	def setFixedItemMatrix(self, itemList = []):
		if len(itemList) == 0:
			itemList = self.m_movingItemInfo["list"];
		for item in itemList:
			row, col = item.m_mt;
			if row > 0:
				self.m_fixedItemMatrix[row][col] = item;

	def checkDirection(self, direction):
		if direction in [Direction.LEFT, Direction.TOP, Direction.RIGHT, Direction.BOTTOM]:
			for item in self.m_movingItemInfo["list"]:
				row, col = item.m_mt;
				if direction == Direction.BOTTOM:
					row+=1;
				elif direction == Direction.LEFT:
					col-=1;
				elif direction == Direction.RIGHT:
					col+=1;
				rows, cols = self.params_["matrix"][0], self.params_["matrix"][1];
				if row >= rows or col < 0 or col >= cols:
					return False;
				elif row >= 0 and self.m_fixedItemMatrix[row][col]:
					return False;
			return True;
		return False;

	def gameOver(self):
		self.stopTimer();
		self.m_playing = False;
		msgDialog = wx.MessageDialog(self, "游戏结束！", "游戏结束", style = wx.OK|wx.ICON_INFORMATION);
		msgDialog.ShowModal();

	def checkGameOver(self):
		for item in self.m_movingItemInfo["list"]:
			if item.m_mt[0] <= 0:
				self.gameOver();
				return True;
		return False;

	def eliminateSquares(self):
		eliminateCount = 0;
		rows, cols = self.params_["matrix"][0], self.params_["matrix"][1];
		for i in range(rows-1, -1, -1):
			squareCount = 0;
			for j in range(cols):
				if self.m_fixedItemMatrix[i][j]:
					squareCount += 1;
			if squareCount > 0:
				if squareCount == cols:
					for j in range(cols):
						if self.m_fixedItemMatrix[i][j]:
							self.m_fixedItemMatrix[i][j].Destroy();
							self.m_fixedItemMatrix[i][j] = None;
					eliminateCount += 1;
				elif eliminateCount > 0:
					for j in range(cols):
						if self.m_fixedItemMatrix[i][j]:
							self.moveItem(self.m_fixedItemMatrix[i][j], i+eliminateCount, j);
							self.m_fixedItemMatrix[i][j], self.m_fixedItemMatrix[i+eliminateCount][j] = None, self.m_fixedItemMatrix[i][j];
			else:
				break;

	def rotateItemList(self):
		if len(self.m_movingItemInfo["list"]) > 0:
			# 获取Item的移动数据
			rotation = (self.m_movingItemInfo["rotation"] + 90) % 360;
			newItemMtList = [];
			centerRow, centerCol = self.m_movingItemInfo["list"][1].m_mt;
			sinVal, cosVal = math.sin(rotation/360), math.cos(rotation/360);
			for item in self.m_movingItemInfo["list"]:
				row, col = item.m_mt;
				hypotenuse = math.sqrt(math.pow(row - centerRow, 2)+math.pow(col - centerCol, 2));
				newRow = centerRow + int(hypotenuse * sinVal);
				newCol = centerCol + int(hypotenuse * cosVal);
				print((row, col), (newRow, newCol))
				if newCol < 0 or newCol >= self.params_["matrix"][1]:
					return
				newItemMtList.append((item, newRow, newCol));
			# 移动Item
			for itemMt in newItemMtList:
				self.moveItem(*itemMt);
			self.m_movingItemInfo["rotation"] = rotation;


if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, size = (800,700));

	panel = wx.Panel(frame);
	panel.SetBackgroundColour("black");
	tv = TetrisView(panel, params = {"pos" : (40,40), "size" : (200,400), "matrix" : (20,10)})
	btn = wx.Button(panel, label = "开始游戏");
	btn.Bind(wx.EVT_BUTTON, tv.startGame);
	boxSizer = wx.BoxSizer(wx.HORIZONTAL);
	boxSizer.Add(btn);
	boxSizer.Add(tv);
	panel.SetSizer(boxSizer);

	def onCharHook(event = None):
		if event:
			event.DoAllowNextEvent();
			if event.GetUnicodeKey() == 0:
				if event.GetKeyCode() == 314:
					tv.moveItemList(direction = Direction.LEFT);
				# if event.GetKeyCode() == 315:
				# 	tv.updateDirection(Direction.TOP);
				if event.GetKeyCode() == 316:
					tv.moveItemList(direction = Direction.RIGHT);
				# if event.GetKeyCode() == 317:
				# 	tv.updateDirection(Direction.BOTTOM);
			elif event.GetUnicodeKey() == 32:
				tv.rotateItemList();
	app.Bind(wx.EVT_CHAR_HOOK, onCharHook)

	frame.Show(True);
	app.MainLoop();
