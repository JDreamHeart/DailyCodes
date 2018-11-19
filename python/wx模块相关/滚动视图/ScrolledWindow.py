# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-11-08 17:00:50
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-11-08 23:56:59

import wx

class ScrolledWindow(wx.ScrolledWindow):
	"""docstring for ScrolledWindow"""
	def __init__(self, parent, id = -1, params = {}, contentView = None):
		self.initParams(params);
		super(ScrolledWindow, self).__init__(parent, id, size = self.params_["size"]);
		self.setContentView(contentView);
		
	def initParams(self, params):
		# 初始化参数
		self.params_ = {
			"size" : (0,0),
		};
		for k,v in params.items():
			self.params_[k] = v;

	def setContentView(self, contentView):
		if contentView:
			# 销毁原有内容节点
			if hasattr(self, "contentView"):
				self.contentView.Destroy();
			# 重置父节点
			if contentView.Parent != self:
				contentView.Reparent(self);
			# 重置self.contentView
			self.contentView = contentView;
			# 调整滚动条
			self.adjustScrollbars();
			# 初始化事件
			self.initContentViewEvents();

	def adjustScrollbars(self, event = None):
		contentSize = self.contentView.GetSize();
		self.SetScrollbars(1, 1, contentSize[0], contentSize[1]);

	def initContentViewEvents(self):
		if hasattr(self, "contentView"):
			self.contentView.Bind(wx.EVT_SIZE, self.adjustScrollbars);


class MyFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, pos=(640,0))

		panel = wx.Panel(self, size = (400,400))
		panel.SetBackgroundColour("black")

		pnl = wx.Panel(self, pos = (100,100), size = (100,100))
		pnl.SetBackgroundColour("green")
		pnl.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
		self.pnl = pnl

		self.scroller = ScrolledWindow(panel, params = {"size" : (300,300)}, contentView = pnl)


		self.SetMinSize((500,640))
		box = wx.BoxSizer(wx.VERTICAL)
		box.Add(panel, wx.EXPAND)
		self.SetSizer(box)


	def onLeftDown(self, event):
		self.pnl.SetSize((400,600))

if __name__ == '__main__':
	app = wx.App(redirect=False)
	frame = MyFrame(None, -1, u'测试')
	frame.Show(True)
	app.MainLoop()