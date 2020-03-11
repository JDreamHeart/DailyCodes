# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-11 14:30:54
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-11 14:31:43
import wx;

class Frame1(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(960,640));
		pass;


if __name__ == "__main__":
	app = wx.App();
	frame1 = Frame1();
	frame1.Show();
	app.MainLoop()