# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-26 11:59:06
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-12-28 15:41:32
import wx;
import copy;
import math;
from enum import Enum, unique;

ChessImgConfig = {
	"R_General" : "res/R_General.png",
	"B_General" : "res/B_General.png",
	"R_Advisor" : "res/R_Advisor.png",
	"B_Advisor" : "res/B_Advisor.png",
	"R_Elephant" : "res/R_Elephant.png",
	"B_Elephant" : "res/B_Elephant.png",
	"R_Horse" : "res/R_Horse.png",
	"B_Horse" : "res/B_Horse.png",
	"R_Chariot" : "res/R_Chariot.png",
	"B_Chariot" : "res/B_Chariot.png",
	"R_Cannon" : "res/R_Cannon.png",
	"B_Cannon" : "res/B_Cannon.png",
	"R_Soldier" : "res/R_Soldier.png",
	"B_Soldier" : "res/B_Soldier.png",
};

ChessConfigList = [
	{"value" : -1, "key" : "R_General", "name" : "帥"},
	{"value" : 1, "key" : "B_General", "name" : "將"},
	{"value" : -2, "key" : "R_Advisor", "name" : "仕"},
	{"value" : -2, "key" : "R_Advisor", "name" : "仕"},
	{"value" : 2, "key" : "B_Advisor", "name" : "士"},
	{"value" : 2, "key" : "B_Advisor", "name" : "士"},
	{"value" : -3, "key" : "R_Elephant", "name" : "相"},
	{"value" : -3, "key" : "R_Elephant", "name" : "相"},
	{"value" : 3, "key" : "B_Elephant", "name" : "象"},
	{"value" : 3, "key" : "B_Elephant", "name" : "象"},
	{"value" : -4, "key" : "R_Horse", "name" : "傌"},
	{"value" : -4, "key" : "R_Horse", "name" : "傌"},
	{"value" : 4, "key" : "B_Horse", "name" : "馬"},
	{"value" : 4, "key" : "B_Horse", "name" : "馬"},
	{"value" : -5, "key" : "R_Chariot", "name" : "俥"},
	{"value" : -5, "key" : "R_Chariot", "name" : "俥"},
	{"value" : 5, "key" : "B_Chariot", "name" : "車"},
	{"value" : 5, "key" : "B_Chariot", "name" : "車"},
	{"value" : -6, "key" : "R_Cannon", "name" : "炮"},
	{"value" : -6, "key" : "R_Cannon", "name" : "炮"},
	{"value" : 6, "key" : "B_Cannon", "name" : "砲"},
	{"value" : 6, "key" : "B_Cannon", "name" : "砲"},
	{"value" : -7, "key" : "R_Soldier", "name" : "兵"},
	{"value" : -7, "key" : "R_Soldier", "name" : "兵"},
	{"value" : -7, "key" : "R_Soldier", "name" : "兵"},
	{"value" : -7, "key" : "R_Soldier", "name" : "兵"},
	{"value" : -7, "key" : "R_Soldier", "name" : "兵"},
	{"value" : 7, "key" : "B_Soldier", "name" : "卒"},
	{"value" : 7, "key" : "B_Soldier", "name" : "卒"},
	{"value" : 7, "key" : "B_Soldier", "name" : "卒"},
	{"value" : 7, "key" : "B_Soldier", "name" : "卒"},
	{"value" : 7, "key" : "B_Soldier", "name" : "卒"},
];

@unique
class Direction(Enum):
	LEFT = 0;
	TOP = 1;
	RIGHT = 2;
	BOTTOM = 3;

@unique
class Comparison(Enum):
	LESS = 0;
	EQUAL = 1;
	LARGE = 2;

class Banqi(wx.Panel):
	"""docstring for Banqi"""
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(Banqi, self).__init__(parent, id, pos = self.params_["pos"], size = self.params_["size"], style = self.params_["style"]);
		self.m_gridViews = [];
		self.m_playing, self.m_curPos, self.m_curItem, self.m_emptyBitmap = False, None, None, None;
		self.m_turn = 0;
		# self.initDragView();
		self.SetBackgroundColour(self.params_["bgColour"]);
		self.initView();

	def initParams(self, params):
		self.params_ = {
			"pos" : (0,0),
			"size" : (360,360),
			"style" : wx.BORDER_THEME,
			"bgColour" : wx.Colour(238,168,37),
			"focusColour" : wx.Colour(240,200,37),
			"emptyColour" : wx.Colour(255,255,255),
			"respDist" : 10, # 移动元素的响应距离
		};
		for k,v in params.items():
			self.params_[k] = v;
		self.params_["matrix"] = (4,8); # 固定维度

	def initDragView(self):
		if hasattr(self, "m_dragView"):
			self.m_dragView.Destroy();
		self.m_dragView = wx.Panel(self, size = (40,40));
		wx.StaticBitmap(self.m_dragView, bitmap = wx.Bitmap((40,40), depth=0));
		# self.m_dragView.SetBackgroundColour("gray");
		wx.CallAfter(self.m_dragView.Hide);

	def initView(self):
		self.m_playing = True; # 游戏状态标记
		self.resetTurn();
		self.createControls();
		self.initViewLayout();
		self.initDragView();

	def createControls(self):
		self.createGridViews();

	def initViewLayout(self):
		gridSizer = wx.GridSizer(self.params_["matrix"][0], self.params_["matrix"][1], 0,0);
		for gridView in self.m_gridViews:
			gridSizer.Add(gridView);
		self.SetSizerAndFit(gridSizer);

	def createGridViews(self):
		chessConfList = copy.copy(ChessConfigList);
		self.m_gridViews = [];
		for i in range(self.params_["matrix"][0]):
			for j in range(self.params_["matrix"][1]):
				if len(chessConfList) > 0:
					chessConfig = chessConfList.pop();
					gridView = self.createItem(wx.Point(i,j), chessConfig);
					self.m_gridViews.append(gridView);

	def createItem(self, mtPos, config):
		p = wx.Panel(self, style = wx.BORDER_THEME);
		p.m_matrixPos = mtPos;
		img = wx.Image(ChessImgConfig[config["key"]], wx.BITMAP_TYPE_ANY);
		bm = wx.StaticBitmap(p, bitmap = wx.BitmapFromImage(img));
		bm.m_value = config["value"];
		bx = wx.BoxSizer(wx.VERTICAL);
		bx.Add(bm);
		p.SetSizerAndFit(bx);
		self.bindEventToItem(p, bm);
		p.m_bitmap = bm;
		wx.CallAfter(p.m_bitmap.Hide);
		return p;

	def bindEventToItem(self, item, bitmap):
		item.Bind(wx.EVT_LEFT_DOWN, self.onItemClick);
		item.Bind(wx.EVT_LEFT_UP, self.onItemLeftUp);
		item.Bind(wx.EVT_MOTION, self.onItemMotion);
		item.Bind(wx.EVT_LEFT_DCLICK, self.onItemDClick);
		def onBitmapClick(event):
			self.onItemClick(event, item);
		def onBitmapMotion(event):
			self.onItemMotion(event, item);
		bitmap.Bind(wx.EVT_LEFT_DOWN, onBitmapClick);
		bitmap.Bind(wx.EVT_MOTION, onBitmapMotion);

	def onItemClick(self, event = None, item = None):
		if not item and event:
			item = event.GetEventObject();
		if item:
			if self.m_playing:
				if self.m_curItem != item:
					item.SetBackgroundColour(self.params_["focusColour"]);
					item.Refresh();
					# 重置self.m_curItem
					if self.m_curItem:
						if not self.m_curItem.m_bitmap.IsShown():
							self.m_curItem.SetBackgroundColour(self.params_["bgColour"]);
						else:
							self.m_curItem.SetBackgroundColour(self.params_["emptyColour"]);
						self.m_curItem.Refresh();
					self.m_curItem = item;
				# 重置self.m_curPos
				if event:
					self.m_curPos = event.GetPosition();
					event.Skip();
			else:
				# 显示游戏结束信息弹窗
				self.showMessageDialog("请重新开始游戏！", "游戏已结束");

	def onItemLeftUp(self, event = None, item = None):
		if not item and event:
			item = event.GetEventObject();
		if item and self.m_playing:
			self.m_curPos = None;

	def onItemDClick(self, event = None, item = None):
		if not item and event:
			item = event.GetEventObject();
		if item and not item.m_bitmap.IsShown():
			item.m_bitmap.Show();
			item.SetBackgroundColour(self.params_["focusColour"]);
			item.Refresh();
			# 判断游戏是否结束
			self.checkGameOver(item);
			self.changeTurn(item);

	def onItemMotion(self, event = None, item = None):
		if not item and event:
			item = event.GetEventObject();
		if event.Dragging() and event.LeftIsDown() and self.m_playing and self.m_curPos:
			if self.m_curItem and self.m_curItem.m_bitmap.IsShown() and self.m_curItem.m_bitmap.m_value != 0 and self.checkItemTurn(self.m_curItem):
				# if item:
				# 	item.SetBackgroundColour("gray");
				if not self.m_dragView.IsShown():
					self.m_dragView.Show();
				newPos = self.ScreenToClient(event.GetEventObject().ClientToScreen(event.GetPosition()));
				self.m_dragView.Move(newPos.x-20, newPos.y-20);
				# 处理校验逻辑
				pos = event.GetPosition() - self.m_curPos;
				direction = None;
				respDist = self.params_["respDist"];
				fabsX, fabsY = math.fabs(pos.x), math.fabs(pos.y);
				if fabsX > respDist or fabsY > respDist:
					self.m_curPos = None;
					if fabsX < fabsY:
						direction = pos.y < 0 and Direction.TOP or Direction.BOTTOM;
					else:
						direction = pos.x < 0 and Direction.LEFT or Direction.RIGHT;
					# 移动Item
					self.moveItem(self.m_curItem, direction);

	def moveItem(self, item, direction):
		bm = item.m_bitmap;
		mtPos = item.m_matrixPos;
		tgPos = [mtPos.x, mtPos.y];
		if direction == Direction.TOP:
			if mtPos.x > 0:
				tgPos[0] -= 1;
		elif direction == Direction.BOTTOM:
			if mtPos.x < self.params_["matrix"][0]-1:
				tgPos[0] += 1;
		elif direction == Direction.LEFT:
			if mtPos.y > 0:
				tgPos[1] -= 1;
		elif direction == Direction.RIGHT:
			if mtPos.y < self.params_["matrix"][1]-1:
				tgPos[1] += 1;
		if tgPos[0] != mtPos.x or tgPos[1] != mtPos.y:
			isMove = False;
			tgItem = self.m_gridViews[tgPos[0]*self.params_["matrix"][1] + tgPos[1]];
			bitmap = tgItem.m_bitmap;
			if bitmap.IsShown():
				ret = self.checkBitmapValue(bm, bitmap);
				if ret != Comparison.LARGE:
					self.changeBitmap(bm, bitmap, ret);
					self.onItemClick(item = tgItem);
					# 判断游戏是否结束
					self.checkGameOver(tgItem);
					self.changeTurn(tgItem);

	def checkBitmapValue(self, srcBitmap, tgBitmap):
		if tgBitmap.m_value == 0:
			return Comparison.LESS;
		srcAbsValue = math.fabs(srcBitmap.m_value);
		tgAbsValue = math.fabs(tgBitmap.m_value);
		if srcBitmap.m_value/srcAbsValue != tgBitmap.m_value/tgAbsValue:	
			if srcAbsValue == tgAbsValue:
				return Comparison.EQUAL;
			elif srcAbsValue < tgAbsValue:
				return Comparison.LESS;
		return Comparison.LARGE;

	def changeBitmap(self, srcBitmap, tgBitmap, result):
		if result == Comparison.EQUAL:
			tgBitmap.m_value = 0;
			tgBitmap.SetBitmap(self.getEmptyBitmap(tgBitmap.GetSize()));
		else:
			tgBitmap.m_value = srcBitmap.m_value;
			tgBitmap.SetBitmap(srcBitmap.GetBitmap());
		srcBitmap.m_value = 0;
		srcBitmap.SetBitmap(self.getEmptyBitmap(srcBitmap.GetSize()));

	def getEmptyBitmap(self, size):
		if not self.m_emptyBitmap:
			self.m_emptyBitmap = wx.Bitmap(size, depth=255);
		return self.m_emptyBitmap;

	def resetTurn(self):
		self.m_turn = -1;
		if hasattr(self, "onChangeTurn"):
			self.onChangeTurn(self.m_turn);

	def changeTurn(self, item = None):
		if self.m_turn == -1 and (item and item.m_bitmap.m_value != 0):
			self.m_turn = item.m_bitmap.m_value > 0 and 1 or 0;
		self.m_turn = (self.m_turn + 1) % 2;
		if hasattr(self, "onChangeTurn"):
			self.onChangeTurn(self.m_turn);

	def checkItemTurn(self, item):
		bitmap = item.m_bitmap;
		if not bitmap.IsShown():
			return True;
		if bitmap.m_value == 0:
			return False;
		if (bitmap.m_value > 0 and 1 or 0) == self.m_turn:
			return True;
		# # 弹窗提示
		# self.showMessageDialog("您不能操作对方的棋子！", "提示");
		return False;

	def checkGameOver(self, item):
		if self.checkCount(item):
			# 回调游戏结束方法
			if hasattr(self, "onGameOver"):
				self.onGameOver();
			# 显示游戏结束信息弹窗
			self.showMessageDialog("游戏结束！", "游戏结束");
			# 重置游戏状态
			self.m_playing = False;

	def checkCount(self, item):
		sign = item.m_bitmap.m_value > 0 and 1 or -1;
		for gridView in self.m_gridViews:
			value = gridView.m_bitmap.m_value;
			if value * sign < 0:
				return False;
		return True;

	def showMessageDialog(self, message, caption):
		msgDialog = wx.MessageDialog(self, message, caption, style = wx.OK|wx.ICON_INFORMATION);
		msgDialog.ShowModal();

def createCtrPanel(parent):
	ctrP = wx.Panel(parent);
	ctrP.SetBackgroundColour("white");
	ctrP.btn = wx.Button(ctrP, label = "重新开始");
	t = wx.StaticText(ctrP, label = "当前操作方：");
	ctrP.text = wx.StaticText(ctrP, label = "--");
	boxSizer = wx.BoxSizer(wx.VERTICAL);
	boxSizer.Add(ctrP.btn);
	boxSizer.Add(t);
	boxSizer.Add(ctrP.text);
	ctrP.SetSizer(boxSizer);
	return ctrP;

if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, size = (700,360));

	panel = wx.Panel(frame);
	panel.SetBackgroundColour("black");
	bq = Banqi(panel, params = {"pos" : (40,40), "size" : (560,280)})
	ctrP = createCtrPanel(panel)
	def onChangeTurn(turn):
		if turn == -1:
			ctrP.text.SetLabel("--");
		elif turn == 0:
			ctrP.text.SetLabel("红方");
		else:
			ctrP.text.SetLabel("黑方");
	bq.onChangeTurn = onChangeTurn;
	boxSizer = wx.BoxSizer(wx.HORIZONTAL);
	boxSizer.Add(ctrP);
	boxSizer.Add(bq);
	panel.SetSizer(boxSizer);

	frame.Show(True);
	app.MainLoop();