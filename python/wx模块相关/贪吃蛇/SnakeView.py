# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-25 10:31:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-23 15:29:27
import wx;
import random;

from Snake import Direction, Snake;

DirectionConfig = {
	Direction.LEFT : "HORIZONTAL",
	Direction.RIGHT : "HORIZONTAL",
	Direction.TOP : "VERTICAL",
	Direction.BOTTOM : "VERTICAL",
};

class SnakeView(wx.Panel):
	"""docstring for SnakeView"""
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(SnakeView, self).__init__(parent, id, pos = self.params_["pos"], size = self.params_["size"], style = self.params_["style"]);
		self.SetBackgroundColour(self.params_["bgColour"]);
		self.createSnake();
		self.createTimer();
		self.m_playing = False; # 游戏进行中的标记
		self.m_foodInfoMap = {}; # 食物信息表【key = idx, value = item】
		self.m_direction = self.m_snake.m_direction; # 初始化方向

	def __del__(self):
		self.stopTimer();

	def initParams(self, params):
		self.params_ = {
			"pos" : (0,0),
			"size" : (360,360),
			"style" : wx.BORDER_NONE,
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
			"matrix" : self.params_["matrix"],
		};
		self.m_snake = Snake(params = params);

	def createTimer(self):
		self.m_timer = wx.Timer(self);
		self.Bind(wx.EVT_TIMER, self.onTimer, self.m_timer);

	def startTimer(self):
		self.m_timer.Start(100);

	def stopTimer(self):
		if self.m_timer.IsRunning():
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
		p = wx.Panel(self, size = self.getItemSize(), style = wx.BORDER_NONE);
		p.m_text = wx.StaticText(p, label = "9");
		p.m_text.SetFont(wx.Font(6, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(p.m_text, flag = wx.ALIGN_CENTER);
		p.SetSizer(box)
		p.m_timer = wx.Timer(p);
		p.m_isFlash = False;
		def onItemTimer(event = None):
			remainTime = int(p.m_text.GetLabel()) - 1;
			if remainTime >= 0:
				p.m_text.SetLabel(str(remainTime));
				if p.m_isFlash:
					if p.IsShown():
						p.Hide();
					else:
						p.Show();
				if remainTime <= 3 and not p.m_isFlash:
					p.m_text.SetLabel(str(remainTime * 10));
					p.m_isFlash = True;
					p.m_timer.Stop();
					p.m_timer.Start(100);
			else:
				idx = self.m_snake.getIdx(p.GetPosition());
				if idx in self.m_foodInfoMap:
					self.createFoodItem();
					foodItem = self.m_foodInfoMap.pop(idx);
					foodItem.Destroy();
		p.Bind(wx.EVT_TIMER, onItemTimer, p.m_timer);
		p.m_timer.Start(1000);
		return p;

	def moveSnake(self):
		ret,idx = self.m_snake.check();
		if ret:
			if idx in self.m_foodInfoMap:
				self.m_snake.eat(self.m_foodInfoMap[idx]);
				self.createFoodItem();
				del self.m_foodInfoMap[idx];
			else:
				self.m_snake.move(idx);
		else:
			self.gameOver();

	def gameOver(self):
		self.stopTimer();
		self.m_playing = False;
		msgDialog = wx.MessageDialog(self, "游戏结束！", "游戏结束", style = wx.OK|wx.ICON_INFORMATION);
		msgDialog.ShowModal();

	def onTimer(self, event = None):
		self.moveSnake();
		self.m_direction = self.m_snake.m_direction;

	def initGame(self):
		row = int(self.params_["matrix"][0]/2);
		col = int(self.params_["matrix"][1]/2);
		itemPos = self.m_snake.getPos(row = row, col = col);
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
			for i in range(3):
				self.createFoodItem();
			self.startTimer();
			self.m_playing = True;

	def createFoodItem(self):
		idx = random.randint(0, len(self.m_snake.getBlankIdxs())-1);
		itemPos = self.m_snake.getPos(idx = idx);
		item = self.createItem();
		item.Move(itemPos.x, itemPos.y);
		item.SetBackgroundColour(self.params_["foodColour"]);
		item.Refresh();
		self.m_foodInfoMap[idx] = item;

	def updateDirection(self, direction):
		if direction in DirectionConfig and DirectionConfig[self.m_direction] != DirectionConfig[direction]:
			self.m_snake.setDirection(direction);


if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, size = (800,700));

	panel = wx.Panel(frame);
	panel.SetBackgroundColour("black");
	sn = SnakeView(panel, params = {"pos" : (40,40), "size" : (600,600), "matrix" : (60,60)})
	btn = wx.Button(panel, label = "开始游戏");
	btn.Bind(wx.EVT_BUTTON, sn.startGame);
	boxSizer = wx.BoxSizer(wx.HORIZONTAL);
	boxSizer.Add(btn);
	boxSizer.Add(sn);
	panel.SetSizer(boxSizer);

	def onCharHook(event = None):
		if event:
			event.DoAllowNextEvent();
			if event.GetUnicodeKey() == 0:
				if event.GetKeyCode() == 314:
					sn.updateDirection(Direction.LEFT);
				if event.GetKeyCode() == 315:
					sn.updateDirection(Direction.TOP);
				if event.GetKeyCode() == 316:
					sn.updateDirection(Direction.RIGHT);
				if event.GetKeyCode() == 317:
					sn.updateDirection(Direction.BOTTOM);
	app.Bind(wx.EVT_CHAR_HOOK, onCharHook)

	frame.Show(True);
	app.MainLoop();
