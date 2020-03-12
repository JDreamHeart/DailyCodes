import os, inspect;

import re;

def testlocal():
    for frame in inspect.stack():
        filename = frame[0].f_code.co_filename;
        print(filename);
        mt = re.match("^E:/project/DailyCodes/python/获取工具key值/((local/)?[^/]+)/+.*$", filename.replace("\\", "/"));
        if mt:
            print("===222===", mt.group(1).replace("/", "-"));
    print("-----------------------")