# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-25 10:31:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-08 18:40:52
import wx;
import random, math;
from enum import Enum, unique;

@unique
class Mark(Enum):
	BLANK = 0;
	SNAKE = 1;
	FOOD = 2;

@unique
class Direction(Enum):
	LEFT = 0;
	TOP = 1;
	RIGHT = 2;
	BOTTOM = 3;

class Snake(wx.Panel):
	"""docstring for Snake"""
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(Snake, self).__init__(parent, id, pos = self.params_["pos"], size = self.params_["size"], style = self.params_["style"]);
		self.m_gridViews = []; # 像素点网格
		self.m_snakeBody = []; # 蛇体
		self.m_blankList = []; # 空格列表
		self.m_playing = False; # 游戏进行中的标记
		self.m_direction = Direction.LEFT; # 蛇移动方向
		self.SetBackgroundColour(self.params_["bgColour"]);
		self.initView();
		self.createTimer();

	def __del__(self):
		self.stopTimer();

	def initParams(self, params):
		self.params_ = {
			"pos" : (0,0),
			"size" : (360,360),
			"style" : wx.BORDER_THEME,
			"bgColour" : wx.Colour(255,255,255),
			"matrix" : (36,36),
			"snakeColour" : wx.Colour(0,0,0),
			"foodColour" : wx.Colour(0,200,0),
		};
		for k,v in params.items():
			self.params_[k] = v;

	def createTimer(self):
		self.m_timer = wx.Timer(self);
		self.Bind(wx.EVT_TIMER, self.onTimer, self.m_timer);

	def startTimer(self):
		self.m_timer.Start(100);

	def stopTimer(self):
		self.m_timer.Stop();

	def initView(self):
		self.createControls();
		self.initViewLayout();

	def createControls(self):
		# self.createGridViews();

	def initViewLayout(self):
		# gridSizer = wx.GridSizer(self.params_["matrix"][0], self.params_["matrix"][1], 0,0);
		# for gridView in self.m_gridViews:
		# 	gridSizer.Add(gridView);
		# self.SetSizerAndFit(gridSizer);
		pass;

	def createGridViews(self):
		self.m_gridViews = [];
		rows, cols = self.params_["matrix"][0], self.params_["matrix"][1];
		gridViewSide = min(self.params_["size"][0]/cols, self.params_["size"][1]/rows);
		for i in range(rows):
			for j in range(cols):
				gridView = wx.Panel(self, size = (gridViewSide, gridViewSide), style = wx.BORDER_NONE);
				gridView.m_pos = wx.Point(i,j);
				gridView.m_mark = Mark.BLANK;
				self.m_gridViews.append(gridView);
				self.m_blankList.append(gridView);

	def moveSnake(self, direction):
		pass;

	def checkGameOver(self, item):
		if self.checkItemNextPos(item.m_pos, direction):
			msgDialog = wx.MessageDialog(self, "游戏结束！", "游戏结束", style = wx.OK|wx.ICON_INFORMATION);
			msgDialog.ShowModal();

	def checkCount(self, pos, direction):
		# if direction == Direction.
		return False;

	def onTimer(self, event = None):
		self.moveSnake(self.m_direction);

	def startGame(self, event = None):
		if not self.m_playing:
			idx = int(len(self.m_blankList)/2);
			item = self.m_blankList.pop(idx);
			item.SetBackgroundColour(self.params_["snakeColour"]);
			item.Refresh();
			self.m_direction = random.choice([Direction.LEFT, Direction.TOP, Direction.RIGHT, Direction.BOTTOM]);
			self.setFoodItem();
			self.startTimer();
			self.m_playing = True;

	def setFoodItem(self):
		idx = random.randint(0, len(self.m_blankList)-1);
		item = self.m_blankList.pop(idx);
		item.SetBackgroundColour(self.params_["foodColour"]);
		item.Refresh();


if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, size = (700,600));

	panel = wx.Panel(frame);
	panel.SetBackgroundColour("black");
	sn = Snake(panel, params = {"pos" : (40,40), "size" : (540,540)})
	btn = wx.Button(panel, label = "开始游戏");
	btn.Bind(wx.EVT_BUTTON, sn.startGame);
	boxSizer = wx.BoxSizer(wx.HORIZONTAL);
	boxSizer.Add(btn);
	boxSizer.Add(sn);
	panel.SetSizer(boxSizer);

	frame.Show(True);
	app.MainLoop();