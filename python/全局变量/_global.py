# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-03-22 13:06:51
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-03-23 13:30:03

global _G;
_G = {};

def setG(key,value):
	try:
		if id(_G[key]):
			print("The global var is existed !");
	except Exception:
		_G[key] = value;
	

def getG(key):
	try:
		return _G[key];
	except NameError as e:
		print("The global var is not exist !");
		raise e
	