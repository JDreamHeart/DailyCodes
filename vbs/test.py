# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-08-27 18:28:13
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-08-27 19:42:35
import os,re,subprocess;

# 无日志打印运行命令
def runCmd(cmd, cwd=os.getcwd(), funcName="call", argDict = {}):
    startupinfo = subprocess.STARTUPINFO();
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW;
    startupinfo.wShowWindow = subprocess.SW_HIDE;
    return getattr(subprocess, funcName)(cmd, cwd = cwd, startupinfo = startupinfo, **argDict);

if __name__ == '__main__':
    runCmd(" ".join(["run.bat", "aaa", "bbb", os.getcwd()]));