# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-25 10:31:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-08 19:24:33
import wx;
from enum import Enum, unique;

@unique
class Mark(Enum):
	BLANK = 0;
	SNAKE = 1;
	FOOD = 2;

class Snake(object):
	"""docstring for Snake"""
	def __init__(self, parent, params = {}):
		self.initParams(params);
		super(Snake, self).__init__();
		self.m_bodyList = []; # 蛇体【0:head; -1:tail】
		self.m_direction = Direction.LEFT; # 蛇移动方向
		self.m_parent = parent;

	def initParams(self, params):
		self.params_ = {
			"size" : (10,10),
			"style" : wx.BORDER_NONE,
			"bgColour" : wx.Colour(0,0,0),
		};
		for k,v in params.items():
			self.params_[k] = v;

	def eat(self, item):
		item.SetBackgroundColour(self.params_["bgColour"]);
		item.Refresh();
		self.m_bodyList.insert(0, item);

	def move(self, pos):
		self.m_bodyList[0].Move(pos.x, pos.y);
		for i in range(1, len(self.m_bodyList)):
			prePos = self.m_bodyList[i-1].GetPosition();
			self.m_bodyList[i].Move(prePos.x, prePos.y);
	
	def check(self, pos):
		pass;
