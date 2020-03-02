# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-02 17:21:19
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-02 18:10:16
import os;

import wx;

from enum import Enum, unique;

@unique
class AdjustType(Enum):
	UNKNOW	  = 0;
	LEFT		= 1;
	TOPLEFT	 = 2;
	TOP		 = 3;
	TOPRIGHT	= 4;
	RIGHT	   = 5;
	BOTTOMRIGHT = 6;
	BOTTOM	  = 7;
	BOTTOMLEFT  = 8;
	INSIDE	  = 9;

# 鼠标图标配置
cursorConfig = {
	AdjustType.UNKNOW : wx.CURSOR_ARROW,
	AdjustType.LEFT : wx.CURSOR_SIZEWE,
	AdjustType.TOPLEFT : wx.CURSOR_SIZENWSE,
	AdjustType.TOP : wx.CURSOR_SIZENS,
	AdjustType.TOPRIGHT : wx.CURSOR_SIZENESW,
	AdjustType.RIGHT : wx.CURSOR_SIZEWE,
	AdjustType.BOTTOMRIGHT : wx.CURSOR_SIZENWSE,
	AdjustType.BOTTOM : wx.CURSOR_SIZENS,
	AdjustType.BOTTOMLEFT : wx.CURSOR_SIZENESW,
	AdjustType.INSIDE : wx.CURSOR_SIZING,
};

# 文件格式配置
fileFormatCfg = {
	".png" : wx.BITMAP_TYPE_PNG,
	".jpg" : wx.BITMAP_TYPE_JPEG,
	".bmp" : wx.BITMAP_TYPE_BMP,
	".tif" : wx.BITMAP_TYPE_TIF,
}

class ScreenshotDialog(wx.Dialog):
	"""docstring for ScreenshotDialog"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(ScreenshotDialog, self).__init__(None, title = "截屏", pos = (0, 0), size = wx.GetDisplaySize(), style = wx.NO_BORDER|wx.STAY_ON_TOP);
		self._className_ = ScreenshotDialog.__name__;
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件
		# 绑定事件
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM);
		self.Bind(wx.EVT_PAINT, self.onPaint);
		self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown);
		self.Bind(wx.EVT_LEFT_UP, self.onLeftUp);
		self.Bind(wx.EVT_MOTION, self.onMove);
		self.Bind(wx.EVT_RIGHT_UP, self.onRightUp);
		# 初始化属性
		self.__grabBmp = self.getScreenBmp();
		self.__firstPoint = wx.Point(0, 0);
		self.__lastPoint = wx.Point(0, 0);
		self.__preAdjustPoint = wx.Point(0, 0);
		self.__downing = False;
		self.__adjusting = False;
		self.__adjustType = AdjustType.UNKNOW;
		self.__menu = None;

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "截屏",
			"size" : wx.GetDisplaySize(),
			"style" : wx.NO_BORDER|wx.STAY_ON_TOP,
		};
		for k,v in params.items():
			self.__params[k] = v;

	# 重置选中区域
	def resetSelectedArea(self):
		self.updateFirstAndLastPoint(wx.Rect(0, 0, 1, 1));
		self.updateDCRect();
		self.SetCursor(wx.Cursor(wx.CURSOR_ARROW)); # 重置鼠标图标
		self.__adjusting = False;
		
	# 全屏选中区域
	def fullScreenSelectedArea(self):
		self.updateFirstAndLastPoint(wx.Rect(0, 0, self.__grabBmp.GetWidth(), self.__grabBmp.GetHeight()));
		self.updateDCRect();
	
	def onPaint(self, event = None):
		dc = wx.GCDC(wx.BufferedPaintDC(self));
		rect = self.GetClientRect();
		color = wx.Colour(0, 0, 0, 120);
		
		# 设置绘制截图区域时矩形的点
		minX, minY = min(self.__firstPoint.x, self.__lastPoint.x), min(self.__firstPoint.y, self.__lastPoint.y);
		maxX, maxY = max(self.__firstPoint.x, self.__lastPoint.x), max(self.__firstPoint.y, self.__lastPoint.y);
		
		# 画出整个屏幕的截图
		dc.DrawBitmap(self.__grabBmp, 0, 0);

		#画出阴影部分（截取的部分不需要画）
		dc.SetPen(wx.Pen(color));
		dc.SetBrush(wx.Brush(color));
		dc.DrawRectangle(0, 0, rect.width, minY);
		dc.DrawRectangle(0, minY, minX, maxY - minY);
		dc.DrawRectangle(maxX, minY, rect.width - maxX, maxY - minY);
		dc.DrawRectangle(0, maxY, rect.width, rect.height);

		if self.__downing:
			# 画出截图区域的边框
			dc.SetPen(wx.Pen(wx.Colour(0, 150, 0)));
			dc.SetBrush(wx.Brush(color, wx.TRANSPARENT));
			dc.DrawRectangle(minX, minY, maxX - minX, maxY - minY);
			# 显示角和边中点
			dc.SetBrush(wx.Brush(wx.Colour(255,0,0)));
			dc.DrawRectangleList([
				(minX - 2, minY - 2, 5, 5),
				(maxX / 2 + minX / 2 - 2, minY - 2, 5, 5),
				(maxX - 2, minY - 2, 5, 5),
				(maxX - 2, maxY / 2 + minY / 2 - 2, 5, 5),
				(maxX - 2, maxY - 2, 5, 5),
				(maxX / 2 + minX / 2 - 2, maxY - 2, 5, 5),
				(minX - 2, maxY - 2, 5, 5),
				(minX - 2, maxY / 2 + minY / 2 - 2, 5, 5)
			]);
			# 显示信息
			w, h = 140, 54;
			color = wx.Colour(0,0,0,180);
			dc.SetPen(wx.Pen(color));
			dc.SetBrush(wx.Brush(color, wx.SOLID));
			text = "区域大小：("+str(maxX - minX)+","+str(maxY - minY)+")";
			text += "\n鼠标位置：("+str(self.__lastPoint.x)+","+str(self.__lastPoint.y)+")";
			posY = minY-h-5;
			if posY < 0:
				posY = minY + 5;
			dc.DrawRectangle(minX, posY, w, h);
			dc.SetTextForeground(wx.Colour(255,255,255));
			dc.DrawText(text, minX+5, posY+5);
			dc.SetTextForeground(wx.Colour(160,160,160));
			dc.DrawText("[右键选中区域显示菜单]", minX+5, posY+h-18);
	pass;

	def onLeftDown(self, event):
		if self.__downing:
			return;
		self.__downing = True;
		if self.__adjusting:
			self.__preAdjustPoint = event.GetPosition();
		else:
			self.__firstPoint = event.GetPosition();
			self.__lastPoint = event.GetPosition();

	def onLeftUp(self, event):
		if self.__downing:
			if not self.__adjusting:
				self.__lastPoint = event.GetPosition();
				if not self.verifyScreenshotRect():
					self.__firstPoint = wx.Point(0, 0);
					self.__lastPoint = wx.Point(self.__grabBmp.GetWidth(), self.__grabBmp.GetHeight());
			# 确保firstPoint一直在lastPoint的左上方向
			self.updateFirstAndLastPoint();
			# 更新DC
			self.updateDCRect();
			# 更新标记
			self.__downing = False;
			self.__adjusting = True;
	
	def onRightUp(self, event):
		rect = self.getScreenshotRect();
		if rect.Contains(event.GetPosition()):
			self.onPopupMenu(event.GetPosition());
		else:
			if self.verifyScreenshotRect():
				self.resetSelectedArea();
			else:
				self.Close();
		pass;
	
	def onMove(self, event):
		pos = event.GetPosition();
		if self.__adjusting:
			if self.__downing:
				if self.__adjustType == AdjustType.LEFT:
					self.__firstPoint = wx.Point(pos.x, self.__firstPoint.y);
				elif self.__adjustType == AdjustType.TOPLEFT:
					self.__firstPoint = pos;
				elif self.__adjustType == AdjustType.TOP:
					self.__firstPoint = wx.Point(self.__firstPoint.x, pos.y);
				elif self.__adjustType == AdjustType.TOPRIGHT:
					self.__firstPoint = wx.Point(self.__firstPoint.x, pos.y);
					self.__lastPoint = wx.Point(pos.x, self.__lastPoint.y);
				elif self.__adjustType == AdjustType.RIGHT:
					self.__lastPoint = wx.Point(pos.x, self.__lastPoint.y);
				elif self.__adjustType == AdjustType.BOTTOMRIGHT:
					self.__lastPoint = pos;
				elif self.__adjustType == AdjustType.BOTTOM:
					self.__lastPoint = wx.Point(self.__lastPoint.x, pos.y);
				elif self.__adjustType == AdjustType.BOTTOMLEFT:
					self.__firstPoint = wx.Point(pos.x, self.__firstPoint.y);
					self.__lastPoint = wx.Point(self.__lastPoint.x, pos.y);
				elif self.__adjustType == AdjustType.INSIDE:
					rect = self.getScreenshotRect();
					rect.Offset(pos - self.__preAdjustPoint);
					self.updateFirstAndLastPoint(rect);
				self.updateDCRect();
				self.__preAdjustPoint = pos;
			else:
				self.__adjustType = self.getAdjustType(pos);
				cs = wx.Cursor(cursorConfig.get(self.__adjustType, wx.CURSOR_ARROW));
				if self.GetCursor().GetHandle() != cs.GetHandle():
					self.SetCursor(cs);
		elif self.__downing:
			self.__lastPoint = pos;
			self.updateDCRect();
	
	def getScreenshotRect(self):
		return wx.Rect(
			min(self.__firstPoint.x, self.__lastPoint.x),
			min(self.__firstPoint.y, self.__lastPoint.y),
			abs(self.__firstPoint.x - self.__lastPoint.x),
			abs(self.__firstPoint.y - self.__lastPoint.y)
		);
	
	def verifyScreenshotRect(self, errVal = 5):
		if abs(self.__firstPoint.x - self.__lastPoint.x) <= errVal or abs(self.__firstPoint.y - self.__lastPoint.y) <= errVal:
			return False;
		return True;
	
	def updateFirstAndLastPoint(self, rect = None):
		if not rect:
			rect = self.getScreenshotRect();
		self.__firstPoint = wx.Point(rect.x, rect.y);
		self.__lastPoint = wx.Point(rect.x + rect.width, rect.y + rect.height);
		pass;
	
	def updateDCRect(self):
		self.RefreshRect(self.GetClientRect(), True);
		self.Update();
	
	def getAdjustType(self, pos):
		rect = self.getScreenshotRect();
		adjustTypeMap = {
			AdjustType.LEFT : wx.Point(rect.GetLeft(), rect.GetBottom()/2 + rect.GetTop()/2),
			AdjustType.TOPLEFT : rect.GetTopLeft(),
			AdjustType.TOP : wx.Point(rect.GetLeft()/2 + rect.GetRight()/2, rect.GetTop()),
			AdjustType.TOPRIGHT : rect.GetTopRight(),
			AdjustType.RIGHT : wx.Point(rect.GetRight(), rect.GetBottom()/2 + rect.GetTop()/2),
			AdjustType.BOTTOMRIGHT : rect.GetBottomRight(),
			AdjustType.BOTTOM : wx.Point(rect.GetLeft()/2 + rect.GetRight()/2, rect.GetBottom()),
			AdjustType.BOTTOMLEFT : rect.GetBottomLeft(),
		};
		for k,v in adjustTypeMap.items():
			diff = pos - v;
			if abs(diff.x) <= 2 and abs(diff.y) <= 2:
				return k;
		if rect.Contains(pos):
			return AdjustType.INSIDE;
		return AdjustType.UNKNOW;

	def getScreenBmp(self):
		ds = wx.GetDisplaySize();
		bmp = wx.Bitmap(ds.x, ds.y);
		mdc = wx.MemoryDC();
		mdc.SelectObject(bmp);
		mdc.Blit(0, 0, ds.x, ds.y, wx.ScreenDC(), 0, 0)
		mdc.SelectObject(wx.NullBitmap);
		return bmp

	def saveAs(self, filePath, fileType):
		bmp = self.__grabBmp.GetSubBitmap(self.getScreenshotRect());
		if bmp.SaveFile(filePath, fileType):
			self.EndModal(wx.ID_OK);
			if self.showMessageDialog(f"保存截屏图片（{filePath}）成功，是否打开其所在文件夹？", "保存截屏图片", style = wx.YES_NO|wx.ICON_QUESTION) == wx.ID_YES:
				os.system("explorer " + os.path.abspath(os.path.dirname(filePath)));
		else:
			self.showMessageDialog(f"保存截屏图片（{filePath}）失败！", "保存截屏图片", style = wx.OK|wx.ICON_ERROR);
		pass;

	def showMessageDialog(self, message, caption = "提示", style = wx.OK):
		return wx.MessageDialog(self, message, caption = caption, style = style).ShowModal();

	def onPopupMenu(self, pos):
		if self.__menu == None:
			self.createMenu(); # 创建菜单
		self.PopupMenu(self.__menu, pos);
		pass;

	def createMenu(self):
		self.__menu = SSMenu(data = [
			{
				"title" : "保存",
				"callback" : self.onSave,
			},
			{
				"isSeparator" : True,
			},
			{
				"title" : "全屏截图",
				"callback" : self.onFullScreen,
			},
			{
				"isSeparator" : True,
			},
			{
				"title" : "取消",
				"callback" : self.onCancel,
			},
		]);

	def onSave(self, event):
		dlg = wx.FileDialog(self, "保存截屏图片", defaultFile = "screenshot", wildcard = "PNG files (.png)|.png|JPEG files (.jpg)|.jpg|BMP files (.bmp)|.bmp|TIF files (.tif)|.tif", style=wx.FD_SAVE);
		if dlg.ShowModal() == wx.ID_OK:
			filePath = dlg.GetPath();
			_, ext = os.path.splitext(filePath);
			if ext in fileFormatCfg:
				self.saveAs(filePath, fileFormatCfg[ext]);
			else:
				self.showMessageDialog(f"保存截屏图片（{filePath}）文件格式错误！", "保存截屏图片", style = wx.OK|wx.ICON_ERROR);
		pass;
	
	def onFullScreen(self, event):
		self.fullScreenSelectedArea();
	
	def onCancel(self, event):
		self.resetSelectedArea();


# 弹出菜单
class SSMenu(wx.Menu):
	"""docstring for SSMenu"""
	def __init__(self, data = []):
		super(SSMenu, self).__init__();
		self.appendMenu(data);

	def appendMenu(self, data = []):
		for itemData in data:
			if "isSeparator" in itemData and itemData["isSeparator"] == True:
				self.appendItem("separator");
			else:
				itemId = None;
				params = {};
				if "itemId" in itemData:
					itemId = itemData["itemId"];
				if "params" in itemData:
					params = itemData["params"];
				self.appendItem("normal", itemData["title"], itemData["callback"], itemId = itemId, params = params);
		pass;

	def appendItem(self, menuType = "", title = "", callback = None, itemId = -1, params = {}):
		if menuType == "normal":
			if not itemId:
				itemId = wx.NewId();
			menuItem = wx.MenuItem(self, itemId, title, **params);
			self.Bind(wx.EVT_MENU, callback, menuItem);
		elif menuType == "separator":
			menuItem = wx.MenuItem(self, wx.NewId(), kind = wx.ITEM_SEPARATOR);
		self.Append(menuItem);
		return menuItem;


# 窗口
class SSFrame(wx.Frame):
	"""docstring for SSFrame"""
	def __init__(self):
		super(SSFrame, self).__init__(None, size = (960,640));
		panel = wx.Panel(self, size = (960,640));
		btn1 = wx.Button(panel, label = "直接截屏", pos=(430,300), size=(100,40));
		btn2 = wx.Button(panel, label = "隐藏窗口后截屏", pos=(430,300), size=(100,40));

		self.Bind(wx.EVT_BUTTON, self.screenshot, btn1);
		self.Bind(wx.EVT_BUTTON, self.hideToScreenshot, btn2);

		box = wx.BoxSizer(wx.VERTICAL)
		box.Add(btn1, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(btn2, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		panel.SetSizer(box);

	def __screenshot__(self):
		ss = ScreenshotDialog(None);
		ss.ShowModal();
		ss.Destroy();
		if not self.IsShown():
			self.Show();
		pass;

	def screenshot(self, event = None):
		wx.CallLater(300, self.__screenshot__);

	def hideToScreenshot(self, event = None):
		self.Hide();
		self.screenshot();
		pass;


if __name__ == "__main__":
	app = wx.App()
	frame = SSFrame();
	frame.Show();
	app.MainLoop();