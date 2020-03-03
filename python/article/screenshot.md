# 基于Python实现截屏功能

----

## 整体思路

  * **对当前屏幕进行截图**；
  * **点击选择截图尺寸（用于对上面获得的截图进行裁剪）**；
  * **允许调整截图尺寸和位置**；
  * **鼠标右键响应（取消或显示操作菜单**）
  * **选择所要保存的图片格式**。


## 1. 截图当前屏幕

以下展示了两种方式的截屏逻辑：  

```py
import wx;
from PIL import ImageGrab;
​
# 第一种：通过ImageGrab截屏
def getScreenBmp1():
  ds = wx.DisplaySize();
  im = ImageGrab.grab((0, 0, ds.x, ds.y));
  # 转成wxPython的Bitmap对象
  img = wx.Image(ds[0], ds[1], im.tobytes());
  return img.ConvertToBitmap();
  
# 第二种：直接通过wxPython进行截屏
def getScreenBmp2():
    ds = wx.GetDisplaySize();
    bmp = wx.Bitmap(ds.x, ds.y);
    mdc = wx.MemoryDC();
    mdc.SelectObject(bmp);
    mdc.Blit(0, 0, ds.x, ds.y, wx.ScreenDC(), 0, 0);
    mdc.SelectObject(wx.NullBitmap);
    return bmp;

```

## 2. 选择截图尺寸
在一个平面上，只需要两个点位置，就能确定出以这两点为对角的矩形。
而这所确定的矩形，就是想要的截图区域。  

因此，可以在鼠标按下和抬起的时候，分别记录第一和第二个点位置，然后根据这两个点，在界面上绘制出选中区。  

同时，为了能实时显示截图选中区，还需监听鼠标的移动事件，在每次移动（在已按下鼠标的前提下）时记录第二点位置。
```py

class ScreenshotDialog(wx.Dialog):
    """docstring for ScreenshotDialog"""
    def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
        self.initParams(params);
        super(ScreenshotDialog, self).__init__(None, title = "截屏", pos = (0, 0), size = wx.GetDisplaySize(), style = wx.NO_BORDER|wx.STAY_ON_TOP);
        # 绑定事件
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown);
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp);
        self.Bind(wx.EVT_MOTION, self.onMove);
        # 初始化属性
        self.__grabBmp = self.getScreenBmp();
        self.__firstPoint = wx.Point(0, 0);
        self.__lastPoint = wx.Point(0, 0);
        self.__downing = False;

    def onLeftDown(self, event):
        if self.__downing:
            return;
        self.__downing = True;
        self.__firstPoint = event.GetPosition();
        self.__lastPoint = event.GetPosition();

    def onLeftUp(self, event):
        if self.__downing:
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
    
    def onMove(self, event):
        pos = event.GetPosition();
        if self.__downing:
            self.__lastPoint = pos;
            self.updateDCRect();
```

以下代码，实现了利用两点位置进行截图选中区绘制的逻辑。  
```py
# 在__init__函数中，添加事件绑定
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM);
        self.Bind(wx.EVT_PAINT, self.onPaint);

    # 绘制选中区
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

    def updateFirstAndLastPoint(self, rect = None):
        if not rect:
            rect = self.getScreenshotRect();
        self.__firstPoint = wx.Point(rect.x, rect.y);
        self.__lastPoint = wx.Point(rect.x + rect.width, rect.y + rect.height);
        pass;

    # 重新绘制选中区
    def updateDCRect(self):
        self.RefreshRect(self.GetClientRect(), True);
        self.Update();

```

## 选中后调整截图尺寸

该部分内容，主要分为以下几个步骤：
  * 首先在点击抬起时，确定当前处于允许调整状态；
  * 然后在鼠标移动到特定的调整点后，改变相应的鼠标的状态图标；
  * 接着在鼠标按下并进行移动的时候，根据鼠标当前的（调整）状态，进行第一和第二点的坐标变化，并重新绘制选中区；
  * 鼠标抬起，重置相关状态。

```py
# 在__init__函数中，添加初始化属性
        self.__preAdjustPoint = wx.Point(0, 0);
        self.__adjusting = False;
        self.__adjustType = AdjustType.UNKNOW;

# 更新鼠标点击事件
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

```

## 取消或显示菜单项
在选中了截图区域之后，就该考虑怎么进行保存或取消选中等操作了。  

以下代码，通过对右键不同区域进行判定，实现了取消或显示菜单项（包括菜单项的点击）的功能。  
```py
# 在__init__函数中，添加事件绑定和初始化属性
        self.Bind(wx.EVT_RIGHT_UP, self.onRightUp);
        self.__menu = None;

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

```

## 选择保存格式
在以上的**取消或显示菜单项**的代码中，出现创建文件保存弹窗的逻辑（`onSave`函数中创建的`wx.FileDialog`对象）。  

这里只允许选择`wildcard`中所包含的格式，包括PNG、JPEG、BMP、TIF。

## 完整代码
Github链接：[https://github.com/JDreamHeart/DailyCodes/python/article/screenshot.py](https://github.com/JDreamHeart/DailyCodes/blob/master/python/article/screenshot.py)  

以上截屏功能基于`Python 3.7`版本开发（如若遇到编码等错误，先确保是否因您所使用的`Python`版本太老）。  

由于截屏的显示界面基于`wxPython`模块进行实现，因此，得确保电脑已安装`wxPython`模块。  
```sh
// 通过 pip 安装 wxPython 模块
pip install wxPython

// 或 使用阿里云镜像安装 wxPython 模块
pip install wxPython -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```