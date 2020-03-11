import wx;

from enum import Enum, unique;

@unique
class AdjustType(Enum):
    UNKNOW      = 0;
    LEFT        = 1;
    TOPLEFT     = 2;
    TOP         = 3;
    TOPRIGHT    = 4;
    RIGHT       = 5;
    BOTTOMRIGHT = 6;
    BOTTOM      = 7;
    BOTTOMLEFT  = 8;
    INSIDE      = 9;

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

class GrabDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, pos = (0, 0), size=wx.GetDisplaySize(), style=wx.NO_BORDER|wx.STAY_ON_TOP);
        # 注册事件
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

    # 重置选中区域
    def resetSelectedArea(self):
        self.updateFirstAndLastPoint(wx.Rect(0, 0, 1, 1));
        self.updateDCRect();
        self.__adjusting = False;
    
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
            self.EndModal(wx.ID_OK);
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

