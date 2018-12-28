# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-28 14:30:30
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-12-28 17:46:52
import wx;


if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, size = (700,360));

	p = wx.Panel(frame, size = (100,100));
	# p.SetBackgroundColour("black");

	t = wx.StaticText(p, label = "雅俗可赏")
	t.m_curPos = None;
	def onItemClick(event):
		t.m_curPos = event.GetPosition();
		event.Skip();
		print("ooo")
	def onItemMotion(event):
		if event.Dragging() and event.LeftIsDown() and t.m_curPos:
			pos = event.GetPosition() - t.m_curPos;
			t.Move(t.GetPosition().x + pos.x, t.GetPosition().y + pos.y);
	t.Bind(wx.EVT_LEFT_DOWN, onItemClick);
	t.Bind(wx.EVT_MOTION, onItemMotion);
	def onBtn(event = None):
		# t.Move(t.GetPosition().x + 100, t.GetPosition().y + 100);
		pass;

	# btn.Bind(wx.EVT_BUTTON, onBtn)

	btn = wx.Button(p, label = "测试", pos = (100,100));
	btn.Bind(wx.EVT_MOTION, onItemMotion);

	p1 = wx.Panel(p, pos = (100,0))
	img = wx.Image("flyChess.jpg", wx.BITMAP_TYPE_ANY);
	bm = wx.StaticBitmap(p1, bitmap = wx.BitmapFromImage(img));
	bx = wx.BoxSizer(wx.VERTICAL);
	bx.Add(bm);
	p1.SetSizerAndFit(bx);
	# p1.SetBackgroundColour("green");
	p1.Bind(wx.EVT_MOTION, onItemMotion);

	frame.Show(True);
	app.MainLoop();