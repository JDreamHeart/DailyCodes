# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-03-22 13:07:28
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-03-23 13:24:56

import _global as _GG;

class Loader:
	def __init__(self):
		print("init___");
		print(_GG.getG("test1"));

	def run(self):
		print("run___");
		print(_GG.getG("test99"));
		_GG.setG("test1", [55,5]);
		print(_GG.getG("test1"));