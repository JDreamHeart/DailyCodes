# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-10-27 15:47:32
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-04 15:12:42

import wx;

class DirInputView(wx.Panel):
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(DirInputView, self).__init__(parent, id, size = self.params["size"]);
		self.createControls();
		self.initViewLayout();

	def initParams(self, params):
		# 初始化参数
		self.params = {
			"size" : (-1,-1),
			"inputSize" : (-1,20),
			"buttonSize" : (30,20),
			"buttonLabel" : "选择",
			"onInput" : None,
		};
		for k,v in params.items():
			self.params[k] = v;

	def createControls(self):
		self.createInput();
		self.createButton();
		pass;

	def initViewLayout(self):
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.__input, proportion = 1);
		box.Add(self.__button, proportion = 0);
		self.SetSizerAndFit(box);

	def createInput(self):
		self.__input = wx.TextCtrl(self, -1, "", size = self.params["inputSize"]);
		def onKillFocus(event):
			self.setInputValue(self.__input.GetValue());
			event.Skip();
		self.__input.Bind(wx.EVT_KILL_FOCUS, onKillFocus);

	def createButton(self):
		self.__button = wx.Button(self, -1, self.params["buttonLabel"], size = self.params["buttonSize"]);
		self.__button.Bind(wx.EVT_BUTTON, self.onClickButton)

	def onClickButton(self, event):
		dirVal = wx.DirSelector();
		if dirVal != "":
			self.setInputValue(dirVal);

	def getInputValue(self):
		return self.__input.GetValue();

	def setInputValue(self, value):
		if callable(self.params["onInput"]):
			return self.params["onInput"](value, self.__input.SetValue);
		return self.__input.SetValue(value);

	def resetInputValue(self):
		return self.__input.SetValue("");