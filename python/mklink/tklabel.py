# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-10 16:05:31
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-10 17:51:56
import re;
import math;

from tkinter import *;

def getTextSize(text):
    tlen = len(text);
    return int((len(text.encode('utf-8')) - tlen)/2 + tlen);

def clipText(text, maxSize, mode = "r"):
	diff = getTextSize(text) - maxSize;
	if diff <= 0: # 判断是否需要裁剪
		return text;
	# 裁剪的开始和结束位置
	sIdx, eIdx = 0, len(text);
	if mode == "m":
		mIdx = int(len(text) / 2);
		sIdx = mIdx - int(diff/4);
		eIdx = mIdx + math.ceil(diff/4);
	elif mode == "l":
		eIdx = sIdx + int(diff/2);
	elif mode == "r":
		sIdx = eIdx - int(diff/2);
	# 校验位置
	if eIdx < 0:
		eIdx = 0;
	if sIdx > len(text):
		sIdx = len(text);
	# 更新裁剪大小
	while (getTextSize(text[sIdx:eIdx]) < diff and (sIdx > 0 or eIdx < len(text))):
		if sIdx > 0:
			sIdx -= 1;
			if getTextSize(text[sIdx:eIdx]) == diff:
				break;
		if eIdx < len(text):
			eIdx += 1;
	# clipSize = getTextSize(text[sIdx:eIdx]);
	# sSize, eSize = 0, 0;
	# while (clipSize + sSize + eSize < diff and (sIdx > 0 or eIdx < len(text))):
	# 	if sSize <= eSize:
	# 		if sIdx > 0:
	# 			charSize = getTextSize(text[sIdx]);
	# 			sSize += charSize;
	# 			sIdx -= 1;
	# 		elif eIdx < len(text):
	# 			charSize = getTextSize(text[eIdx]);
	# 			eSize += charSize;
	# 			eIdx += 1;
	# 	else:
	# 		if eIdx < len(text):
	# 			charSize = getTextSize(text[eIdx]);
	# 			eSize += charSize;
	# 			eIdx += 1;
	# 		elif sIdx > 0:
	# 			charSize = getTextSize(text[sIdx]);
	# 			sSize += charSize;
	# 			sIdx -= 1;
	# 返回裁剪结果
	return text[:sIdx] + "..." + text[eIdx:];

window = Tk()
window.title('Label的使用')
window.geometry('400x400')

tips = StringVar();

label = Label(window, textvariable=tips) #text为显示的文本内容
tips.set('www.jdreamheart.com/xxx/yyy/zzz.zip的开发计划数量的返回拉萨扩大解放螺丝钉福克斯的就恢复了深刻的回复');
label.pack()

text = tips.get()
tips.set(clipText(text, 60));

# 复选框
cv1 = BooleanVar();
cv2 = BooleanVar();
cv3 = BooleanVar();
c1 = Checkbutton(window, text = "生成", variable = cv1, onvalue = True, offvalue = False)
cv1.set(True)
c2 = Checkbutton(window, text = "打开", variable = cv2, onvalue = True, offvalue = False)
c3 = Checkbutton(window, text = "运行", variable = cv3, onvalue = True, offvalue = False)

c1.pack()
c2.pack()
c3.pack()

def onClick():
	print(cv1.get(), cv2.get(), cv3.get())

b = Button(window, text="测试", command=onClick);
b.pack()

window.mainloop()