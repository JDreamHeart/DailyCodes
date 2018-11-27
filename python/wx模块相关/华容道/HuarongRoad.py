# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-11-13 10:10:06
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-11-14 18:05:48

import wx;
import math;
from enum import Enum, unique;

@unique
class Direction(Enum):
	LEFT = 0;
	TOP = 1;
	RIGHT = 2;
	BOTTOM = 3;

class HuarongRoad(wx.Panel):
	"""docstring for HuarongRoad"""
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(HuarongRoad, self).__init__(parent, id, size = self.params_["size"], style = self.params_["style"]);
		self.SetBackgroundColour("grey");
		self.initView();
		self.curItem = None;

	def initParams(self, params):
		self.params_ = {
			"size" : (0,0),
			"style" : wx.BORDER_THEME,
			"matrix" : (4,4),
		};
		for k,v in params.items():
			self.params_[k] = v;

	def initView(self):
		self.createControls();
		self.initViewLayout();

	def createControls(self):
		self.createCaoCao();
		self.createZhangFei();
		self.createZhaoYun();
		self.createGuanYu();
		self.createSoldiers();

	def initViewLayout(self):
		bagSizer = wx.GridBagSizer(0,0);
		bagSizer.Add(self.ZhangFei, pos = (1,1), span = (2,1));
		bagSizer.Add(self.CaoCao, pos = (1,2), span = (2,2));
		bagSizer.Add(self.ZhaoYun, pos = (1,4), span = (2,1));
		bagSizer.Add(self.GuanYu, pos = (3,2), span = (1,2));
		bagSizer.Add(self.Soldiers[0], pos = (3,1), span = (1,1));
		bagSizer.Add(self.Soldiers[1], pos = (3,4), span = (1,1));
		bagSizer.Add(self.Soldiers[2], pos = (4,1), span = (1,1));
		bagSizer.Add(self.Soldiers[3], pos = (4,4), span = (1,1));
		self.SetSizerAndFit(bagSizer);
		pass;

	def createCaoCao(self):
		self.CaoCao = wx.Panel(self, size = (self.GetSize().x/2, self.GetSize().y/2), style = wx.BORDER_THEME);
		self.CaoCao.SetBackgroundColour("white");
		self.bindEventToItem(self.CaoCao);

	def createZhangFei(self):
		self.ZhangFei = wx.Panel(self, size = (self.GetSize().x/4, self.GetSize().y/2), style = wx.BORDER_THEME);
		self.ZhangFei.SetBackgroundColour("green");
		self.bindEventToItem(self.ZhangFei);

	def createZhaoYun(self):
		self.ZhaoYun = wx.Panel(self, size = (self.GetSize().x/4, self.GetSize().y/2), style = wx.BORDER_THEME);
		self.ZhaoYun.SetBackgroundColour("yellow");
		self.bindEventToItem(self.ZhaoYun);

	def createGuanYu(self):
		self.GuanYu = wx.Panel(self, size = (self.GetSize().x/2, self.GetSize().y/4), style = wx.BORDER_THEME);
		self.GuanYu.SetBackgroundColour("red");
		self.bindEventToItem(self.GuanYu);

	def createSoldiers(self):
		self.Soldiers = [];
		for i in range(0,4):
			soldier = wx.Panel(self, size = (self.GetSize().x/4, self.GetSize().y/4), style = wx.BORDER_THEME);
			soldier.SetBackgroundColour("blue");
			self.bindEventToItem(soldier);
			self.Soldiers.append(soldier);

	def bindEventToItem(self, item):
		item.Bind(wx.EVT_LEFT_DOWN, self.onClick);
		item.Bind(wx.EVT_MOTION, self.onMotion);

	def onClick(self, event):
		self.curPos = event.GetPosition();
		event.Skip();

	def onMotion(self, event):
		if event.Dragging() and event.LeftIsDown() and self.curPos:
			pos = event.GetPosition() - self.curPos;
			direction = None;
			if math.fabs(pos.x) > 8:
				self.curPos = None;
				if pos.x < 0:
					direction = Direction.LEFT;
				else:
					direction = Direction.RIGHT;
				if self.moveItem(event.GetEventObject(), direction):
					return True;
			if math.fabs(pos.y) > 8:
				self.curPos = None;
				if pos.y < 0:
					direction = Direction.TOP;
				else:
					direction = Direction.BOTTOM;
				if self.moveItem(event.GetEventObject(), direction):
					return True;

	def moveItem(self, item, direction):
		try:
			pos = self.GetSizer().GetItemPosition(item);
			isLayout = False;
			if direction == Direction.LEFT:
				if pos[1] - 1 > 0 :
					isLayout = True;
					self.GetSizer().SetItemPosition(item, wx.GBPosition(pos[0], pos[1] - 1));
			elif direction == Direction.TOP:
				if pos[0] - 1 > 0 :
					isLayout = True;
					self.GetSizer().SetItemPosition(item, wx.GBPosition(pos[0] - 1, pos[1]));
			elif direction == Direction.RIGHT:
				if pos[1] + 1 <= self.params_["matrix"][1] :
					isLayout = True;
					self.GetSizer().SetItemPosition(item, wx.GBPosition(pos[0], pos[1] + 1));
			elif direction == Direction.BOTTOM:
				if pos[0] + 1 <= self.params_["matrix"][0] :
					isLayout = True;
					self.GetSizer().SetItemPosition(item, wx.GBPosition(pos[0] + 1, pos[1]));
			if isLayout:
				self.GetSizer().Layout();
				self.checkGameOver();
		except Exception:
			pass;

	def checkGameOver(self):
		pos = self.GetSizer().GetItemPosition(self.CaoCao);
		if pos[0] == 3 and pos[1] == 3:
			print("========== Game Over ==========");

	def restart(self, event):
		self.GetSizer().Clear(True);
		self.SetSize(self.params_["size"]);
		self.initView();

if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, size = (300,300));

	panel = wx.Panel(frame);
	panel.SetBackgroundColour("black");
	hr = HuarongRoad(panel, params = {"size" : (200,200)})
	btn = wx.Button(panel, label = "重新开始");
	btn.Bind(wx.EVT_BUTTON, hr.restart);
	boxSizer = wx.BoxSizer(wx.HORIZONTAL);
	boxSizer.Add(hr);
	boxSizer.Add(btn);
	panel.SetSizer(boxSizer);

	frame.Show(True);
	app.MainLoop();