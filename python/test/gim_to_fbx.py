import os
import sys


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));

# def get_path_cfg(path):
#     gim_path, fbx_path = "", ""
#     exe_path = ""
#     cfg_path = os.path.join(path, "path_config")
#     if os.path.exists(cfg_path):
#         with open(cfg_path) as f:
#             for line in f.readlines():
#                 kv_list = line.strip().split("=")
#                 if len(kv_list) > 1:
#                     if kv_list[0] == "gim_path":
#                         gim_path = kv_list[1]
#                     elif kv_list[0] == "fbx_path":
#                         fbx_path = kv_list[1]
#                     elif kv_list[0] == "exe_path":
#                         exe_path = kv_list[1]
#     return gim_path, fbx_path, exe_path

class GimToFbx(object):
    def __init__(self, src_path, tgt_path, exe_path=""):
        self._src_path = src_path.replace("\\", "/")
        self._tgt_path = tgt_path.replace("\\", "/")
        if not os.path.exists(self._tgt_path):
            os.makedirs(self._tgt_path)
        self._exe_path = exe_path
    
    def convert(self):
        if not os.path.exists(self._src_path):
            print("Non-exists src path[{}]!".format(self._src_path))
            return
        if not os.path.exists(self._exe_path):
            print("Non-exists exe path[{}]!".format(self._exe_path))
            return
        for root, _, files in os.walk(self._src_path):
            for file_name in files:
                if not file_name.endswith(".gim"):
                    continue
                full_path = os.path.join(root, file_name).replace("\\", "/")
                self._convert(full_path)
    
    def _convert(self, full_path):
        relative_path = full_path.replace(self._src_path + "/", "")
        print("Start convert gim[{}] to fbx".format(relative_path))

        fbx_path, ext = os.path.splitext(relative_path)
        full_fbx_path = os.path.join(self._tgt_path, fbx_path)

        code = os.system("{} {} {}".format(self._exe_path, os.path.abspath(full_fbx_path), os.path.abspath(full_path)))
        if code != 0:
            print("Failed to convert gim[{}] to fbx[{}]!".format(os.path.abspath(full_path), os.path.abspath(full_fbx_path)))


if __name__ == "__main__":
    cwd = CURRENT_PATH

    # gim_path, fbx_path, exe_path = get_path_cfg(cwd)

    
    if len(sys.argv) < 4:
        raise Exception("Invalid argv[{}]!".format(sys.argv))
    gim_path, fbx_path, exe_path = sys.argv[1], sys.argv[2], sys.argv[3]

    if not gim_path:
        gim_path = cwd
    if not fbx_path:
        fbx_path = os.path.join(cwd, "output")

    gtf = GimToFbx(gim_path, fbx_path, exe_path)
    gtf.convert()