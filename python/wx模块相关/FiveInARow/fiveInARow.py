# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-25 10:31:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-12-26 11:26:53
import wx;

class FiveInARow(wx.Panel):
	"""docstring for FiveInARow"""
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(FiveInARow, self).__init__(parent, id, pos = self.params_["pos"], size = self.params_["size"], style = self.params_["style"]);
		self.m_gridViews = [];
		self.m_curItem = None;
		self.m_toggle = 0;
		self.SetBackgroundColour(self.params_["bgColour"]);
		self.initView();

	def initParams(self, params):
		self.params_ = {
			"pos" : (0,0),
			"size" : (360,360),
			"style" : wx.BORDER_THEME,
			"bgColour" : wx.Colour(238,168,37),
			"focusColour" : wx.Colour(240,200,37),
			"matrix" : (18,18),
		};
		for k,v in params.items():
			self.params_[k] = v;

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
		self.m_gridViews = [];
		gridViewSide = min(self.params_["size"][0]/self.params_["matrix"][0], self.params_["size"][1]/self.params_["matrix"][1]);
		for i in range(self.params_["matrix"][0]):
			for j in range(self.params_["matrix"][1]):
				gridView = wx.Panel(self, size = (gridViewSide, gridViewSide), style = wx.BORDER_THEME);
				gridView.m_matrixPos = wx.Point(i,j);
				gridView.m_flag = -1;
				gridView.Bind(wx.EVT_LEFT_DOWN, self.onItemClick);
				gridView.Bind(wx.EVT_LEFT_DCLICK, self.onItemDClick);
				self.m_gridViews.append(gridView);

	def onItemClick(self, event = None, item = None):
		if not item and event:
			item = event.GetEventObject();
		if item:
			item.SetBackgroundColour(self.params_["focusColour"]);
			item.Refresh();
			# 重置self.m_curItem
			if self.m_curItem:
				self.m_curItem.SetBackgroundColour(self.params_["bgColour"]);
				self.m_curItem.Refresh();
			self.m_curItem = item;
		pass;

	def onItemDClick(self, event = None, item = None):
		if not item and event:
			item = event.GetEventObject();
		if item:
			self.m_toggle = (self.m_toggle + 1) % 2;
			colour = self.m_toggle == 0 and "white" or "black";
			item.SetBackgroundColour(colour);
			item.Refresh();
			item.m_flag = self.m_toggle;
			# 重置self.m_curItem
			if self.m_curItem == item:
				self.m_curItem = None;
			# 判断游戏是否结束
			self.checkGameOver(item);

	def checkGameOver(self, item):
		pos = item.m_matrixPos;
		flag = item.m_flag;
		if self.checkCount(pos, flag):
			msgDialog = wx.MessageDialog(self, "游戏结束！", "游戏结束", style = wx.OK|wx.ICON_INFORMATION);
			msgDialog.ShowModal();

	def checkCount(self, pos, flag, count = 5):
		rows = self.params_["matrix"][0];
		cols = self.params_["matrix"][1];
		minX = max(pos.x - 4, 0);
		maxX = min(pos.x + 4, rows-1);
		minY = max(pos.y - 4, 0);
		maxY = min(pos.y + 4, cols-1);
		# 校验横向
		count = 0;
		for i in range(minX, maxX+1):
			gridView = self.m_gridViews[i*cols + pos.y];
			if gridView.m_flag == flag:
				count += 1;
				if count == 5:
					return True;
			else:
				count = 0;
		# 校验竖向
		count = 0;
		for j in range(minY, maxY+1):
			gridView = self.m_gridViews[pos.x*cols + j];
			if gridView.m_flag == flag:
				count += 1;
				if count == 5:
					return True;
			else:
				count = 0;
		# 校验斜向
		startIdx, endIdx = max(minX - pos.x, minY - pos.y), min(maxX - pos.x, maxY - pos.y);
		idxList = range(startIdx, endIdx+1);
		countList = [0,0];
		for k in range(0, len(idxList)):
			# 右斜向
			gridView = self.m_gridViews[(pos.x + idxList[k])*cols + pos.y + idxList[k]];
			if gridView.m_flag == flag:
				countList[0] += 1;
				if countList[0] == 5:
					return True;
			else:
				countList[0] = 0;
			# 左斜向
			if pos.y - idxList[k] >= 0 and pos.y - idxList[k] < cols:
				gridView = self.m_gridViews[(pos.x + idxList[k])*cols + pos.y - idxList[k]];
				if gridView.m_flag == flag:
					countList[1] += 1;
					if countList[1] == 5:
						return True;
				else:
					countList[1] = 0;
		return False;



if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, size = (700,600));

	panel = wx.Panel(frame);
	panel.SetBackgroundColour("black");
	hr = FiveInARow(panel, params = {"pos" : (40,40), "size" : (540,540)})
	btn = wx.Button(panel, label = "重新开始");
	# btn.Bind(wx.EVT_BUTTON, hr.restart);
	boxSizer = wx.BoxSizer(wx.HORIZONTAL);
	boxSizer.Add(btn);
	boxSizer.Add(hr);
	panel.SetSizer(boxSizer);

	frame.Show(True);
	app.MainLoop();