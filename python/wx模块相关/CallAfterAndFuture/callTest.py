# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-10 10:59:57
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-12-10 12:03:21

import wx;
import time;
import threading

def onBtn(event):
	print("00000")
	wx.CallAfter(printStr, "123")
	time.sleep(1)
	onBtn2()

def onBtn2(event = None):
	print("33333")
	wx.CallAfter(printStr, "789")
	time.sleep(1)
	print("44444")

def printStr(key = ""):
	print("11111" + key)

def doFunc():
	i = 0;
	while i < 10:
		print(i);
		i += 1;
		yield;

def callPrintStr(key = ""):
	print("call ====");
	printStr(key)


if __name__ == '__main__':
	# app = wx.App();
	# frame = wx.Frame(None, size = (400,400))
	# btn = wx.Button(frame, label = "fff");
	# btn.Bind(wx.EVT_BUTTON, onBtn);
	# frame.Show();
	# app.MainLoop();
	# for i in doFunc():
	# 	# print(i)
	# 	pass;

	thr = threading.Thread(target = callPrintStr, args = ("ttt",))
	thr.start();