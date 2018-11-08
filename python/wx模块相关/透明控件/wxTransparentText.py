# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-11-07 17:39:54
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-11-07 18:12:28

import wx;

class TransparentText(wx.StaticText):
	def __init__(self,parent,id=wx.ID_ANY,label='',pos=wx.DefaultPosition,size=wx.DefaultSize,style=wx.BORDER_NONE|wx.TB_HORIZONTAL,name='PyToolBarNameStr'):
		style |= wx.CLIP_CHILDREN|wx.TRANSPARENT_WINDOW
		wx.StaticText.__init__(self,parent,id,label,pos,size,style = style)
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.Bind(wx.EVT_PAINT, self.on_paint)
		# self.Bind(wx.EVT_ERASE_BACKGROUND,self.OnEraseBackground)
		# self.Bind(wx.EVT_SIZE, self.on_size)

	def on_paint(self, event):
		bdc = wx.PaintDC(self) 
		dc = wx.GCDC(bdc)
		# font_face = self.GetFont() 
		# font_color = self.GetForegroundColour() 
		# dc.SetFont(font_face) 
		# dc.SetTextForeground(font_color) 
		dc.DrawText(self.GetLabel(), 0, 0) 

	# def OnEraseBackground(self,event):
	# 	pass;

	# def on_size(self, event): 
	# 	self.Refresh() 
	# 	event.Skip() 

def on_down(event):
	print("000000000000000")

if __name__ == '__main__':
	app = wx.App();
	frame = wx.Frame(None, -1, size = (300,300))
	frame.SetTransparent(100) # 设置窗口的透明度

	# 显示内容
	panel = wx.Panel(frame, size = (200,200))
	panel.SetBackgroundColour("red")
	# p1 = wx.Panel(panel, size = (50,40))
	# p1.SetBackgroundColour("green")
	# 文本测试
	# text = wx.StaticText(panel, label = "测试文本")
	text = TransparentText(panel, label = "测试文本")
	text.Bind(wx.EVT_LEFT_DOWN, on_down)

	# 运行窗口
	frame.Show()
	app.MainLoop()