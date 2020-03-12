# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-11 14:37:58
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-12 14:33:12

import wx;
import math;
from datetime import datetime, timedelta;
import threading;
from threadEx import stopThread;

from PIL import ImageGrab

import numpy as np

import cv2

from GrabDialog import GrabDialog;

class SRControler(wx.Dialog):
	def __init__(self, countdown = 0, frame = 30, bbox = None):
		wx.Dialog.__init__(self, None, style=wx.NO_BORDER|wx.STAY_ON_TOP);
		self.__frame = frame;
		self.__bbox = bbox;
		self.createVideo();
		self.__countdown = countdown;
		self.__startTime = None;
		self.__pauseTime = None;
		# self.__lastRecordTime = None;
		self.__isPlaying = True;
		btn = self.createBtnPanel();
		self.__label = wx.StaticText(self, label = f"--:--:--");
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(btn, flag = wx.ALIGN_CENTER);
		box.Add(self.__label, flag = wx.ALIGN_CENTER);
		self.SetSizerAndFit(box);
		# 设置定时器
		self.__timer = wx.Timer(self);
		self.Bind(wx.EVT_TIMER, self.onTimer, self.__timer);
		wx.CallAfter(self.onStart);
		# # 设置定时器
		# self.__recordTimer = wx.Timer(self);
		# self.Bind(wx.EVT_TIMER, self.onRecordVideo, self.__recordTimer);
		self.recordThread = None;

	def createBtnPanel(self):
		btnPanel = wx.Panel(self);
		self.__startPause = wx.Button(btnPanel, label = "暂停", size = (50, 30));
		self.__startPause.SetForegroundColour(wx.Colour(68, 68, 68));
		self.__stop = wx.Button(btnPanel, label = "停止", size = (50, 30));
		self.__stop.SetForegroundColour("red");
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.__startPause, flag = wx.ALIGN_CENTER);
		box.Add(self.__stop, flag = wx.ALIGN_CENTER);
		btnPanel.SetSizerAndFit(box);
		# 绑定事件
		self.__startPause.Bind(wx.EVT_BUTTON, self.onStartPause);
		self.__stop.Bind(wx.EVT_BUTTON, self.onStop);
		return btnPanel;

	def onTimer(self, event = None):
		if self.__countdown > 0:
			self.__label.SetLabel(f"{self.__countdown}秒后开始");
			self.__countdown -= 1;
		else:
			if not self.__startTime:
				self.__startTime = datetime.now();
				self.__label.SetLabel("00:00:00");
				self.recordVideo();
			else:
				diffDataTime = datetime.now() - self.__startTime;
				days, diffSeconds = diffDataTime.days, diffDataTime.seconds;
				hours = math.floor(diffSeconds / (60 * 60)) % 24;
				minutes = math.floor(diffSeconds / 60) % 60;
				seconds = diffSeconds % 60;
				if days > 0:
					self.__label.SetLabel(f"{days}D " + ":".join(["%02d"%hours, "%02d"%minutes, "%02d"%seconds]));
				else:
					self.__label.SetLabel(":".join(["%02d"%hours, "%02d"%minutes, "%02d"%seconds]));
		pass;

	def onStartPause(self, event):
		if self.__isPlaying:
			self.onPause();
		else:
			self.onStart();
		pass;

	def onStop(self, event):
		self.onPause();
		self.__video.release();
		self.EndModal(wx.ID_OK);
		pass;

	def onStart(self):
		self.__startPause.SetLabel("暂停");
		self.__isPlaying = True;
		if self.__pauseTime:
			self.__startTime += datetime.now() - self.__pauseTime;
		self.onTimer();
		if not self.__timer.IsRunning():
			self.__timer.Start(100);
		# 继续录屏
		if self.__countdown <= 0:
			self.recordVideo();
		pass;

	def onPause(self):
		self.__startPause.SetLabel("继续");
		if self.__timer.IsRunning():
			self.__timer.Stop();
		# if self.__recordTimer.IsRunning():
		# 	self.__recordTimer.Stop();
		self.__pauseTime = datetime.now();
		self.__isPlaying = False;
		if self.recordThread:
			stopThread(self.recordThread);
		pass;

	def createVideo(self):
		if self.__bbox:
			ig = ImageGrab.grab(self.__bbox);
		else:
			ig = ImageGrab.grab();
		fourcc = cv2.VideoWriter_fourcc(*'MJPG'); #编码格式
		self.__video = cv2.VideoWriter('test.avi', fourcc, self.__frame, ig.size); #输出文件命名为test.avi,帧率为self.__frame

	def recordVideo(self):
		# if not self.__lastRecordTime:
		# 	self.__lastRecordTime = datetime.now();
		# elif self.__pauseTime:
		# 	self.__lastRecordTime += datetime.now() - self.__pauseTime;
		if self.recordThread:
			stopThread(self.recordThread);
		self.recordThread = threading.Thread(target = self.onRecordVideo);
		self.recordThread.start();
		# if not self.__recordTimer.IsRunning():
		# 	self.__recordTimer.Start(int(1000/self.__frame));
		pass;

	def onRecordVideo(self, event = None):
		while self.__isPlaying:
			# diffTime = datetime.now() - self.__lastRecordTime;
			# if diffTime.microseconds < 1000000/self.__frame:
			# 	wx.CallLater(1,self.onRecordVideo);
			# 	return;
			if self.__bbox:
				ig = ImageGrab.grab(self.__bbox);
			else:
				ig = ImageGrab.grab();
			im=cv2.cvtColor(np.array(ig), cv2.COLOR_RGB2BGR); # 转为opencv的BGR格式
			self.__video.write(im);
			self.__video.write(im);
			# wx.CallLater(1,self.onRecordVideo);
			# self.__lastRecordTime = self.__lastRecordTime + timedelta(microseconds = int(1000000/self.__frame));
		pass;



class Frame1(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(960,640));

		btn1 = wx.Button(self,label=u"全屏录制",pos=(280, 400),size=(100,45))
		self.Bind(wx.EVT_BUTTON,self.rsFull,btn1);

		btn2 = wx.Button(self,label=u"选择区域录制",pos=(430, 400),size=(100,45))
		self.Bind(wx.EVT_BUTTON,self.rsRect,btn2);

	def rsFull(self, event):
		self.Hide();
		src = SRControler();
		src.ShowModal();
		self.Show();

	def rsRect(self, event):
		self.Hide();
		gd = GrabDialog();
		ret = gd.ShowModal();
		rect = gd.getScreenshotRect();
		gd.Destroy();
		if ret == wx.ID_OK:
			src = SRControler(bbox = (rect.x, rect.y, rect.width, rect.height));
			src.ShowModal();
		self.Show();



if __name__ == "__main__":
	app = wx.App();
	frame1 = Frame1();
	frame1.Show();
	app.MainLoop()