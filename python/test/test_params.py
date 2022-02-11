from genericpath import exists
import os
import sys

def func(a, *args, b=233):
    print("params:", a, args, b)

if __name__ == "__main__":
    # func("t", b=110)
    # print("测试文本 {1}, {0}。".format(1, 2, 3, 4))
    print(sys.argv)
    if len(sys.argv) > 2:
        file_path = sys.argv[1] + ".fbx"
        dir_path = os.path.dirname(file_path)
        if not exists(dir_path):
            os.makedirs(dir_path)
        with open(file_path, "w+") as f:
            f.write(sys.argv[2])
