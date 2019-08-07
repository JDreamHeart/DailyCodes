# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-08-06 17:39:27
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-08-07 16:16:08
import sys, os, re, json;

CURRENT_PATH = os.getcwd();

defaultCfg = {
	# "userInfo" : "name:password",
	"gitList" : [
		{
			"git" : "https://code.266.com/266-hall-client/hall_demo.git",
			"path" : "hall_demo",
			"branch" : "test",
		},
		{
			"git" : "https://code.266.com/266-mahjong/client.git",
			"path" : "hall_demo/assets/app/game/box/mahjong",
			"branch" : "develop",
		},
		{
			"git" : "https://code.266.com/266-hall-client/matchkit.git",
			"path" : "hall_demo/assets/app/game/matchKit",
			"branch" : "",
		},
		{
			"git" : "https://code.266.com/266/roomkit.git",
			"path" : "hall_demo/assets/app/game/roomKit",
			"branch" : "",
		},
	],
	"replaceList" : [
		{
			"file" : "hall_demo/assets/app/config/appConfig/win32/featureConfig.lua",
			"content" : [
				["IGNOREUPDATEHALL = false", "IGNOREUPDATEHALL = true"],
				["IGNOREUPDATEGAME = false", "IGNOREUPDATEGAME = true"],
				["IGNOREROOMKITUPDATE = false", "IGNOREROOMKITUPDATE = true"],
				["IGNOREMATCHKITUPDATE = false", "IGNOREMATCHKITUPDATE = true"],
			],
		},
		{
			"file" : "hall_demo/assets/app/modules/notify/appNotifyCenter.lua",
			"content" : [
				["  elseif key == 293 then", " -- elseif key == 293 then"],
				[" -- elseif key == 293 then --f4", "  elseif key == 293 then --f4"],
			],
		},
		{
			"file" : "hall_demo/run.bat",
			"content" : [
				[":: start babe.exe \"x=", "start babe.exe \"console=0;x="]
			]
		},
	],
};

# 获取配置
def getCfg():
	cfg = defaultCfg;
	if os.path.exists("config.json"):
		with open("config.json", "r") as f:
			cfg = json.load(f);
	return cfg;

# 切换分支
def checkoutBranch(gitPath, branch):
	if not branch:
		return;
	localBranchReader = os.popen(gitPath+" branch");
	localBranchLines = localBranchReader.read();
	for line in localBranchLines.splitlines():
		if line.find(branch) != -1:
			os.system(gitPath+" checkout "+branch);
			return;
	os.system(gitPath+" checkout -b "+branch+" origin/"+branch);

# 拉取或克隆
def pullOrClone(uinfo, gitUrl, tgPath, branch = ""):
	gitPath = "git -C "+tgPath;
	if os.path.exists(tgPath):
		os.system(gitPath+" reset --hard HEAD^");
		# 切到master分支后拉取
		checkoutBranch(gitPath, "master");
		os.system(gitPath+" pull");
	else:
		url = gitUrl.replace("://", "://"+uinfo+"@");
		os.system("git clone " + url + " " + tgPath);
	# 切换分支
	checkoutBranch(gitPath, branch);
	# 最后重新拉取
	os.system(gitPath+" pull");

def pullOrCloneGit(uinfo, gitList = []):
	for gitInfo in gitList:
		if "git" in gitInfo and "path" in gitInfo:
			pullOrClone(uinfo, gitInfo["git"], gitInfo["path"], gitInfo.get("branch", ""));

# 替换文件内容
def replaceFileContent(path, content = []):
	if not os.path.exists(path):
		return;
	data = "";
	with open(path, "r", encoding = "utf-8") as f:
		for line in f.readlines():
			for v in content:
				if len(v) < 2:
					print("==== replaceFileContent fail ! ====", v)
					continue;
				if line.find(v[0]) != -1:
					line = line.replace(v[0], v[1]);
			data += line;
	with open(path, "w", encoding = "utf-8") as f:
		f.write(data);

def replaceFiles(replaceList = []):
	print("==== ReplaceFiles start ====");
	for replaceInfo in replaceList:
		if "file" in replaceInfo and "content" in replaceInfo:
			print("replace file:", replaceInfo["file"]);
			replaceFileContent(replaceInfo["file"], replaceInfo["content"]);
	print("==== ReplaceFiles end ====");

# 拉取或克隆
def pull_clone(cfg):
	pullOrCloneGit(cfg.get("userInfo", "JZ:pwd"), cfg.get("gitList", []));
	replaceFiles(cfg.get("replaceList", []));

# 删除文件夹
def removeFolder(path):
	if not os.path.exists(path):
		return;
	for p in os.listdir(path):
		f = os.path.join(path, p);
		if os.path.isdir(f):
			removeFolder(f);
			os.removedirs(f);
		elif os.path.isfile(f):
			os.remove(f);
		else:
			raise Exception("Invalid file", f);

# 删除hall_demo文件夹
def tryRemoveHallDemo():
	path = os.path.join(CURRENT_PATH, "hall_demo");
	if not os.path.exists(path):
		return;
	# 移除hall_demo文件夹
	if input("Warning! Should I remove folder 'hall_demo'? (y/n):") == "y":
		try:
			removeFolder(path);
		except Exception as e:
			print(e);
			print("Warning! Removing folder 'hall_demo' failed. Please remove folder 'hall_demo' manually!");

# 主函数
def main():
	# 获取配置
	cfg = getCfg();
	# 错误次数
	errCount, maxErrCount = 0, cfg.get("maxErrCount", 3);
	while errCount <= maxErrCount:
		try:
			pull_clone(cfg);
			return; # 没报错则直接退出主函数
		except Exception as e:
			print(e);
			errCount += 1;
			while errCount <= maxErrCount:
				ret = input("There is a error to pull or clone git! Should I try again? (y/n):");
				if ret == "y":
					if maxErrCount == errCount:
						tryRemoveHallDemo(); # 尝试删除hall_demo文件夹
					break; # 继续运行
				elif ret == "n":
					return; # 直接退出主函数


if __name__ == '__main__':
	# 运行主函数
	main();
	# 等待输入，便于查看日志
	input("Press any key to continue...");