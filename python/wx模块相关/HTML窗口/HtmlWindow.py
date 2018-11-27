# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-11-21 11:13:33
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-11-21 12:27:09
import  wx 
import  wx.html2
import webbrowser

class MyHtmlFrame(wx.Frame): 
	def __init__(self, parent, title): 
		wx.Frame.__init__(self, parent, -1, title, size = (600,400)) 
		# html = wx.html2.HtmlWindow(self) 

		# if "gtk2" in wx.PlatformInfo: 
		# 	html.SetStandardFonts() 

		# dlg = wx.TextEntryDialog(self, 'Enter a URL', 'HTMLWindow') 

		# if dlg.ShowModal() == wx.ID_OK: 
		# 	html.LoadPage(dlg.GetValue()) 

		# wx.CallAfter(html.LoadPage, "https://www.baidu.com/")
		# wx.CallAfter(html.LoadFile, "E:\\Project\\JSWorkSpace\\PiXiProjects\\PiXiJS_Test\\index.html")
		browser = wx.html2.WebView.New(self, style=0)
		wx.CallAfter(browser.LoadURL, "http://127.0.0.1:8020/PiXiJS_Test/index.html?__hbt=1542774008894")
		# webbrowser.open_new("https://www.baidu.com")
		
app = wx.App()  
frm = MyHtmlFrame(None, "Simple HTML Browser")  
frm.Show()  
app.MainLoop()