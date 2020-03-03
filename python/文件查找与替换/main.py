# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-03 14:41:18
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-03 18:05:35
import os;
import re;

import wx;

defaultLevelCnt = 10;
maxLevelCnt = 21;

class Frame1(wx.Frame):
	"""docstring for Frame1"""
	def __init__(self):
		super(Frame1, self).__init__(None, size = (960,640));
		self.__cfg = {
			"level" : 10,
		};
		self.createContent();
		self.createConfig();
		self.initLayout();

	def initLayout(self):
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.__content);
		box.Add(self.__config);
		self.SetSizerAndFit(box);

	def createContent(self):
		self.__content = wx.Panel(self, size = (640, -1), style = wx.BORDER_THEME);
		title = wx.StaticText(self.__content, label = "文件名称批量查找与替换");
		title.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		dirPath = self.createDirPath();
		opContent = self.createOpContent();
		# 布局
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(title, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(dirPath, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(opContent, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		self.__content.SetSizerAndFit(box);
		pass;

	def createConfig(self):
		self.__config = wx.Panel(self, size = (200, self.GetSize().y), style = wx.BORDER_THEME);
		title = wx.StaticText(self.__config, label = "工具配置");
		title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		cfgContent = self.createCfgContent();
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(title, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(cfgContent, flag = wx.TOP|wx.BOTTOM, border = 5);
		self.__config.SetSizer(box);
		pass;

	def createCfgContent(self):
		cfgContent = wx.Panel(self.__config, size = (self.__config.GetSize().x, -1), style = wx.BORDER_THEME);
		level = self.createLevelCfg(cfgContent);
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(level, flag = wx.TOP|wx.BOTTOM, border = 5);
		cfgContent.SetSizer(box);
		return cfgContent;

	def getConfig(self, key = "", default = None):
		return self.__cfg.get(key, default);

	def createLevelCfg(self, parent):
		level = wx.Panel(parent, size = (parent.GetSize().x, -1));
		title = wx.StaticText(level, label = "遍历层级数：");
		val = wx.StaticText(level, label = str(defaultLevelCnt));
		btn = wx.Button(level, label = "更改", size = (40, 20));
		def onChangeBtn(event):
			ned = wx.NumberEntryDialog(parent, "更改遍历层级数", "请输入数字", "更改配置", int(val.GetLabel()), 1, maxLevelCnt);
			if ned.ShowModal() == wx.ID_OK:
				self.__cfg["level"] = int(ned.GetValue());
				val.SetLabel(str(ned.GetValue()));
		btn.Bind(wx.EVT_BUTTON, onChangeBtn);
		# 布局
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(title, flag = wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, border = 5);
		box.Add(val, flag = wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, border = 5);
		box.Add(btn, flag = wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, border = 5);
		level.SetSizerAndFit(box);
		return level;

	def createDirPath(self):
		dirPath = wx.Panel(self.__content, size = (self.__content.GetSize().x, -1));
		tc = wx.TreeCtrl(dirPath, size = (dirPath.GetSize().x, 20));
		tips = wx.StaticText(dirPath, label = "请输入文件夹路径");
		tips.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		tips.SetForegroundColour("gray");
		# 布局
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(tc, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.EXPAND, border = 5);
		box.Add(tips, flag = wx.ALIGN_CENTER|wx.BOTTOM, border = 5);
		dirPath.SetSizerAndFit(box);
		return dirPath;

	def createOpContent(self):
		opContent = wx.Panel(self.__content, size = (self.__content.GetSize().x, -1), style = wx.BORDER_THEME);
		dirTrees = self.createDirTrees(opContent);
		far = self.createFindAndReplace(opContent);
		# 布局
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(dirTrees);
		box.Add(far);
		opContent.SetSizerAndFit(box);
		return opContent;

	def createDirTrees(self, parent):
		dirTrees = wx.Panel(parent, size = (240, -1), style = wx.BORDER_THEME);
		btn = wx.Button(dirTrees, label = "生成树状图");
		tc = wx.TreeCtrl(dirTrees, size = (dirTrees.GetSize().x, 400), style = wx.TR_HIDE_ROOT|wx.TR_LINES_AT_ROOT|wx.TR_HAS_BUTTONS);
		tc.AddRoot("root");
		# 布局
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(btn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		box.Add(tc, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.EXPAND, border = 5);
		dirTrees.SetSizerAndFit(box);
		# 响应按钮事件
		def onClick(event):
			root = tc.GetRootItem();
			tc.DeleteChildren(root);
			self.updateDirTree(tc, root, os.path.join(os.getcwd(), "..", ".."));
		btn.Bind(wx.EVT_BUTTON, onClick);
		return dirTrees;

	def createFindAndReplace(self, parent):
		far = wx.Panel(parent, size = (parent.GetSize().x - 240, -1), style = wx.BORDER_THEME);
		findIb = self.createInputBtn(far, label = "查找");
		replaceIb = self.createInputBtn(far, label = "替换");
		ctx = wx.TextCtrl(far, size = (far.GetSize().x, 420), style = wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_RICH);
		# 布局
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(findIb, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		box.Add(replaceIb, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		box.Add(ctx, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.EXPAND, border = 5);
		far.SetSizerAndFit(box);
		# 响应按钮事件
		def onClickFindIB(textCtrl):
			ctx.SetValue("");
			self.appendRichTextTo(ctx, "---- 开始查找 ---- \n");
			self.findByDirTree(ctx, os.path.join(os.getcwd(), "..", ".."), findStr = textCtrl.GetValue());
			self.appendRichTextTo(ctx, "---- 结束查找 ---- \n");
		def onClickReplaceIB(textCtrl):
			pass;
		findIb.onClickBtn = onClickFindIB;
		replaceIb.onClickBtn = onClickFindIB;
		return far;

	def createInputBtn(self, parent, label = "按钮文本", onClickBtn = None):
		inputBtn = wx.Panel(parent);
		inputBtn.onClickBtn = onClickBtn;
		textCtrl = wx.TextCtrl(inputBtn, size = (parent.GetSize().x - inputBtn.GetSize().x, -1));
		btn = wx.Button(inputBtn, label = label);
		# 布局
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(textCtrl, flag = wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.EXPAND, border = 5);
		box.Add(btn, flag = wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, border = 5);
		inputBtn.SetSizerAndFit(box);
		# 设置点击事件
		def clickCallback(event):
			if callable(inputBtn.onClickBtn):
				inputBtn.onClickBtn(textCtrl);
			pass;
		btn.Bind(wx.EVT_BUTTON, clickCallback);
		return inputBtn;

	def updateDirTree(self, dirTree, parentItem, dirPath, level = 1):
		if os.path.exists(dirPath) and os.path.isdir(dirPath):
			for file in os.listdir(dirPath):
				item = dirTree.AppendItem(parentItem, file);
				if os.path.isdir(os.path.join(dirPath, file)) and level <= self.getConfig("level", 0):
					self.updateDirTree(dirTree, item, os.path.join(dirPath, file), level = level + 1);
		pass;

	def findByDirTree(self, textCtrl, dirPath, srcPath = "", findStr = "", level = 1):
		if findStr and os.path.exists(dirPath) and os.path.isdir(dirPath):
			if not srcPath:
				srcPath = dirPath;
			for file in os.listdir(dirPath):
				mt = re.match("(.*)("+ findStr +")(.*)", file);
				if mt:
					self.appendRichTextTo(textCtrl, os.path.join(dirPath.replace(srcPath, ""), mt.group(1)), style = "normal");
					self.appendRichTextTo(textCtrl, mt.group(2), style = "bold");
					self.appendRichTextTo(textCtrl, mt.group(3)+"\n", style = "normal");
				# 正则匹配并
				if os.path.isdir(os.path.join(dirPath, file)) and level <= self.getConfig("level", 0):
					self.findByDirTree(textCtrl, os.path.join(dirPath, file), srcPath = srcPath, findStr = findStr, level = level + 1);
		pass;

	def appendRichTextTo(self, textCtrl, text, style = ""):
		attr = None;
		if style == "normal":
			attr = wx.TextAttr(wx.Colour(100, 100, 100), font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		elif style == "bold":
			attr = wx.TextAttr(wx.Colour(0, 0, 0), font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		# 添加富文本
		if attr:
			default = textCtrl.GetDefaultStyle();
			textCtrl.SetDefaultStyle(attr);
			textCtrl.AppendText(text);
			textCtrl.SetDefaultStyle(default);
		else:
			textCtrl.AppendText(text);
		pass;



if __name__ == "__main__":
	app = wx.App()
	frame = Frame1();
	frame.Show();
	app.MainLoop();