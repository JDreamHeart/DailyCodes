# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-25 10:31:47
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-01-08 23:45:11
import wx;
import random, math;
from enum import Enum, unique;

from Snake import Direction, Snake;

@unique
class Mark(Enum):
	BLANK = 0;
	SNAKE = 1;
	FOOD = 2;

class SnakeView(wx.Panel):
	"""docstring for SnakeView"""
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(SnakeView, self).__init__(parent, id, pos = self.params_["pos"], size = self.params_["size"], style = self.params_["style"]);
		self.m_playing = False; # 游戏进行中的标记
		self.SetBackgroundColour(self.params_["bgColour"]);
		self.createSnake();
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

	# 创建蛇体
	def createSnake(self):
		params = {
			"size" : self.getItemSize(),
			"bgColour" : self.params_["snakeColour"],
			"matrix" : (36,36),
		};
		self.m_snake = Snake(params = params);

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
		pass;

	def initViewLayout(self):
		pass;

	def getItemSize(self):
		rows, cols = self.params_["matrix"][0], self.params_["matrix"][1];
		return wx.Size(self.params_["size"][0]/cols, self.params_["size"][1]/rows);

	def createItem(self):
		return wx.Panel(self, size = self.getItemSize(), style = wx.BORDER_NONE);

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

	def initGame(self):
		idx = math.floor(self.params_["matrix"][0]*self.params_["matrix"][1]/2);
		itemPos = self.m_snake.getPos(idx = idx);
		item = self.createItem();
		item.Move(itemPos.x, itemPos.y);
		item.SetBackgroundColour(self.params_["foodColour"]);
		item.Refresh();
		direction = random.choice([Direction.LEFT, Direction.TOP, Direction.RIGHT, Direction.BOTTOM]);
		self.m_snake.setDirection(direction);
		self.m_snake.eat(item);

	def startGame(self, event = None):
		if not self.m_playing:
			self.initGame();
			self.setFoodItem();
			self.startTimer();
			self.m_playing = True;

	def setFoodItem(self):
		blankIdxs = self.m_snake.getBlankIdxs();
		idx = random.randint(0, len(blankIdxs)-1);
		itemPos = self.m_snake.getPos(idx = idx);
		item = self.createItem();
		item.Move(itemPos.x, itemPos.y);
		item.SetBackgroundColour(self.params_["foodColour"]);
		item.Refresh();


if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, size = (700,600));

	panel = wx.Panel(frame);
	panel.SetBackgroundColour("black");
	sn = SnakeView(panel, params = {"pos" : (40,40), "size" : (540,540)})
	btn = wx.Button(panel, label = "开始游戏");
	btn.Bind(wx.EVT_BUTTON, sn.startGame);
	boxSizer = wx.BoxSizer(wx.HORIZONTAL);
	boxSizer.Add(btn);
	boxSizer.Add(sn);
	panel.SetSizer(boxSizer);

	frame.Show(True);
	app.MainLoop();