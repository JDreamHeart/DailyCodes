
import wx

from PIL import ImageGrab
import cv2;
import numpy as np;

from GrabFrame import GrabFrame;
from GrabDialog import GrabDialog;

class Dialog2(wx.Dialog):
    def __init__(self, bitmap, pos = (0, 0)):
        wx.Dialog.__init__(self,None,style=wx.RESIZE_BORDER|wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.TRANSPARENT_WINDOW)
        self.__bm = wx.StaticBitmap(self, bitmap = bitmap, pos = pos);
        
        self.__op = wx.Panel(self);
        save_Button = wx.Button(self.__op,label=u"关闭",pos=(0,0),size=(100,45))
        self.Bind(wx.EVT_BUTTON,self.OnSave,save_Button)
        b = wx.BoxSizer(wx.HORIZONTAL);
        b.Add(save_Button);
        self.__op.SetSizerAndFit(b);

        box = wx.BoxSizer(wx.VERTICAL);
        box.Add(self.__bm);
        box.Add(self.__op);
        self.SetSizerAndFit(box);
        self.__op.Move(-100, 0);
        pass;
    
    def OnSave(self, event):
        self.Hide();
        dlg = wx.FileDialog(self, "保存截屏图片", defaultFile = "screenshot", wildcard = "JPEG files (.jpg)|.jpg|PNG files (.png)|.png", style=wx.FD_SAVE);
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename();
            if not self.__bm.GetBitmap().SaveFile(filename, wx.BITMAP_TYPE_PNG):
                print("保存失败！", filename)


class Dialog1(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,style=wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.TRANSPARENT_WINDOW)

        ds = wx.DisplaySize()
        im = ImageGrab.grab((0, 0, ds[0], ds[1]))

        # im.save("temp_sreenshot.png");

        img = wx.Image(ds[0], ds[1], im.tobytes());

        self.bm = wx.StaticBitmap(self, bitmap = img.ConvertToBitmap(), pos = (0, 0));



        self.__timer = wx.Timer(self.bm);
        self.bm.Bind(wx.EVT_TIMER, self.onTimer, self.__timer);

        self.__isDowning = False;
        self.bm.Bind(wx.EVT_LEFT_DOWN, self.onClickDown);
        self.bm.Bind(wx.EVT_LEFT_UP, self.onClickUp);

        # self.panel = wx.Panel(self.bm,pos = (100, 100), size=(640,320))
        
        Close_Button = wx.Button(self.bm,label=u"关闭",pos=(200,100),size=(100,45))
        
        self.Bind(wx.EVT_BUTTON,self.OnClose,Close_Button)

        im1 = im.crop((40,60, 100,200))
        img1 = wx.Image(im1.size[0], im1.size[1], im1.tobytes());

        bmBtn = wx.BitmapButton(self.bm, bitmap = img1.ConvertToBitmap(), pos = (0, 0))
        
    def OnClose(self,event):
        self.Destroy()
    
    def onClickDown(self, event):
        self.__isDowning = True;
        pass;
    
    def onClickUp(self, event):
        if self.__isDowning:
            self.__isDowning = False;
        pass;
    
    def onTimer(self, event):
        if self.__isDowning:
            pass;

class Frame1(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,size=(960,640))
        self.panel = wx.Panel(self,size=(960,640))
        
        btn = wx.Button(self.panel,label=u"开启弹窗",pos=(540,320),size=(100,45))
        
        self.Bind(wx.EVT_BUTTON,self.onOpen,btn)

        self.grabBmp = wx.Bitmap();
        self.__sdc = wx.ScreenDC();
        self.__mdc = wx.MemoryDC();
        self.__mdc.SelectObject(self.grabBmp)
        self.__gf = None;
        
    def onOpen(self,event):
        self.Hide();
        self.Update_Screen_Bmp();
        # if not self.__gf:
        #     # self.__gf = GrabFrame(self);
        # self.__gf.Show()
        gd = GrabDialog();
        gd.ShowModal();
        gd.Destroy();
        self.Show();
    
    def Update_Screen_Bmp(self):
        ds = wx.GetDisplaySize()
        self.grabBmp = self.getScreenBmp() #.SetSize(ds);
        # self.__mdc.Blit(0, 0, ds.x, ds.y, wx.ScreenDC(), 0, 0);

    def getScreenBmp(self):
        ds = wx.GetDisplaySize()
        bmp = wx.Bitmap(ds.x, ds.y);
        mdc = wx.MemoryDC()
        mdc.SelectObject(bmp)
        mdc.Blit(0, 0, ds.x, ds.y, wx.ScreenDC(), 0, 0)
        mdc.SelectObject(wx.NullBitmap)
        return bmp
    
    def onGrab(self, bmp):
        d = Dialog2(bmp);
        d.Show();
        pass;



        
if __name__ == "__main__":
    app = wx.App()
    frame1 = Frame1()
    frame1.Show()
    app.MainLoop()