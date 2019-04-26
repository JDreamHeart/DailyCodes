# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-04-24 10:11:53
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-04-26 10:41:43

import json
import hashlib

stageKeyMap = {
	"kaishiyouxi" : "GameStart",
	"dingzhuang" : "DingZhuang",
	"zhitou" : "ZhiTou",
	"fapai" : "DealCard",
	"jiesuan" : "Settle",
	"jieshuyouxi" : "GameEnd",
};

nodeKeyMap = {
	"onStart" : "on_start",
	"opUsers" : "get_next_op_user",
	"opInfo" : "set_op_info",
	"opCheck" : "wait_op_msg",
	"opResult" : "set_op_result",
	"opNext" : "get_next_node",
	"onEnd" : "on_end",
};

opCodeKeyMap = {
	u"过" : "Pass",
	u"出牌" : "Out",
	u"抓牌" : "Grab",
	u"分张" : "FenZhang",
	u"吃牌" : "Chi",
	u"碰牌" : "Peng",
	u"暗杠" : "AnGang",
	u"直杠" : "PengGang",
	u"补杠" : "BuGang",
	u"点炮胡" : "Hu",
	u"自摸" : "ZiMo",
	u"抢杠胡" : "QiangHu",
	u"听牌" : "Ting",
	u"夹听" : "JiaTing",
	u"翻宝" : "FanBao",
	u"看宝" : "KanBao",
	u"换宝" : "HuanBao",
};

baseKeyMap = {
	"playerNumber" : "PlayerNumber",
	"totalCards" : "TotalCards",
	"zhuapai" : "Grab",
	"chupai" : "Out",
	"chipai" : "Chi",
	"pengpai" : "Peng",
	"gangpai" : "Gang",
	"baoting" : "Ting",
	"hupai" : "Hu",
	"jichupaixing" : "JiChuPaiXing",
	"tihuanpaizhang" : "ReplaceToCheckOp",
	"hutinggonggongjiance" : "CheckHuGroupCondition",
	"fenzhang" : "FenZhang",
	"liuju" : "LiuJu",
	"huanbao" : "HuanBao",
	"kanbao" : "KanBao",
	"caozuojianguolv" : "FilterOpInfo",
};

nameIdxMap = {}
def getIdByName(name):
	if name not in nameIdxMap:
		nameIdxMap[name] = 0;
	nameIdxMap[name] += 1;
	key = "_".join([name, str(nameIdxMap[name])])
	hm = hashlib.md5();
	hm.update(key.encode("utf-8"))
	return hm.hexdigest();

def insertTree2Pcfg(pcfg, tree):
	pcfg["trees"].append(tree);

def getGameTree(cfg):
	tree = {
		"title": "Game",
		"description": "game",
		"root": "0",
		"properties": {},
		"nodes": {
			"0" : {
				"id" : getIdByName("Game"),
				"name" : "Game",
				"children": cfg["stages"],
			},
		},
	};
	for k in cfg["stages"]:
		name = stageKeyMap.get(k, "Stage");
		tree["nodes"][k] = {
			"id" : getIdByName(name),
			"name" : name,
			"description" : k,
			"properties": {},
		};
		if k == "dapai" and "dapai" in cfg["process"]:
			tree["nodes"][k]["properties"] = getDaPaiData(cfg["process"]["dapai"]);
		if k == "jiesuan":
			tree["nodes"][k]["properties"] = {"settleTypes" : "Fan;Gang;"}
	return tree;

def getDaPaiData(cfg):
	pid2indexMap = {}; # 流程id对应位置信息
	totalPptsList = []; # 所有参数列表
	ppts = {};
	for i in range(len(cfg)):
		p = cfg[i];
		pid2indexMap[p["id"]] = i;
		ppts[str(i)] = {
			"id" : getIdByName("Process"),
			"name": "Process",
			"properties" : {},
		};
		pptsp = ppts[str(i)]["properties"];
		for k,v in nodeKeyMap.items():
			if k in p:
				pptsp[v] = {
					"properties": {},
				}
				if len(p[k]) > 0:
					# 根据priority字段，排序数据
					rl = sorted(p[k][0], key=lambda r:r["priority"]);
					for j in range(len(rl)):
						r = rl[j];
						name = r["id"].encode("utf-8");
						rule = {
							"id" : getIdByName(name),
							"name" : name,
							"properties" : getRuleArgs(r.get("args", [])),
						};
						totalPptsList.append(rule["properties"]);
						pptsp[v]["properties"][str(j)] = rule;
	# 转换格式
	formatPptsList(totalPptsList, [pid2indexMap, opCodeKeyMap]);
	# 转换成字符串
	for k in ppts:
		pptsp = ppts[k]["properties"];
		for k1 in pptsp:
			for k2 in pptsp[k1]["properties"]:
				pptsp[k1]["properties"][k2] = json.dumps(pptsp[k1]["properties"][k2]);
			pptsp[k1] = json.dumps(pptsp[k1]);
		ppts[k] = json.dumps(ppts[k]);
	return ppts;

# 获取规则参数
def getRuleArgs(args):
	properties = {};
	for i in range(len(args)):
		val = args[i];
		if not isinstance(val, int) and val.isdigit():
			properties[str(i)] = int(val);
		else:
			properties[str(i)] = val;
	return properties;

# 转换格式
def formatPptsList(totalPptsList, keyMapList = []):
	for pro in totalPptsList:
		for k,v in pro.items():
			for keyMap in keyMapList:
				if v in keyMap:
					pro[k] = keyMap[v];
					break;

def insertBaseRuleTrees(projectCfg, cfg):
	for k in baseKeyMap:
		if k in cfg:
			totalPptsList = []; # 所有参数列表
			treeChildren = [];
			tree = {
				"title" : baseKeyMap[k],
				"root" : "0",
				"nodes": {
					"0": {
						"id" : getIdByName("Sequence"),
						"name": "Sequence",
						"children": treeChildren,
					},
				},
			};
			for r in cfg[k]:
				rid = r["id"];
				rule = {
					"id" : getIdByName(rid),
					"name": rid,
					"description": "",
					"properties": getRuleArgs(r.get("args", [])),
				};
				totalPptsList.append(rule["properties"]);
				tree["nodes"][rule["id"]] = rule;
				treeChildren.append(rule["id"]);
			# 转换格式
			formatPptsList(totalPptsList, [opCodeKeyMap]);
			insertTree2Pcfg(projectCfg, tree);


if __name__ == '__main__':
	with open("GameConfig.json", "rb") as f:
		cfg = json.load(f);
	# Game树
	projectCfg = {
		"trees" : [],
	};
	insertTree2Pcfg(projectCfg, getGameTree(cfg));
	insertBaseRuleTrees(projectCfg, cfg);
	# 合并旧配置【如结算】
	with open("tree.json", "rb") as f:
		treeCfg = json.load(f);
	for tree in treeCfg.get("trees", []):
		insertTree2Pcfg(projectCfg, tree);
	# 输出配置
	with open("project.json", "wb") as f:
		f.write(json.dumps(projectCfg, sort_keys = True, indent = 2, separators=(',', ':')).encode("utf-8"));