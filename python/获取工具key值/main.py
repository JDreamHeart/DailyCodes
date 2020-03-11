import re;

from gettkey.test import *;

from local.gettkey.test import *;

def main():
    test();
    print("+++++++++++++++++++++++++++++");
    testlocal();

if __name__ == "__main__":
    main();

    # findStr = "/(.*)_(.*)_";

    # replaceStr = "{}.te{}st{}";

    # s = "aaa/bbb_111_ccc/ddd";
    # mt = re.match("(.*)("+ findStr +")(.*)", s);
    # if mt:
    #     a, b, *c, d = mt.groups();
    #     print(mt.groups());
    #     print(a, b, c, d);
    #     diff = replaceStr.count("{}") - len(c);
    #     if diff > 0:
    #         c.extend([""]*diff);
    #     print(replaceStr.format(*c));