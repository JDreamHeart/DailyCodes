# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-03-22 13:06:26
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-03-23 13:09:51

import _global as _GG;

import init as Init;

class Loader:
	def __init__(self):
		Runner = Init.Loader();
		_GG.setG("test99", [1,11,9]);
		Runner.run();


if __name__ == "__main__":
	_GG.setG("test1", 999);
	Loader()