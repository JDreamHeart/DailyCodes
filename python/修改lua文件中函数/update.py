# -*- coding: utf-8 -*-
# @Author: HymanLiu
# @Date:   2018-01-24 11:56:37
# @Last Modified by:   JinZhang
# @Last Modified time: 2018-01-26 12:09:56

# 目前只适用于函数的增、改、删

import os
import re

# 该文件主要放置所要修改的函数【一般不改变】
base_file_path = {
    './baseFunc.lua',
}

# 是否检测所有版本的文件【为False则表示只检测最新版本号的文件】
is_check_all_version = False;

# 所需修改的麻将名称
check_file_path = [
    "sxlinfenmj",
    "scziyangsanfangmj",
    # "scziyangmj",
    "lnshenyangmj",
    "lndalianmj",
    "xueliuchenghemj",
    "lnchaoyangnewmj",
    "scyibinnewmj",
]

# 所需修改的文件路径【会检查该路径是否存在】
change_file_list = [
    "bin/game/common/new_core/operation/opLogic/gang/gangLogic.lua",
    "bin/game/common/core/operation/opLogic/gang/gangLogic.lua",

    "bin/game/common/logic/rules/operation/make/MakeBehavior.lua",
    "bin/game/common/core/mahjong.lua",
]


# 获取所有要修改的麻将tag路径
def getTagFilePath(basePath):
    allTagPathsList = [];
    pathDist = {};
    rpcPathDist = {};
    maxVersion = -1;
    rpcMaxVersion = -1;
    if os.path.exists(basePath):
        subPaths = os.listdir(basePath);
        for subPath in subPaths :
            key = re.search(r"_(\d*)_", subPath).group(1);
            key = int(key); # 转换为数字
            if not pathDist.has_key(key) :
                pathDist[key] = [];
            pathDist[key].append(basePath + "/" + subPath + "/"); # 对应于版本号【key】的tag路径
            allTagPathsList.append(basePath + "/" + subPath + "/"); # 所有满足要求的tag路径
            if maxVersion < key :
                maxVersion = key;
                pass;
    rpcBasePath = basePath + "_rpc";
    if os.path.exists(rpcBasePath):
        subPaths = os.listdir(rpcBasePath);
        for subPath in subPaths :
            key = re.search(r"_(\d*)_", subPath).group(1);
            key = int(key); # 转换为数字
            if not rpcPathDist.has_key(key) :
                rpcPathDist[key] = [];
            rpcPathDist[key].append(rpcBasePath + "/" + subPath + "/"); # 对应于版本号【key】的tag路径
            allTagPathsList.append(rpcBasePath + "/" + subPath + "/"); # 所有满足要求的tag路径
            if rpcMaxVersion < key :
                rpcMaxVersion = key;
                pass;
    if is_check_all_version :
        return allTagPathsList; # 返回所有版本号的检测路径

    retPathList = [];
    if pathDist.has_key(maxVersion) :
        retPathList.extend(pathDist[maxVersion]); # 版本号maxVersion的检测路径
    if rpcPathDist.has_key(rpcMaxVersion) :
        retPathList.extend(rpcPathDist[rpcMaxVersion]); # 版本号rpcMaxVersion的检测路径
    return retPathList;

# 获取所有要修改的路径文件
def getAllChangePathList(checkPaths, changeFiles):
    allPathList = [];
    for basePath in checkPaths:
        pathList = getTagFilePath(basePath);
        for theBasePath in pathList:
            for theFilePath in changeFiles:
                thePath = theBasePath + theFilePath;
                if os.path.exists(thePath):
                    allPathList.append(thePath);
                    pass;
    return allPathList;


# 替换类型
CHANGE_TYPE = {
    "ADD" : 0,
    "REMOVE" : 1,
    "REPLACE" : 2,
    "UNCHANGE" : 3,
}

# 获取替换或增加的内容
def getReplaceContentList(baseFileName):

    repContentList = {};
    addContentList = {};
    contentSortList = [];
    
    content = "";
    matchCount = 0;
    funcStart = False;
    funcEnd = True;
    funcName = "";
    changeType = CHANGE_TYPE["UNCHANGE"];
    with open(baseFileName, 'r') as f:
        for line in f.readlines():
            if re.search('ADD', line):
                changeType = CHANGE_TYPE["ADD"];
            elif re.search('REMOVE', line):
                changeType = CHANGE_TYPE["REMOVE"];
            elif re.search('REPLACE', line):
                changeType = CHANGE_TYPE["REPLACE"];
            elif re.search('UNCHANGE', line):
                changeType = CHANGE_TYPE["UNCHANGE"];

            if not funcStart:
                funcNameGroup = re.search( r'function (.*?)[(]', line, re.I);
                if funcNameGroup and funcNameGroup.group():
                    funcName = funcNameGroup.group(1);
                    matchCount = 0;
                    funcStart = True;
                    funcEnd = False;
                    pass;

            if funcStart:
                content += line;
                line = line.strip();
                line = line.lstrip();
                if re.search('function ', line):
                    matchCount += 1;
                if re.search('if ', line) and not re.search('elseif', line):
                    matchCount += 1;
                if re.search('for ', line):
                    matchCount += 1;
                if line.find('end') == 0:
                    matchCount -= 1;
                    if matchCount == 0:
                        funcStart = False;
                        funcEnd = True;
                        pass;
                if funcEnd and content != "" and funcName != "":
                    if changeType == CHANGE_TYPE["ADD"]:
                        addContentList[funcName] = content;
                    elif changeType == CHANGE_TYPE["UNCHANGE"]:
                        repContentList[funcName] = -1;
                    elif changeType == CHANGE_TYPE["REMOVE"]:
                        repContentList[funcName] = "";
                    else:
                        repContentList[funcName] = content;

                    contentSortList.append(funcName);
                    content = "";
                    funcName = "";
                    pass;

    return repContentList, addContentList, contentSortList;


# 添加对应的文件内容
def checkToAddContent(funcName, addContentList, contentSortList, printStrInfo):
    if addContentList:
        idx = contentSortList.index(funcName);
        if idx > 0 :
            tempAddFuncName = [];
            checkIdxList = range(idx - 1, -1, -1);
            for i in checkIdxList:
                if contentSortList[i] in addContentList.keys():
                    tempAddFuncName.append(contentSortList[i]);
                else:
                    break;
            if len(tempAddFuncName) > 0 :
                addData = "";
                tempAddFuncName.reverse();
                for tempFuncName in tempAddFuncName:
                    addData += addContentList[tempFuncName];
                    printStrInfo['replaceFuncNames'].append({'funcName' : 'function ' + tempFuncName + '(...)', 'changeTypeStr' : '增加函数'});
                return True, addData;

    return False, '';


# 修改对应的文件内容
def changeContenByFile(filePath, repContentList, addContentList, contentSortList):
    printStrInfo = {'filePath' : filePath, 'replaceFuncNames' : []};

    data = ''

    matchCount = 0
    funcStart = False
    funcEnd = True
    funcName = "";
    isAddContent = False;
    with open(filePath, 'r') as f:
        for line in f.readlines():

            if not funcStart:
                funcNameGroup = re.search( r'function (.*?)[(]', line, re.I);
                if funcNameGroup and funcNameGroup.group():
                    funcName = funcNameGroup.group(1);
                    if funcName in repContentList.keys():
                        if not isAddContent:
                            isAddContent, content = checkToAddContent(funcName, addContentList, contentSortList, printStrInfo);
                            if isAddContent:
                                data += content;
                                pass;
                        if repContentList[funcName] == -1 :
                            funcName = "";
                        else:
                            matchCount = 0;
                            funcStart = True;
                            funcEnd = False;
            if funcStart and funcName != "":
                line = line.strip();
                line = line.lstrip();
                if re.search(r'function[ ,(]', line):
                    matchCount += 1;
                if re.search(r'if[ ,(]', line) and not re.search('elseif', line):
                    matchCount += 1;
                if re.search('for ', line):
                    matchCount += 1;
                if line.find('end') == 0:
                    matchCount -= 1;
                    if matchCount == 0:
                        funcStart = False;
                        funcEnd = True;
                        pass;
                line = "";
                if funcEnd:
                    line = repContentList[funcName];
                    changeTypeStr = (line == "") and "删除函数" or "替换函数";
                    printStrInfo['replaceFuncNames'].append({'funcName' : 'function ' + funcName + '(...)', 'changeTypeStr' : changeTypeStr});
                    funcName = "";
                    pass;

            data += line

    open(filePath,'r+').truncate()

    with open(filePath, 'r+') as f:
        f.writelines(data)

    return printStrInfo;


# 打印替换结果
def dumpResult(printStrList):
    for v in printStrList:
        print(v['filePath'])
        for vv in v['replaceFuncNames']:
            print(vv['changeTypeStr'] + ': ' + vv['funcName']);
        print("-------------------------------");

    pass;


def main():
    printStrList = [];
    allPathList = getAllChangePathList(check_file_path, change_file_list);
    # allPathList = ["changeFunc.lua"]; # 测试时使用
    # for printPath in allPathList :
    #     print(printPath);
    #     pass;

    for basePath in base_file_path:
        repContentList, addContentList, contentSortList = getReplaceContentList(basePath);

        # print(contentSortList)
        # print(repContentList,addContentList)

        for checkPath in allPathList:
            printStrInfo = changeContenByFile(checkPath, repContentList, addContentList, contentSortList);
            printStrList.append(printStrInfo);

    dumpResult(printStrList);
    pass;

# contentList = getReplaceContentList('./test.lua');
# # 测试结果
# idx = 1;
# for k in contentList:
#     print(idx, k);
#     idx += 1;
#     print(contentList[k]);
#     pass;

# print "ChouJiangLib.tttest" in contentList.keys()


## 测试python语法
# test = {};
# if test in vars() :
#     print("111")
# else:
#     print("222")

# test = range(9,1,-1)
# test = test.reverse()
# print(test)
# test = "gamescziyangsanfangmj_rpc_10_20180102174717";
# key = re.search(r"_([0-9]\d*)_", test).group(1);
# print(key)


## 运行主函数
main()