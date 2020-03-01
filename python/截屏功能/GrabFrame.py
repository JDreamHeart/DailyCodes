import wx;

class GrabFrame(wx.Dialog):
    def __init__(self, frame):
        wx.Dialog.__init__(self, frame, wx.NewId(), pos = (0, 0),
                          size=wx.GetDisplaySize(), style=wx.NO_BORDER | wx.STAY_ON_TOP)
 
        ###################################全局变量########################################
        self.firstPoint = wx.Point(0, 0)#记录截图的第一个点
        self.lastPoint  = wx.Point(0, 0)#记录截图的最后一个点
        self.Started = False            #记录是否按下鼠标左键
        self.frame = frame
 
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.On_Mouse_LeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.On_Mouse_LeftUp)
        self.Bind(wx.EVT_MOTION, self.On_Mouse_Move)
 
    def OnPaint(self, evt):
        dc = wx.GCDC(wx.BufferedPaintDC(self))
        self.PaintUpdate(dc)
 
    def PaintUpdate(self, dc):
        rect = self.GetClientRect()
        color = wx.Colour(0, 0, 0, 120)
 
        #设置绘制截图区域时矩形的点
        minX, minY = min(self.firstPoint.x, self.lastPoint.x), min(self.firstPoint.y, self.lastPoint.y)
        maxX, maxY = max(self.firstPoint.x, self.lastPoint.x), max(self.firstPoint.y, self.lastPoint.y)
 
        #画出整个屏幕的截图
        dc.DrawBitmap(self.frame.grabBmp, 0, 0)
 
        #画出阴影部分（截取的部分不需要画）
        dc.SetPen(wx.Pen(color));
        dc.SetBrush(wx.Brush(color));
        dc.DrawRectangle(0, 0, rect.width, minY);
        dc.DrawRectangle(0, minY, minX, maxY - minY);
        dc.DrawRectangle(maxX, minY, rect.width - maxX, maxY - minY);
        dc.DrawRectangle(0, maxY, rect.width, rect.height);
 
        if(self.Started == True):
 
            #画出截图区域的边框
            dc.SetPen(wx.Pen(wx.Colour(0, 150, 0)))
            dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
            dc.DrawRectangle(minX, minY, maxX - minX, maxY - minY)
 
            #显示信息
            dc.SetBrush(wx.Brush(wx.Colour(255,0,0)))
            dc.DrawRectangleList([
                (minX - 2, minY - 2, 5, 5),
                (maxX / 2 + minX / 2 - 2, minY - 2, 5, 5),
                (maxX - 2, minY - 2, 5, 5),
                (maxX - 2, maxY / 2 + minY / 2 - 2, 5, 5),
                (maxX - 2, maxY - 2, 5, 5),
                (maxX / 2 + minX / 2 - 2, maxY - 2, 5, 5),
                (minX - 2, maxY - 2, 5, 5),
                (minX - 2, maxY / 2 + minY / 2 - 2, 5, 5)
                ])
            color = wx.Colour(0,0,0,180)
            dc.SetPen(wx.Pen(color))
            dc.SetBrush(wx.Brush(color, wx.SOLID))
            w,h = 140, 43
            s = u'区域大小：'+str(maxX - minX)+'*'+str(maxY - minY)
            s += u'\n鼠标位置：（'+str(self.lastPoint.x)+','+str(self.lastPoint.y)+')'
            dc.DrawRectangle(minX, minY-h-5 if minY -5 > h else minY+5, w, h)
            dc.SetTextForeground(wx.Colour(255,255,255))
            dc.DrawText(s, minX+5, (minY-h-5 if minY-5 > h else minY + 5)+5)
 
 
 
    def On_Mouse_LeftDown(self, evt):
        self.Started = True
        self.firstPoint = evt.GetPosition()
        self.lastPoint = evt.GetPosition()
        
    def On_Mouse_LeftUp(self, evt):
        if(self.Started):
            self.lastPoint = evt.GetPosition()
            if(self.firstPoint.x == self.lastPoint.x)&(self.firstPoint.y == self.lastPoint.y):
                wx.MessageBox(u"区域设置不正确", "Error", wx.OK | wx.ICON_ERROR, self)
                self.Started = False
                self.firstPoint = wx.Point(0, 0)#记录截图的第一个点
                self.lastPoint  = wx.Point(0, 0)#记录截图的最后一个点
                
            else:
                bmp = self.frame.grabBmp.GetSubBitmap(wx.Rect(
                    min(self.firstPoint.x, self.lastPoint.x),
                    min(self.firstPoint.y, self.lastPoint.y),
                    abs(self.firstPoint.x - self.lastPoint.x),
                    abs(self.firstPoint.y - self.lastPoint.y)
                    ))
 
                self.Close()
                self.frame.Show()
                self.frame.onGrab(bmp)
        
    def On_Mouse_Move(self, evt):
        if(self.Started):
            self.lastPoint = evt.GetPosition()
            self.NewUpdate()
 
    def NewUpdate(self):
        self.RefreshRect(self.GetClientRect(), True)
        self.Update()