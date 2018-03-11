import os;
import re;
import time;
from urllib import request;
from bs4 import BeautifulSoup;
from selenium import webdriver;

class DownloadImg:
	def __init__(self, flag):
		self.downloadFlag = flag;

	def getDownloadName(self, nameArr, formatStr):
		return "_".join(nameArr) + "." + formatStr;

	def download(self, imgUrl, name):
		if imgUrl != None:
			print(imgUrl)
			result = request.urlopen(imgUrl);
			if result.getcode() == 200:
				data = result.read();
				with open(name, "wb") as code:
					code.write(data);
					code.close();

	def findImgByBeautifulSoup(self, url):
		res = request.urlopen(url);
		respond = res.read();
		soup = BeautifulSoup(respond);
		for link in soup.find_all("img"):
			print(link);

	def getDynamicImgPath(self, url):
		# imgPathList = [];
		driver = webdriver.PhantomJS(executable_path="D:\\OtherApplication\\phantomjs\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
		# browser = webdriver.Chrome(executable_path = "D:\\OtherApplication\\chromedriver_win32\\chromedriver.exe",options=option);
		# time.sleep(10)
		driver.get(url);
		# imgTags = driver.find_elements_by_tag_name("img");
		# # print(imgTags.get_attribute("src"))
		# for img in imgTags:
		# 	print(img.get_attribute("src"))
		# print(driver.title)
		soup = BeautifulSoup(driver.page_source);
		for link in soup.find_all("img"):
			print(link);
			# if "?cid=" in link.attrs['src']:
			# 	print(link);
				# imgPathList.append(link.attrs['src']);
		driver.quit();
		# return imgPathList;

	def main(self, url):
		pathName = "F:\\Projects\\Workspace\\PythonWorkSpace\\";



if __name__ == "__main__" :
	url = "http://www.shenmanhua.com/doupocangqiong/669.html";
	# url = "http://www.baidu.com";

	# main()
	# result = request.urlopen(url);
	# if result.getcode() == 200:
	# 	print(result.read())

	pathName = "F:\\Projects\\Workspace\\PythonWorkSpace\\";

	DownloadImg = DownloadImg(2);
	# help(webdriver.Chrome)

	# imgPathList = DownloadImg.getDynamicImgPath(url);
	# DownloadImg.findImgByBeautifulSoup(url);
	# for imgPath in imgPathList:
	# 	print(imgPath);
		# DownloadImg.download(imgPath, pathName + "test1.jpg");

	DownloadImg.download("http://mhpic.mh51.com/comic/D%2F%E6%96%97%E7%A0%B4%E8%8B%8D%E7%A9%B9%2F669%E8%AF%9DSM%2F1.jpg-smh.middle", pathName + "test1.jpg");

	# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
 
	# dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置userAgent
	# dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
	 
	# obj = webdriver.PhantomJS(executable_path='D:\OtherApplication\phantomjs\phantomjs-2.1.1-windows\bin\',desired_capabilities=dcap)