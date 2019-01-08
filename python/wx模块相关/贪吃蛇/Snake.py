# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-25 10:31:47
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-01-08 23:45:50
import wx;
import math;
from enum import Enum, unique;

@unique
class Direction(Enum):
	LEFT = 0;
	TOP = 1;
	RIGHT = 2;
	BOTTOM = 3;

class Snake(object):
	"""docstring for Snake"""
	def __init__(self, params = {}):
		self.initParams(params);
		super(Snake, self).__init__();
		self.m_bodyList = []; # 蛇体【0:head; -1:tail】
		self.m_direction = Direction.LEFT; # 蛇移动方向
		self.init();

	def initParams(self, params):
		self.params_ = {
			"size" : (10,10),
			"bgColour" : wx.Colour(0,0,0),
			"matrix" : (36,36),
		};
		for k,v in params.items():
			self.params_[k] = v;

	def init(self):
		self.m_blankIdxs = range(0, self.params_["matrix"][0]*self.params_["matrix"][1]); # 空白位置列表

	def eat(self, item):
		item.SetBackgroundColour(self.params_["bgColour"]);
		item.Refresh();
		self.m_bodyList.insert(0, item);
		self.m_blankIdxs.remove(self.getIdx(item.GetPosition()));

	def move(self, idx):
		pos = self.getPos(idx = idx);
		lastPos = self.m_bodyList[0].GetPosition();
		self.m_bodyList[0].Move(pos.x, pos.y);
		for i in range(1, len(self.m_bodyList)):
			prePos = self.m_bodyList[i-1].GetPosition();
			lastPos = self.m_bodyList[i-1].GetPosition();
			self.m_bodyList[i].Move(prePos.x, prePos.y);
		self.m_blankIdxs.remove(idx);
		self.m_blankIdxs.append(self.getIdx(lastPos));
	
	def check(self):
		if len(self.m_bodyList) > 0 and self.checkDirection():
			itemPos = self.m_bodyList[0].GetPosition();
			itemRow, itemCol = itemPos.x/10, itemPos.y/10;
			if self.m_direction == Direction.LEFT:
				itemCol-=1;
			elif self.m_direction == Direction.TOP:
				itemRow-=1;
			elif self.m_direction == Direction.RIGHT:
				itemCol+=1;
			elif self.m_direction == Direction.BOTTOM:
				itemRow+=1;
			rows, cols = self.params_["matrix"][0], self.params_["matrix"][1];
			if itemRow >= 0 and itemRow < rows and itemCol >= 0 or itemCol < cols:
				targetIdx = itemRow*cols+itemCol;
				if targetIdx in self.m_blankIdxs:
					return True, targetIdx;
		return False, -1;

	def checkDirection(self, direction):
		if self.m_direction in [Direction.LEFT, Direction.TOP, Direction.RIGHT, Direction.BOTTOM]:
			return True;
		return False;

	def setDirection(self, direction):
		if self.checkDirection(direction):
			self.m_direction == direction;

	def getPos(self, row = 0, col = 0, idx = -1):
		if idx >= 0:
			cols = self.params_["matrix"][1];
			row = math.floor(idx/cols);
			col = idx % cols;
		return wx.Point(row*self.params_["size"][0], col*self.params_["size"][1]);

	def getIdx(self, pos):
		return pos.x/self.params_["size"][0], pos.y/self.params_["matrix"][1]

	def getBlankIdxs(self):
		return self.m_blankIdxs;
