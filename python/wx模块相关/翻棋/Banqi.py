# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-26 11:59:06
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-12-27 18:54:44
import wx;
import copy;

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
	{"value" : 0, "key" : "R_General", "name" : "帥"},
	{"value" : 0, "key" : "B_General", "name" : "將"},
	{"value" : 1, "key" : "R_Advisor", "name" : "仕"},
	{"value" : 1, "key" : "R_Advisor", "name" : "仕"},
	{"value" : 1, "key" : "B_Advisor", "name" : "士"},
	{"value" : 1, "key" : "B_Advisor", "name" : "士"},
	{"value" : 2, "key" : "R_Elephant", "name" : "相"},
	{"value" : 3, "key" : "R_Elephant", "name" : "相"},
	{"value" : 3, "key" : "B_Elephant", "name" : "象"},
	{"value" : 3, "key" : "B_Elephant", "name" : "象"},
	{"value" : 4, "key" : "R_Horse", "name" : "傌"},
	{"value" : 4, "key" : "R_Horse", "name" : "傌"},
	{"value" : 4, "key" : "B_Horse", "name" : "馬"},
	{"value" : 4, "key" : "B_Horse", "name" : "馬"},
	{"value" : 5, "key" : "R_Chariot", "name" : "俥"},
	{"value" : 5, "key" : "R_Chariot", "name" : "俥"},
	{"value" : 5, "key" : "B_Chariot", "name" : "車"},
	{"value" : 5, "key" : "B_Chariot", "name" : "車"},
	{"value" : 6, "key" : "R_Cannon", "name" : "炮"},
	{"value" : 6, "key" : "R_Cannon", "name" : "炮"},
	{"value" : 6, "key" : "B_Cannon", "name" : "砲"},
	{"value" : 6, "key" : "B_Cannon", "name" : "砲"},
	{"value" : 7, "key" : "R_Soldier", "name" : "兵"},
	{"value" : 7, "key" : "R_Soldier", "name" : "兵"},
	{"value" : 7, "key" : "R_Soldier", "name" : "兵"},
	{"value" : 7, "key" : "R_Soldier", "name" : "兵"},
	{"value" : 7, "key" : "R_Soldier", "name" : "兵"},
	{"value" : 7, "key" : "B_Soldier", "name" : "卒"},
	{"value" : 7, "key" : "B_Soldier", "name" : "卒"},
	{"value" : 7, "key" : "B_Soldier", "name" : "卒"},
	{"value" : 7, "key" : "B_Soldier", "name" : "卒"},
	{"value" : 7, "key" : "B_Soldier", "name" : "卒"},
];

class Banqi(wx.Panel):
	"""docstring for Banqi"""
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(Banqi, self).__init__(parent, id, pos = self.params_["pos"], size = self.params_["size"], style = self.params_["style"]);
		self.m_gridViews = [];
		self.m_curItem = None;
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
		};
		for k,v in params.items():
			self.params_[k] = v;
		self.params_["matrix"] = (4,8); # 固定维度

	def initView(self):
		self.createControls();
		self.initViewLayout();

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
		p.m_value = config["value"];
		img = wx.Image(ChessImgConfig[config["key"]], wx.BITMAP_TYPE_ANY);
		bm = wx.StaticBitmap(p, bitmap = wx.BitmapFromImage(img));
		bx = wx.BoxSizer(wx.VERTICAL);
		bx.Add(bm);
		p.SetSizerAndFit(bx);
		self.bindEventToItem(p, bm);
		p.m_bitmap = bm;
		wx.CallAfter(p.m_bitmap.Hide);
		return p;

	def bindEventToItem(self, item, bitmap):
		item.Bind(wx.EVT_LEFT_DOWN, self.onItemClick);
		item.Bind(wx.EVT_LEFT_DCLICK, self.onItemDClick);
		def onClickText(event):
			self.onItemClick(event, item);
		bitmap.Bind(wx.EVT_LEFT_DOWN, onClickText);

	def onItemClick(self, event = None, item = None):
		if not item and event:
			item = event.GetEventObject();
		if item:
			item.SetBackgroundColour(self.params_["focusColour"]);
			item.Refresh();
			# 重置self.m_curItem
			if self.m_curItem:
				if self.m_curItem.m_bitmap:
					self.m_curItem.SetBackgroundColour(self.params_["bgColour"]);
				else:
					self.m_curItem.SetBackgroundColour(self.params_["emptyColour"]);
				self.m_curItem.Refresh();
			self.m_curItem = item;
		pass;

	def onItemDClick(self, event = None, item = None):
		if not item and event:
			item = event.GetEventObject();
		if item and (item.m_bitmap and not item.m_bitmap.IsShown()):
			item.m_bitmap.Show();
			# 判断游戏是否结束
			self.checkGameOver(item);

	def checkGameOver(self, item):
		pos = item.m_matrixPos;
		if self.checkCount(pos):
			msgDialog = wx.MessageDialog(self, "游戏结束！", "游戏结束", style = wx.OK|wx.ICON_INFORMATION);
			msgDialog.ShowModal();

	def checkCount(self, pos):
		return False;


if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, size = (700,360));

	panel = wx.Panel(frame);
	panel.SetBackgroundColour("black");
	hr = Banqi(panel, params = {"pos" : (40,40), "size" : (560,280)})
	btn = wx.Button(panel, label = "重新开始");
	# btn.Bind(wx.EVT_BUTTON, hr.restart);
	boxSizer = wx.BoxSizer(wx.HORIZONTAL);
	boxSizer.Add(btn);
	boxSizer.Add(hr);
	panel.SetSizer(boxSizer);

	frame.Show(True);
	app.MainLoop();