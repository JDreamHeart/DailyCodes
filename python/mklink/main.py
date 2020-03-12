# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-10 15:16:05
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-10 17:12:54
import os,re,subprocess;

# 无日志打印运行命令
def runCmd(cmd, cwd=os.getcwd(), funcName="call", argDict = {}):
    startupinfo = subprocess.STARTUPINFO();
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW;
    startupinfo.wShowWindow = subprocess.SW_HIDE;
    return getattr(subprocess, funcName)(cmd, cwd = cwd, startupinfo = startupinfo, **argDict);


def updateTestEnv():
	with open("test.env", "w", encoding = "utf-8") as f:
		f.write("\n".join([
			"pyexe="+"xxx.python.exe",
			"mainfile=" + "main.p",
			"buildfile=" + "build.y",
		]));


if __name__ == '__main__':
	# 生成桌面快捷方式
	# runCmd("E:\\MyOthers\\Private\\ptip\\PyToolsIP\\run\\makelnk.bat E:\\MyOthers\\Private\\ptip\\PyToolsIP\\pytoolsip.exe PyToolsIP Python工具集成平台")
	# 运行
	# os.system("start /d E:\\MyOthers\\Private\\ptip\\PyToolsIP pytoolsip.exe");
	# 打开目录
	# runCmd("cmd /c explorer E:\\MyOthers\\Private\\ptip\\PyToolsIP");
	# os.system("explorer E:\\MyOthers\\Private\\ptip\\PyToolsIP");
	pass;
	# updateTestEnv();
	tips = "dhjsfkasdjh";
	rate = 3.976
	print(f"{tips}[%.2f%%]" % (rate * 100))