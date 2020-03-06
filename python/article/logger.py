# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-05 17:35:44
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-06 16:21:44
import os,logging;
from logging.handlers import RotatingFileHandler;

# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
# main文件路径
MAIN_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "../.."))

LevelKeyMap = {
	"debug" : logging.DEBUG,
	"info" : logging.INFO,
	"warning" : logging.WARNING,
	"error" : logging.ERROR,
};

MethodKeyMap = {
	"d" : "debug",
	"i" : "info",
	"w" : "warning",
	"e" : "error",
};

# LogRecord类
class LogRecord(logging.LogRecord):
	"""docstring for LogRecord"""
	def __init__(self, name, level, pathname, lineno, msg, args, exc_info, func=None):
		pathname = pathname.replace(VerifyPath(MAIN_PATH+"/"), ""); # 修改路径为相对路径
		super(LogRecord, self).__init__(name, level, pathname, lineno, msg, args, exc_info, func=None);

	def getMessage(self):
		logMsg = "{} "*(len(self.args) + 1);
		return logMsg.format(self.msg, *self.args);

# Logger类
class Logger(logging.Logger):
	"""docstring for Logger"""
	def __init__(self, name, level = "debug", fmt="%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s",
		methodKeyMap = None, isLogStream = True, isLogFile = False, logFileName = "", maxBytes = 1000, backupCount = 10):
		super(Logger, self).__init__(name, level = LevelKeyMap[level]);
		self.__formatter = logging.Formatter(fmt);
		self.setLevel(LevelKeyMap[level]);
		# 设置handler
		if isLogStream:
			self.__setStreamHandler__(level = level);
		if isLogFile:
			if len(logFileName) == 0:
				logFileName = name;
			self.__setFileHandler__(logFileName, maxBytes, backupCount, level = level);
		# 新增日志打印方法接口
		self.__initMethods__(methodKeyMap);

	# 覆盖Logger类的makeRecord方法
	def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
		rv = LogRecord(name, level, fn, lno, msg, args, exc_info, func);
		if extra:
			for key in extra:
				if (key in ["message", "asctime"]) or (key in rv.__dict__):
					raise KeyError("Attempt to overwrite %r in LogRecord" % key);
				rv.__dict__[key] = extra[key];
		return rv;

	# 添加handler
	def __addHandler__(self, handler, level = "debug"):
		handler.setLevel(LevelKeyMap[level]);
		handler.setFormatter(self.__formatter);
		self.addHandler(handler);

	# 设置日志窗口输出
	def __setStreamHandler__(self, level = "debug"):
		if not hasattr(self, "_streamHandler"):
			self._streamHandler = logging.StreamHandler();
			self.__addHandler__(self._streamHandler, level = level);

	# 设置日志文件输出
	def __setFileHandler__(self, fileName, maxBytes, backupCount, level = "debug"):
		if not hasattr(self, "_fileHandler"):
			dirName = os.path.abspath(os.path.dirname(fileName));
			if not os.path.exists(dirName):
				os.makedirs(dirName);
			self._fileHandler = RotatingFileHandler(fileName, maxBytes = maxBytes, backupCount = backupCount, encoding = "utf-8");
			self.__addHandler__(self._fileHandler, level = level);

	# 初始化方法
	def __initMethods__(self, methodKeyMap = None):
		if methodKeyMap == None:
			methodKeyMap = MethodKeyMap;
		for key in methodKeyMap:
			setattr(self, key, self.__getMethod__(methodKeyMap[key]));

	def __getMethod__(self, level):
		def method(msg, *args, **kwargs):
			if self.isEnabledFor(LevelKeyMap[level]):
				argList = list(args);
				argList.append("");
				self._log(LevelKeyMap[level], msg, argList, **kwargs);
		return method;