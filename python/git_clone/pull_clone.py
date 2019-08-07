# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-08-06 17:39:27
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-08-07 11:51:46
import sys, os, re, json;

CURRENT_PATH = os.getcwd();

defaultCfg = {
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
				[" -- elseif key == 293 then --f4模拟旋转", "  elseif key == 293 then --f4模拟旋转"],
			],
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

# 获取用户信息
def getUinfo():
	# if len(sys.argv) <= 2:
	# 	raise Exception("参数错误，必须填入用户名和密码！");
	# return ":".join([sys.argv[1], sys.argv[2]]);
	return "ZJ:pwdXXX";

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
def pullOrClone(gitUrl, tgPath, branch = ""):
	gitPath = "git -C "+tgPath;
	if os.path.exists(tgPath):
		os.system(gitPath+" reset --hard HEAD^");
		# 切到master分支后拉取
		checkoutBranch(gitPath, "master");
		os.system(gitPath+" pull");
	else:
		url = gitUrl.replace("://", "://"+getUinfo()+"@");
		os.system("git clone " + url + " " + tgPath);
	# 切换分支
	checkoutBranch(gitPath, branch);
	# 最后重新拉取
	os.system(gitPath+" pull");

def pullOrCloneGit(gitList = []):
	for gitInfo in gitList:
		if "git" in gitInfo and "path" in gitInfo:
			pullOrClone(gitInfo["git"], gitInfo["path"], gitInfo.get("branch", ""));

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
	with open(path, "w") as f:
		f.write(data);

def replaceFiles(replaceList = []):
	print("==== ReplaceFiles start ====");
	for replaceInfo in replaceList:
		if "file" in replaceInfo and "content" in replaceInfo:
			print("replace file:", replaceInfo["file"]);
			replaceFileContent(replaceInfo["file"], replaceInfo["content"]);
	print("==== ReplaceFiles end ====");


if __name__ == '__main__':
	cfg = getCfg();
	pullOrCloneGit(cfg.get("gitList", []));
	replaceFiles(cfg.get("replaceList", []));