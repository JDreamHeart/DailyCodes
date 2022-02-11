# -*- coding: utf-8 -*-

import os
import re
import json
import threading
import xml.dom.minidom


# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
# res文件路径
RES_PATH = CURRENT_PATH  # os.path.abspath(os.path.join(CURRENT_PATH, ".."))


class FindFuncBase(object):
    def __init__(self):
        super(FindFuncBase, self).__init__()

    def get_file_path_list(self):
        pass
    
    def add_file_path_list(self, file_path_list, file_path):
        if file_path and file_path not in file_path_list:
            file_path_list.append(file_path)

    def get_not_fund_path_list(self, file_path_list):
        ret = []
        for file_path in file_path_list:
            if "." not in file_path:
                continue
            if file_path[0] in ("/", "\\"):
                file_path = file_path[1:]
            full_path = os.path.join(RES_PATH, file_path)
            if not os.path.exists(full_path):
                ret.append(file_path)
        return ret

    def get_result(self):
        path_list = self.get_file_path_list()
        return self.get_not_fund_path_list(path_list)


class FindFuncXml(FindFuncBase):
    def __init__(self, file_path):
        super(FindFuncXml, self).__init__()
        self._file_path = file_path
        self._dom = None
        content = ""
        try:
            with open(file_path, "r") as f:
                content = f.read()
        except:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        if content:
            self._dom = xml.dom.minidom.parseString(content)
        else:
            print("Invalid file content!", file_path)
    
    @property
    def root(self):
        if self._dom:
            return self._dom.documentElement
        return None
        
    @staticmethod
    def get_child_by_tag_name(node, tag_name):
        for child in node.childNodes:
            if child.nodeType != xml.dom.Node.ELEMENT_NODE:
                continue
            if child.tagName == tag_name:
                return child
        return None


class FindFuncMtg(FindFuncXml):

    def get_text_value(self, param_tb, name):
        tex = FindFuncXml.get_child_by_tag_name(param_tb, name)
        if tex:
            return tex.getAttribute("Value")
        return ""
    
    def get_file_path_list(self):
        root = self.root
        if not root:
            return []
        path_list = []
        for mat in root.getElementsByTagName("Material"):
            param_tb = FindFuncXml.get_child_by_tag_name(mat, "ParamTable")
            if not param_tb:
                continue
            for key in ("Tex0", "Tex1", "Tex2", "Tex3", "Tex4", "Tex5",
            "NormalMap", "TexReflection", "SpecularMap", "TexNoise", "Spec2dTex0", "Spec2dTex1",
            "screenTex0", "screenTex1", "screenTex2", "screenTex3"):
                self.add_file_path_list(path_list, self.get_text_value(param_tb, key))
        return path_list


class FindFuncScn(FindFuncXml):

    def get_file_path_list(self):
        root = self.root
        if not root:
            return []
        path_list = []
        for all_files in root.getElementsByTagName("AllFiles"):
            for child in all_files.childNodes:
                if child.nodeType != xml.dom.Node.ELEMENT_NODE:
                    continue
                self.add_file_path_list(path_list, child.getAttribute("Path"))
        return path_list


class FindFuncSfx(FindFuncXml):

    def get_file_path_list(self):
        root = self.root
        if not root:
            return []
        path_list = []
        for sprite in root.getElementsByTagName("Sprite"):
            self.add_file_path_list(path_list, sprite.getAttribute("Texture"))
        return path_list


class FindFuncPse(FindFuncBase):
    def __init__(self, file_path):
        super(FindFuncPse, self).__init__()
        self._file_path = file_path
        self._cfg = {}
        try:
            with open(file_path, "rb") as f:
                self._cfg = json.load(f);
        except Exception as e:
            print("Failed to load pse! [{}]".format(file_path))
    
    @property
    def body(self):
        return self._cfg.get("Body", {})
    
    def _get_file_path(self, cfg, k, path_list):
        sub_cfg = cfg[k]
        if isinstance(sub_cfg, dict):
            for sub_k in sub_cfg:
                self._get_file_path(sub_cfg, sub_k, path_list)
        elif isinstance(sub_cfg, list):
            for sub_i in range(len(sub_cfg)):
                self._get_file_path(sub_cfg, sub_i, path_list)
        elif k in ("_filename", "_file_name", "_texture"):
            if sub_cfg and isinstance(sub_cfg, str) and sub_cfg not in path_list:
                path_list.append(sub_cfg)

    def get_file_path_list(self):
        path_list = []
        body = self.body
        if isinstance(body, dict):
            for k in body:
                self._get_file_path(body, k, path_list)
        return path_list


class FindFuncSfxMus(FindFuncSfx):
    def get_file_path_list(self):
        root = self.root
        if not root:
            return []
        path_list = []
        for sprite in root.getElementsByTagName("FxSoundEventDrive"):
            file_name = sprite.getAttribute("FileName")
            event_name = sprite.getAttribute("EventName")
            if event_name:
                file_name += ":{}".format(event_name)
            self.add_file_path_list(path_list, file_name)
        # return path_list

        filter_path_list = []
        for path in path_list:
            path = path.replace("\\", "/")
            if ".fev:" in path:
                continue
            filter_path_list.append(path)
        return filter_path_list

    def get_result(self):
        return self.get_file_path_list()


class FindFuncPseMus(FindFuncPse):
    
    def _get_file_path(self, cfg, k, path_list):
        sub_cfg = cfg[k]
        if isinstance(sub_cfg, dict):
            for sub_k in sub_cfg:
                self._get_file_path(sub_cfg, sub_k, path_list)
        elif isinstance(sub_cfg, list):
            for sub_i in range(len(sub_cfg)):
                self._get_file_path(sub_cfg, sub_i, path_list)
        elif k == "TypeName" and sub_cfg == "ParticleComponentAudio":
            audio_name = cfg.get("_name", "")
            is_find_out = False
            for name in ("_filename", "_file_name", "_texture"):
                path = cfg.get(name, None)
                if path and isinstance(path, str) and path not in path_list:
                    path_list.append("{}  ({})".format(path, audio_name))
                    is_find_out = True
            if not is_find_out:
                path_list.append("空路径  ({})".format(audio_name))

    def get_file_path_list(self):
        path_list = []
        for k in self._cfg:
            self._get_file_path(self._cfg, k, path_list)
        # return path_list

        filter_path_list = []
        for path in path_list:
            path = path.replace("\\", "/")
            if ".fev:" in path:
                continue
            filter_path_list.append(path)
        return filter_path_list

    def get_result(self):
        return self.get_file_path_list()


class FindFuncMtgShader(FindFuncXml):

    def get_tech_path(self, tech):
        tech_name = tech.getAttribute("TechName")
        if not tech_name:
            return None
        ret = re.search(r"(.*)::\w+$", tech_name)
        if ret:
            tech_path_ori = ret.group(1)
            tech_path, tech_ext = os.path.splitext(tech_path_ori)
            if not tech_ext:
                return None
            if tech_path[0] in ("/", "\\"):
                tech_path = tech_path[1:]
            full_path = os.path.join(RES_PATH, tech_path + ".nfx")
            if not os.path.exists(full_path):
                return tech_path_ori
        return None
    
    def get_file_path_list(self):
        root = self.root
        if not root:
            return []
        path_list = []
        for tech in root.getElementsByTagName("Technique"):
            tech_path = self.get_tech_path(tech)
            if not tech_path:
                continue
            name = tech.parentNode.getAttribute("Name")
            self.add_file_path_list(path_list, "{} ({})".format(tech_path, name))
        return path_list

    def get_result(self):
        return self.get_file_path_list()


class FindFuncSfxShader(FindFuncXml):

    def get_tech_path(self, tech):
        tech_name = tech.getAttribute("DecalTech")
        if not tech_name:
            return None
        ret = re.search(r"(.*)::\w+$", tech_name)
        if ret:
            tech_path_ori = ret.group(1)
            tech_path, tech_ext = os.path.splitext(tech_path_ori)
            if not tech_ext:
                return None
            if tech_path[0] in ("/", "\\"):
                tech_path = tech_path[1:]
            full_path = os.path.join(RES_PATH, tech_path + ".nfx")
            if not os.path.exists(full_path):
                return tech_path_ori
        return ""
    
    def get_file_path_list(self):
        root = self.root
        if not root:
            return []
        path_list = []
        for tech_key in ("ShaderCtrl", "Sprite"):
            for tech in root.getElementsByTagName(tech_key):
                tech_path = self.get_tech_path(tech)
                if not tech_path:
                    continue
                name = tech.getAttribute("Name")
                self.add_file_path_list(path_list, "{} ({})".format(tech_path, name))
            
        return path_list

    def get_result(self):
        return self.get_file_path_list()


class FindFuncPseTech(FindFuncPse):
    
    def _get_file_path(self, cfg, k, path_list):
        sub_cfg = cfg[k]
        if isinstance(sub_cfg, dict):
            for sub_k in sub_cfg:
                self._get_file_path(sub_cfg, sub_k, path_list)
        elif isinstance(sub_cfg, list):
            for sub_i in range(len(sub_cfg)):
                self._get_file_path(sub_cfg, sub_i, path_list)
        elif k == "TypeName" and sub_cfg == "ParticleRenderEffect":
            tech_name = cfg.get("_name", "")
            component = cfg.get("_component", {})
            if "_ext_technique" in component and component["_ext_technique"] not in FindExtTech.VALID_EXT_TECH_TYPE:
                path = component["_ext_technique"]
                if path not in path_list:
                    path_list.append("ExtTechnique[{}]  ({})".format(path, tech_name))

    def get_file_path_list(self):
        path_list = []
        for k in self._cfg:
            self._get_file_path(self._cfg, k, path_list)
        # return path_list

        filter_path_list = []
        for path in path_list:
            path = path.replace("\\", "/")
            if ".fev:" in path:
                continue
            filter_path_list.append(path)
        return filter_path_list

    def get_result(self):
        return self.get_file_path_list()


class FindFuncSfxTech(FindFuncXml):

    def get_tech_path(self, tech):
        tech_name = tech.getAttribute("PostProcessKind")
        if not tech_name or not tech_name.isdigit():
            return None
        if int(tech_name) not in FindExtTech.VALID_EXT_TECH_TYPE:
            return tech_name
        return ""
    
    def get_file_path_list(self):
        root = self.root
        if not root:
            return []
        path_list = []
        for tech_key in ("ShaderCtrl",):
            for tech in root.getElementsByTagName(tech_key):
                tech_path = self.get_tech_path(tech)
                if not tech_path:
                    continue
                name = tech.getAttribute("Name")
                self.add_file_path_list(path_list, "ExtTechnique[{}]  ({})".format(tech_path, name))
            
        return path_list

    def get_result(self):
        return self.get_file_path_list()


class FindNotFund(object):
    OUTPUT_FILE_NAME = "output_not_fund.txt"

    IS_SEARCH_ALL = False

    TYPE_DICT = {
        ".mtg": FindFuncMtg,
        ".scn": FindFuncScn,
        ".sfx": FindFuncSfx,
        ".pse": FindFuncPse,
    }

    def __init__(self, dir_path):
        super(FindNotFund, self).__init__()
        self._dir_path = dir_path

    def _output_result(self, dir_path, result = []):
        if os.path.isdir(dir_path):
            for root, _, files in os.walk(dir_path):
                for file_name in files:
                    self._output_one_result(root, file_name, result)
        else:
            dir_name = os.path.dirname(dir_path)
            self._output_one_result(dir_name, dir_name.replace(dir_path, ""), result)
    
    def _output_one_result(self, root, file_name, result):
        _, ext = os.path.splitext(file_name)
        type_class = self.TYPE_DICT.get(ext.lower(), None)
        if not type_class:
            return
        try:
            full_path = os.path.join(root, file_name)
            ff = type_class(full_path)
            if not self.check_preconditions(ff):
                return
            ret = ff.get_result()
            if ret:
                if self.IS_SEARCH_ALL:
                    result.extend(ret)
                else:
                    relative_path = full_path.replace(RES_PATH, "").replace("\\", "/")
                    content = "{}:\n\t{}\n\n".format(relative_path, "\n\t".join(ret))
                    result.append(content)
        except Exception as e:
            print("Failed to get not fund result![{}, {}]\n".format(file_name, root), e)
    
    def check_preconditions(self, find_obj):
        return True
    
    def output(self):
        if os.path.isdir(self._dir_path):
            content_dict = {}
            for path in os.listdir(self._dir_path):
                dir_path = os.path.join(self._dir_path, path)
                if path not in content_dict:
                    content_dict[path] = []
                t = threading.Thread(target = self._output_result, args = (dir_path, content_dict[path]))
                t.start();
                t.join()
            # 转换内容
            content_list = []
            if self.IS_SEARCH_ALL:
                for result in content_dict.values():
                    for k in result:
                        if k in content_list:
                            continue
                        content_list.append(k)
            else:
                for result in content_dict.values():
                    if result:
                        content_list.append("".join(result))
            if content_list:
                output_file = os.path.join(self._dir_path, self.OUTPUT_FILE_NAME)
                with open(output_file, "w+") as f:
                    f.write("\n".join(content_list))
        else:
            raise Exception("Invalid dir path!", self._dir_path)


class FindMusic(FindNotFund):
    IS_EXISTS_USER_FILE = True

    OUTPUT_UNUSED_FILE_NAME = "output_music_unused.txt"

    OUTPUT_FILE_NAME = "output_music.txt"
    TYPE_DICT = {
        ".sfxmusic": FindFuncSfxMus,
        ".psemusic": FindFuncPseMus,
    }

    def __init__(self, dir_path):
        super(FindMusic, self).__init__(dir_path)
        self._unused_file_list = []

    def check_preconditions(self, ff):
        full_path = ff._file_path
        file_name, ext = os.path.splitext(full_path)
        user_file = file_name + ext.replace("music", "")
        if not os.path.exists(user_file):
            relative_path = full_path.replace(RES_PATH, "").replace("\\", "/")
            # print("Does not exist user file! [{}]".format(relative_path))
            self._unused_file_list.append(relative_path)
            return False
        return True

    def output(self):
        super(FindMusic, self).output()
        if self._unused_file_list:
            output_file = os.path.join(self._dir_path, self.OUTPUT_UNUSED_FILE_NAME)
            with open(output_file, "w+") as f:
                f.write("\n".join(self._unused_file_list))


class FindShader(FindNotFund):
    OUTPUT_FILE_NAME = "output_shader.txt"
    TYPE_DICT = {
        ".sfx": FindFuncSfxShader,
        ".mtg": FindFuncMtgShader,
        ".mtl": FindFuncMtgShader,
    }


class FindExtTech(FindNotFund):
    OUTPUT_FILE_NAME = "output_ext_tech.txt"
    TYPE_DICT = {
        ".pse": FindFuncPseTech,
        ".sfx": FindFuncSfxTech,
    }

    VALID_EXT_TECH_TYPE = (0, 7, 3, 15, 8)



if __name__ == "__main__":
    pass

    # file_path = os.path.join(RES_PATH, "models/field/high/a/prop/high_a_box_wood_a.mtg")
    # ff = FindFuncMtg(file_path)
    
    # file_path = os.path.join(RES_PATH, "scene/world/novice_village01/novice_village01_content/-5_-4.scn")
    # ff = FindFuncScn(file_path)
    
    # file_path = os.path.join(RES_PATH, "fx/ui/zhuangbeijiebao/zhuangbeijiebao.sfx")
    # ff = FindFuncSfx(file_path)
    
    # file_path = os.path.join(RES_PATH, "fx/skill/03fs/12/fx_skill_fs12_start.pse")
    # ff = FindFuncScn(file_path)

    # print("==========", ff.get_result())

    # dir_path = os.path.join(CURRENT_PATH, "ui/")
    
    # f = FindNotFund(CURRENT_PATH)
    # f.output()
    
    # file_path = os.path.join(RES_PATH, "fx/monster/g_niutouren/fx_g_niutouren_magic01_boom.sfxmusic")
    # ff = FindFuncSfxMus(file_path)
    
    # file_path = os.path.join(RES_PATH, "fx/skill/12zs/02/fx_skill_zs02_boom.psemusic")
    # ff = FindFuncPseMus(file_path)

    # print("==========", ff.get_result())
    
    f = FindMusic(CURRENT_PATH)
    f.IS_SEARCH_ALL = True
    f.output()

    # file_path = os.path.join(RES_PATH, "fx/monster/g_julang/fx_g_julang_magic05_boom.sfx")
    # ff = FindFuncSfxShader(file_path)
    
    # file_path = os.path.join(RES_PATH, "character/zuoqi/q7_zuolang/q7_fx.mtg")
    # ff = FindFuncMtgShader(file_path)

    # print("==========", ff.get_result())

    # f = FindShader(CURRENT_PATH)
    # # f.IS_SEARCH_ALL = True
    # f.output()
    
    # file_path = os.path.join(RES_PATH, "fx/skill/09gd/02/fx_skill_gd02_hit.pse")
    # ff = FindFuncPseTech(file_path)
    
    # file_path = os.path.join(RES_PATH, "fx/monster/g_quchong/fx_g_quchong_die.sfx")
    # ff = FindFuncSfxTech(file_path)

    # print("==========", ff.get_result())
    
    # f = FindExtTech(CURRENT_PATH)
    # # f.IS_SEARCH_ALL = True
    # f.output()

    # _FxResTable_data = ()
    # ret = []
    # for fx_res in _FxResTable_data:
    #     file_path = fx_res[1]
    #     if file_path[0] in ("/", "\\"):
    #         file_path = file_path[1:]
    #     full_path = os.path.join(RES_PATH, file_path)
    #     if not os.path.exists(full_path):
    #         ret.append("{}: {}".format(fx_res[0], file_path))
    # print("\n".join(ret))
