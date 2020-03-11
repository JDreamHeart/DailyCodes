# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-05 17:10:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-11 15:10:21

import wx;

from PIL import ImageGrab

import numpy as np

import cv2

from GrabDialog import GrabDialog;

# import imageio

def recordScreen(bbox = []):
	if bbox:
		p = ImageGrab.grab(bbox)
	else:
		p = ImageGrab.grab()#获得当前屏幕

	k=np.zeros((200,200),np.uint8)

	a,b=p.size#获得当前屏幕的大小

	fourcc = cv2.VideoWriter_fourcc(*'MJPG')#编码格式

	video = cv2.VideoWriter('test.avi', fourcc, 16, (a, b))#输出文件命名为test.avi,帧率为16，可以自己设置

	buff=[]

	i=64
	while i>0:
		im = ImageGrab.grab()
		imm=cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)#转为opencv的BGR格式     video.write(imm)
		# cv2.imshow("test", imm)
		video.write(imm)
		buff.append(imm)
		if cv2.waitKey(16) & 0xFF == ord('q'):
			break
		i-=1;
	video.release()
	# imageio.mimsave('test.gif',buff,'GIF',duration=0.1)
	# buff[0].save("test.gif", save_all=True, append_images=buff, duration=4)
	cv2.destroyAllWindows()


class Frame1(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(960,640), style=wx.STAY_ON_TOP);
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.Bind(wx.EVT_PAINT, self.onPaint);
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)

		btn = wx.Button(self,label=u"透明",pos=(480, 320),size=(100,45))
		self.Bind(wx.EVT_BUTTON,self.onTrans,btn);

		btn1 = wx.Button(self,label=u"关闭",pos=(480, 400),size=(100,45))
		self.Bind(wx.EVT_BUTTON,self.onClose,btn1);

	def onEraseBackground(self, event):
		pass;

	def onTrans(self, event):
		self.SetTransparent(1) #设置透明
		# recordScreen();

	def onClose(self, event):
		self.Destroy();

	def onPaint(self, event):
		dc = wx.GCDC(wx.PaintDC(self));
		dc.SetBackground(wx.TRANSPARENT_BRUSH);
		dc.Clear()
		rect = self.GetClientRect();
		color = wx.Colour(0, 0, 0);

		minX, minY = 10, 10;
		maxX, maxY = 950, 630;

		dc.SetPen(wx.Pen(color));
		dc.SetBrush(wx.Brush(color));
		dc.DrawRectangle(0, 0, rect.width, minY);
		dc.DrawRectangle(0, minY, minX, maxY - minY);
		dc.DrawRectangle(maxX, minY, rect.width - maxX, maxY - minY);
		dc.DrawRectangle(0, maxY, rect.width, rect.height);

		# dc.DrawText("---- label ----", 200, 100)
		pass;
		# x,y=self.GetPosition()
		# dc = wx.ScreenDC()
		# bmp = self.GetBg()
		# brush = wx.Brush(bmp)
		# dc.SetBackground(brush)
		# orange = wx.Colour(255,132,0)
		# dc.SetTextForeground(orange)
		# dc.DrawText('Hello transparent window! This text is not transparent.', x+13, y+11);

	def GetBg(self):
		x,y=self.GetPosition()
		xx,yy=self.GetSizeTuple()
		bmp = wx.EmptyBitmap(xx, yy)
		dc = wx.MemoryDC()
		dc.SelectObject(bmp)
		dc.Blit(x,y,xx,yy,wx.ScreenDC(),x,y)
		return bmp


# 键盘值映射表
KeyCodeMap = {
	314 : "LEFT",
	315 : "UP",
	316 : "RIGHT",
	317 : "DOWN",
};

# Unicode值映射表
UnicodeKeyMap = {
	27 : "ESC",
	32 : "SPACE",
};

# 根据事件获取热键值
def getHotKeyByEvent(event):
	key = [];
	if event.ControlDown():
		key.append("CTRL");
	if event.AltDown():
		key.append("ALT");
	if event.ShiftDown():
		key.append("SHIFT");
	if event.GetKeyCode() >= 340 and event.GetKeyCode() <= 351:
		key.append("F" + str(event.GetKeyCode() - 339)); # F1 ~ F12
	elif event.GetKeyCode() in KeyCodeMap:
		key.append(KeyCodeMap[event.GetKeyCode()]);
	elif event.GetUnicodeKey() in UnicodeKeyMap:
		key.append(UnicodeKeyMap[event.GetUnicodeKey()]);
	else:
		key.append(chr(event.GetUnicodeKey()).upper());
	return "_".join(key);

def onKeyDown(event):
	event.DoAllowNextEvent();
	print(getHotKeyByEvent(event))


if __name__ == "__main__":
	app = wx.App();
	app.Bind(wx.EVT_CHAR_HOOK, onKeyDown);
	frame1 = Frame1();
	frame1.Show();
	app.MainLoop()