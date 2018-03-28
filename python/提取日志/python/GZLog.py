# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-03-22 16:52:33
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-03-22 21:35:56

import gzip;
import os;

class GZLogFile:
	def __init__(self, filePath, isRemoveFile):
		self.filePath = filePath;
		self.isRemoveFile = isRemoveFile;
