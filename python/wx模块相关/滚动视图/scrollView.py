# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-11-08 17:00:50
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-11-08 17:25:24

import wx

class MyFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, pos=(640,0))

		panel = wx.Panel(self, size = (400,400))
		panel.SetBackgroundColour("black")

		self.scroller = wx.ScrolledWindow(panel, -1, size = (300,300))
		self.scroller.SetBackgroundColour("red")
		self.scroller.SetScrollbars(0, 0, 200, 900)

		pnl = wx.Panel(self.scroller, pos = (100,100))
		pnl.SetBackgroundColour("green")
		pnl.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
		self.SetMinSize((500,640))
		box = wx.BoxSizer(wx.VERTICAL)
		box.Add(panel, wx.EXPAND)
		self.SetSizer(box)


	def onLeftDown(self, event):
		# print("0000000000000")
		self.scroller.SetScrollbars(1, 1, 400, 900)

if __name__ == '__main__':
	app = wx.App(redirect=False)
	frame = MyFrame(None, -1, u'测试')
	frame.Show(True)
	app.MainLoop()