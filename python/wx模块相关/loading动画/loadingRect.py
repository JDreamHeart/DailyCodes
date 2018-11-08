# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-11-08 12:13:55
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-11-08 14:22:37

import wx;

global gridSizerList
global curIdx;

def updateBgColor(lastIdx = None):
	global gridSizerList;
	global curIdx;
	gridSizerList[curIdx].SetBackgroundColour("red")
	gridSizerList[curIdx].Refresh()
	if lastIdx != None :
		gridSizerList[lastIdx].SetBackgroundColour("green")
		gridSizerList[lastIdx].Refresh()

def onTimer(event):
	global curIdx;
	try:
		lastIdx = curIdx;
		curIdx = (curIdx + 1) % len(gridSizerList);
		updateBgColor(lastIdx);
	except Exception as e:
		print(e)
		curIdx = 0;

def main(app, frame):
	global gridSizerList;
	global curIdx;
	gridSizerList = [];
	curIdx = 0;
	panel = wx.Panel(frame)
	gridSizer = wx.GridSizer(1, 6, 3, 3)
	for i in range(0, 6):
		p = wx.Panel(panel, size = (40,30))
		p.SetBackgroundColour("green")
		gridSizer.Add(p, flag = wx.LEFT, border = 10)
		gridSizerList.append(p)
	panel.SetSizer(gridSizer)
	box = wx.BoxSizer()
	box.Add(panel, flag = wx.TOP, border = 100)
	frame.SetSizer(box)
	# 创建定时器
	panel.timer = wx.Timer(panel)
	panel.Bind(wx.EVT_TIMER, onTimer, panel.timer);
	panel.timer.Start(80)
	updateBgColor()

if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, size = (400,400))
	main(app, frame)
	frame.Show()
	app.MainLoop()