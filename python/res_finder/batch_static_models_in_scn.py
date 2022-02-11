# -*- coding: utf-8 -*-

from genericpath import exists
import os
import re
import sys
import math
import threading
import inspect
import ctypes
import xml.dom.minidom
from tkinter import *
from tkinter import messagebox;


# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
# res文件路径
RES_PATH = os.path.abspath(os.path.join(CURRENT_PATH, ".."))


# 停止线程
def StopThread(thread):
	try:
		if thread.is_alive():
			tid = ctypes.c_long(thread.ident);
			exctype = SystemExit;
			if not inspect.isclass(exctype):
				exctype = type(exctype);
			res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype));
			if res == 0:
				raise ValueError("Invalid thread !");
			elif res != 1:
				ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None);
				raise SystemError("PyThreadState_SetAsyncExc failed !");
	except Exception as e:
		show_log("Error: stop thread failed !", e);


class MainApp(Tk):
    AppTitle = "场景中静态模型合批设置处理器"
    AppSize = (1080, 720)

    def __init__(self):
        Tk.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.on_destroy)

        self.init_title()
        self.init_size()

        self._win = MainWin(self)

    def init_title(self):
        self.title(self.AppTitle)

    def init_size(self):
        width, height = self.AppSize
        posX, posY = (self.winfo_screenwidth() - width) / 2, (self.winfo_screenheight() - height) / 2
        self.geometry("%dx%d+%d+%d" % (width, height, posX, posY))

    def on_destroy(self):
        if self._win.is_running:  # 判断是否还存在处理线程
            if not messagebox.askokcancel(title="取消处理", message="当前仍在处理场景静态模型合批设置，是否确定要取消本次处理？"):
                return
        self.destroy()
    
    def show_log(self, log):
        self._win.output_text(log)


class MainWin(Frame):
    DefaultDistance = 300
    DefaultCount = 5
    
    LimitDistance = 1  # 限制的最小距离

    def __init__(self, app):
        Frame.__init__(self, app)
        self._app = app
        self.pack(expand=YES, fill=BOTH)
        
        self._smp_handler = ScnModelPosHandler()

        self._init_win()
    
    @property
    def is_running(self):
        return self._smp_handler.has_thread()
    
    def _init_win(self):
        self._create_params_frame()
        self._create_ctrl_frame()

        self._output_text = Text(self, width=MainApp.AppSize[0], height=300)
        self._output_text.pack(side=TOP, fill=X, padx=5, pady=5)
        
    def _create_field(self, parent, text, is_expand_entry, *args, **kwargs):
        field = Frame(parent)
        field.pack(side=TOP, fill=X, padx=5, pady=5)

        lab = Label(field, text=text, anchor=W)
        lab.pack(side=LEFT)
        ent = Entry(field, *args, **kwargs)
        if is_expand_entry:
            ent.pack(side=LEFT, expand=YES, fill=X)
        else:
            ent.pack(side=LEFT, fill=X)
        return field
    
    def _create_params_frame(self):
        frame = Frame(self, borderwidth = 1, relief = GROOVE);
        frame.pack(side=TOP, fill=X, padx=5, pady=5);
        
        Label(frame, text="【请输入参数】 ").pack(side=LEFT)

        self._dist_var = StringVar()
        self._dist_var.set(self.DefaultDistance)
        self._create_field(frame, "检测距离：", False, textvariable=self._dist_var)

        self._count_var = StringVar()
        self._count_var.set(self.DefaultCount)
        self._create_field(frame, "距离范围内的最低数量：", False, textvariable=self._count_var)

        self._scn_path_var = StringVar()
        self._scn_path_field = self._create_field(frame, "场景文件相对路径（不包含res）：", True, textvariable=self._scn_path_var)

        return frame
    
    def _create_ctrl_frame(self):
        frame = Frame(self, borderwidth = 1, relief = GROOVE);
        frame.pack(side=TOP, fill=X, padx=5, pady=5);
    
        Label(frame, text="【请选择模式】 ").pack(side=LEFT)
        
        self._ctrl_val = IntVar()
        self._ctrl_val.set(0)
        Radiobutton(frame, text="单个场景文件", variable=self._ctrl_val, value=0, command=self._on_change_ctrl_val).pack(anchor=W)
        Radiobutton(frame, text="游戏中生效的所有场景文件", variable=self._ctrl_val, value=1, command=self._on_change_ctrl_val).pack(anchor=W)
        
        self._ctrl_btn = Button(frame, width = 40, command=self._on_handle)
        self._ctrl_btn.pack(side=LEFT, pady=5)
        self.update_ctrl_btn_text()

        return frame
    
    def update_ctrl_btn_text(self):
        if self.is_running:
            self._ctrl_btn["text"] = "停止"
        else:
            self._ctrl_btn["text"] = "开始"

    def _on_change_ctrl_val(self):
        if self._ctrl_val.get() == 0:
            self._scn_path_field.pack(side=TOP, fill=X, padx=5, pady=5);
        else:
            self._scn_path_field.forget()
    
    def _on_handle(self):
        if self.is_running:
            if messagebox.askokcancel(title="停止处理", message="当前仍在处理场景静态模型合批设置，是否确定要停止本次处理？"):
                self._smp_handler.stop_thread_dict()
                show_log("已停止检测和处理场景文件!")
                self.update_ctrl_btn_text()
            return

        try:
            dist_str = self._dist_var.get().strip()
            dist = float(dist_str)
        except:
            messagebox.showerror(title="输入错误", message="检测距离必须是数字！")
            return
        if dist <= self.LimitDistance:
            messagebox.showerror(title="输入错误", message="检测距离必须大于{}！".format(self.LimitDistance))
            return

        try:
            count_str = self._count_var.get().strip()
            count = int(count_str)
        except:
            messagebox.showerror(title="输入错误", message="距离范围内的最低数量必须是整数！")
            return
        if count <= 0:
            messagebox.showerror(title="输入错误", message="距离范围内的最低数量必须大于0！")
            return

        if self._ctrl_val.get() == 0:
            scn_path = self._scn_path_var.get().strip()
            if not scn_path:
                messagebox.showerror(title="输入错误", message="场景文件不能为空！")
                return
            _, ext = os.path.splitext(scn_path)
            if ext != ".scn":
                messagebox.showerror(title="输入错误", message="仅支持SCN格式的场景文件！")
                return
            scn_full_path = os.path.abspath(os.path.join(RES_PATH, scn_path))
            if not os.path.exists(scn_full_path):
                messagebox.showerror(title="输入错误", message="场景文件不存在！{}".format(scn_full_path))
                return

        self._output_text.delete('1.0', END)  # 清空
        
        show_log("开始对场景文件的检测和处理...")

        if self._ctrl_val.get() == 0:
            self._smp_handler.start_thread([scn_path], dist, count, thread_callback=self._on_thread_callback)
        else:
            scn_path_cnt, thread_cnt = self._smp_handler.check_model_pos_by_valid_scn(dist, count, thread_callback=self._on_thread_callback)
            show_log("场景文件数量：{}; 线程数量：{}".format(scn_path_cnt, thread_cnt))

        self.update_ctrl_btn_text()

    def output_text(self, text):
        self._output_text.insert(END, text)
    
    def _on_thread_callback(self, is_thread_end, gim_info_list):
        if not is_thread_end and gim_info_list:
            show_log("-----------------------------------------", is_output_file=True, is_print_when_output=False)
            show_log("\n".join(["{}  -> {}".format(*gim_info) for gim_info in gim_info_list]), is_output_file=True, is_print_when_output=False)
            show_log("-----------------------------------------", is_output_file=True, is_print_when_output=False)

        if is_thread_end and not self.is_running:
            show_log("已完成对场景文件的检测和处理.\n")
            self.update_ctrl_btn_text()


class XmlParser(object):
    def __init__(self, file_path):
        super(XmlParser, self).__init__()
        self._file_path = ""
        self._dom = None

        self.set_file_path(file_path)
    
    def set_file_path(self, file_path):
        if self._file_path == file_path:
            return
        self._file_path = file_path
        if self._dom:
            del self._dom
        self._dom = None
        # content = ""
        # try:
        #     with open(file_path, "r") as f:
        #         content = f.read()
        # except:
        #     with open(file_path, "r", encoding="utf-8") as f:
        #         content = f.read()
        # if content:
        #     self._dom = xml.dom.minidom.parseString(content)
        # else:
        #     show_log("Warning: Invalid file content![{}]".format(file_path))
        try:
            self._dom = xml.dom.minidom.parse(file_path)
        except Exception as e:
            real_file_path = self.real_file_path
            show_log("Warning: Failed to parse xml file[{}]!".format(real_file_path))
            show_log("Exception({}) in set_file_path:".format(real_file_path), e, is_output_file=True)
    
    @property
    def file_path(self):
        return self._file_path
    
    @property
    def real_file_path(self):
        return os.path.abspath(self._file_path).replace(RES_PATH, "")
    
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
    
    def save(self):
        if not self._dom:
            return
        content = self._dom.toxml()
        content = content.strip().replace('<?xml version="1.0" ?>', "")
        # with open(self._file_path, "w") as f:
        #     f.write(content)
        # return
    
        content = content.replace(" ", "\n\t")
        content = content.replace("=", " = ")

        tab_str = ""
        new_content = ""
        for line in content.split("\n"):
            line += "\n"
            ret = re.search("^(\t*)<.*$", line)
            if not ret:
                new_content += tab_str + line
                continue
            tab_str = ret.group(1)
            new_content += line

        with open(self._file_path, "w") as f:
            f.write(new_content)


class ModelPosData(XmlParser):
    def __init__(self, gim_path, pos_list=[]):
        super(ModelPosData, self).__init__(gim_path)

        self._pos_list = pos_list

        # self._each_pos_distance = {}

    def check_and_set_enable_hw(self, is_enable_hw, is_save=False):
        root = self.root
        if root:
            is_enable_str = root.getAttribute("HwInstancingEnable")
            cur_is_enable = is_enable_str.lower() == "true"

            is_change = False
            if is_enable_hw:
                if not cur_is_enable:
                    root.setAttribute("HwInstancingEnable", "true")
                    is_change = True
            else:
                if cur_is_enable:
                    root.removeAttribute("HwInstancingEnable")
                    is_change = True
            if is_change:
                if is_save:
                    self.save()  # 保存文件
                return True
        return False

    @staticmethod
    def calc_distance_by_pos(pos_1, pos_2):
        pos_1_x, pos_1_y, pos_1_z = pos_1
        pos_2_x, pos_2_y, pos_2_z = pos_2
        return (pos_2_x - pos_1_x)**2 + (pos_2_z - pos_1_z)**2
    
    # def calc_each_pos_distance(self):
    #     if self._each_pos_distance:
    #         return
    #     for i in range(len(self._pos_list)):
    #         pos_i = self._pos_list[i]
    #         for j in range(i+1, len(self._pos_list)):
    #             pos_j = self._pos_list[j]
    #             self._each_pos_distance[(i, j)] = self.calc_distance_by_pos(pos_i, pos_j)

    # def get_max_count_by_distance(self, distance):
    #     if len(self._pos_list) < 2:
    #         return len(self._pos_list)
        
    #     self.calc_each_pos_distance()

    #     distance_square = distance**2

    #     max_cnt = 0
    #     cnt_dict = {}
    #     for pos_tuple, dist in self._each_pos_distance.items():
    #         if dist > distance_square:
    #             continue
    #         for pos_idx in pos_tuple:
    #             if pos_idx not in cnt_dict:
    #                 cnt_dict[pos_idx] = 1
    #             cnt_dict[pos_idx] += 1
    #             if max_cnt < cnt_dict[pos_idx]:
    #                 max_cnt = cnt_dict[pos_idx]
    #     return max_cnt

    def check_count_by_real_time(self, distance, count):
        if len(self._pos_list) < count:
            return False

        distance_square = distance**2
        
        cnt_dict = {}
        for i in range(len(self._pos_list)):
            pos_i = self._pos_list[i]
            for j in range(i+1, len(self._pos_list)):
                pos_j = self._pos_list[j]

                if self.calc_distance_by_pos(pos_i, pos_j) > distance_square:
                    continue
            
                if i not in cnt_dict:
                    cnt_dict[i] = 1
                cnt_dict[i] += 1
                if cnt_dict[i] >= count:
                    return True
            
                if j not in cnt_dict:
                    cnt_dict[j] = 1
                cnt_dict[j] += 1
                if cnt_dict[j] >= count:
                    return True
        return False


class ScnModelPosData(XmlParser):
    def __init__(self, scn_path=""):
        super(ScnModelPosData, self).__init__(scn_path)

        self._model_pos_dict = {}

        if scn_path:
            self.set_file_path(scn_path)
    
    @property
    def model_pos_dict(self):
        return self._model_pos_dict
    
    @property
    def is_in_content_path(self):
        root = self.root
        if not root:
            return False
        for global_node in root.getElementsByTagName("Global"):
            if global_node.getAttribute("ContentPath"):
                return True
        return False
    
    def set_file_path(self, file_path):
        super(ScnModelPosData, self).set_file_path(file_path)

        self._model_pos_dict = self.get_model_pos_dict()

        scn_content_path = self.get_scn_content_path()
        if scn_content_path:
            self.find_all_model_pos_by_path(scn_content_path)
        
    def get_scn_content_path(self):
        root = self.root
        if not root:
            return []
        scn_header = XmlParser.get_child_by_tag_name(root, "SceneHeader")
        if scn_header:
            content_path = scn_header.getAttribute("ContentPath")
            return os.path.join(RES_PATH, content_path)
        return ""
    
    def get_model_pos_dict(self):
        root = self.root
        if not root:
            return {}
        ret = {}
        for entities in root.getElementsByTagName("Entities"):
            all_file_path = self.get_all_file_path(entities)
            if not all_file_path:
                continue
            all_models_node = XmlParser.get_child_by_tag_name(entities, "Models")
            if not all_models_node:
                return {}
            for child in all_models_node.childNodes:
                if child.nodeType != xml.dom.Node.ELEMENT_NODE:
                    continue
                if child.tagName != "model":
                    continue
                idx_str = child.getAttribute("FilePathIndex")
                if idx_str not in all_file_path:  # 对应模型的路径不存在
                    continue
                file_path = all_file_path[idx_str]
                if file_path not in ret:
                    ret[file_path] = []
                pos_list = self.parse_pos_str(child.getAttribute("Position"))
                if pos_list:
                    ret[file_path].append(pos_list)
                else:
                    show_log("Warning: Invalid model[{}] pos in file[{}]!".format(child.getAttribute("Name"), self.real_file_path))
        return ret
    
    def parse_pos_str(self, pos_str):
        try:
            # 位置为原点时，该属性为空字符
            if not pos_str:
                pos_str = "0,0,0"
            pos_list = pos_str.split(",")
            return [float(pos.strip()) for pos in pos_list]
        except Exception as e:
            print("Exception in parse_pos_str:", e)
        return []

    def get_all_file_path(self, entities_node):
        all_files_node = XmlParser.get_child_by_tag_name(entities_node, "AllFiles")
        if not all_files_node:
            return {}
        ret = {}
        for child in all_files_node.childNodes:
            if child.nodeType != xml.dom.Node.ELEMENT_NODE:
                continue
            idx_str = child.tagName.replace("File_", "")
            file_path = child.getAttribute("Path")
            full_file_path = os.path.join(RES_PATH, file_path)
            if not os.path.exists(full_file_path):
                show_log("Warning: No such file[{}] by handling scn[{}]!".format(file_path, self.real_file_path))
                continue
            ret[idx_str] = full_file_path
        return ret
    
    def find_all_model_pos_by_path(self, content_path):
        smpd = ScnModelPosData()
        for root, _, files in os.walk(content_path):
            for file_name in files:
                _, ext = os.path.splitext(file_name)
                if ext.lower() == ".scn":
                    full_path = os.path.join(root, file_name)
                    smpd.set_file_path(full_path)
                    for file_path, pos_list in smpd.model_pos_dict.items():
                        if file_path not in self._model_pos_dict:
                            self._model_pos_dict[file_path] = []
                        self._model_pos_dict[file_path].extend(pos_list)

    def get_file_list_by_dist_and_cnt(self, dist, cnt):
        file_list = []
        for file_path, pos_list in self._model_pos_dict.items():
            model_pos_data = ModelPosData(file_path, pos_list)
            if not model_pos_data.root:
                continue
            is_enable = model_pos_data.check_count_by_real_time(dist, cnt)
            if model_pos_data.check_and_set_enable_hw(is_enable):
                file_list.append((model_pos_data.real_file_path, is_enable))
        return file_list

    def set_enable_hw_by_dist_and_cnt(self, dist, cnt):
        change_file_list = []
        for file_path, pos_list in self._model_pos_dict.items():
            model_pos_data = ModelPosData(file_path, pos_list)
            if not model_pos_data.root:
                continue
            is_enable = model_pos_data.check_count_by_real_time(dist, cnt)
            if model_pos_data.check_and_set_enable_hw(is_enable, is_save=True):
                change_file_list.append((model_pos_data.real_file_path, is_enable))
        return change_file_list


class ScnModelPosHandler(object):
    HandleCntPerThread = 5  # 每个线程处理scn文件的数量

    def __init__(self):
        super(ScnModelPosHandler, self).__init__()

        self._thread_dict = {}
    
    def has_thread(self):
        if self._thread_dict:
            return True
        return False

    def stop_thread_dict(self):
        for thread in self._thread_dict.values():
            StopThread(thread)
        self._thread_dict = {}

    def get_all_useful_scn_path_list(self):
        script_path = os.path.abspath(os.path.join(RES_PATH, "../script"))
        map_base_info_mod_name = "MapBaseInfo"

        map_base_info_mod_path = "clientdata/_ClientConfigData/{}".format(map_base_info_mod_name)
        map_base_info_file_path = os.path.abspath(os.path.join(script_path, "{}.py".format(map_base_info_mod_path)))
        if not os.path.exists(map_base_info_file_path):
            return []
        path_list = []
        
        is_script_in_sys_path = script_path in sys.path
        if not is_script_in_sys_path:
            sys.path.insert(0, script_path);
        map_base_info_mod = __import__(map_base_info_mod_path.replace("/", "."), fromlist=[map_base_info_mod_name])
        if not is_script_in_sys_path:
            sys.path.remove(script_path);

        map_base_info = getattr(map_base_info_mod, "MapBaseInfo")
        for map_row in map_base_info.all():
            res_psth = map_row.MapResource.replace("\\", "/")
            if res_psth not in path_list:
                path_list.append(res_psth)
        return path_list

    @staticmethod
    def get_all_gim_path_by_scn_path(scn_path, dist, cnt):
        smpd = ScnModelPosData(scn_path)
        file_list = smpd.get_file_list_by_dist_and_cnt(dist, cnt)
        return file_list

    @staticmethod
    def set_enable_hw_by_scn_path(scn_path, dist, cnt):
        smpd = ScnModelPosData(scn_path)
        file_list = smpd.set_enable_hw_by_dist_and_cnt(dist, cnt)
        return file_list

    def check_model_pos_by_scn_list(self, path_list, dist, cnt, is_set_hw=False, thread_idx=-1, thread_callback=None):
        try:
            smpd = ScnModelPosData()
            for path in path_list:
                show_log("Info: Start to check model pos by scn[{}].".format(path))
                scn_path = os.path.join(RES_PATH, path)
                smpd.set_file_path(scn_path)

                if is_set_hw:
                    gim_info_list = smpd.set_enable_hw_by_dist_and_cnt(dist, cnt)
                else:
                    gim_info_list = smpd.get_file_list_by_dist_and_cnt(dist, cnt)
                
                show_log("Info: Change gim file count[{}] in scn[{}]".format(len(gim_info_list), path))
                show_log("Info: Finish to check model pos by scn[{}].\n".format(path))
                try:
                    if callable(thread_callback):
                        thread_callback(False, gim_info_list)
                except Exception as e:
                    show_log("Exception({}) in thread_callback:".format(path), e, is_output_file=True)
        except Exception as e:
            show_log("Exception({}) in check_model_pos_by_scn_list:".format(thread_idx), e, is_output_file=True)
            show_log("Error: Failed to check model pos by scn list[{}]!".format(path_list))

        if thread_idx in self._thread_dict:
            self._thread_dict.pop(thread_idx)

        # 最后必须要回调
        try:
            if callable(thread_callback):
                thread_callback(True, [])
        except Exception as e:
            show_log("Exception in thread_callback:", e, is_output_file=True)

    def start_thread(self, path_list, dist, cnt, is_set_hw=False, thread_idx=-1, thread_callback=None):
        t = threading.Thread(target=self.check_model_pos_by_scn_list, args=(path_list, dist, cnt, is_set_hw, thread_idx, thread_callback))
        t.setDaemon(True)
        t.start()
        self._thread_dict[thread_idx] = t

    def check_model_pos_by_valid_scn(self, dist, cnt, is_set_hw=False, cnt_per_thread=-1, thread_callback=None):
        if cnt_per_thread <= 0:
            cnt_per_thread = self.HandleCntPerThread

        scn_path_list = self.get_all_useful_scn_path_list()
        prev_idx = 0
        thread_cnt = int(math.ceil(len(scn_path_list)/cnt_per_thread))
        for i in range(thread_cnt):
            next_idx = min((i + 1) * cnt_per_thread, len(scn_path_list) - 1)
            path_list = scn_path_list[prev_idx: next_idx+1]
            if not path_list:
                break
            prev_idx = next_idx

            self.start_thread(path_list, dist, cnt, is_set_hw, i, thread_callback)
        
        return len(scn_path_list), len(self._thread_dict)


_app = None
def run_app():
    global _app
    # 加载程序
    _app = MainApp()
    # 运行程序
    _app.mainloop()


# _logger_dir_path = os.path.join(CURRENT_PATH, "log")
# _logger_file_path = os.path.join(_logger_dir_path, "log_batch_static_models_in_scn.txt")
# if not exists(_logger_dir_path):
#     os.makedirs(_logger_dir_path)
# with open(_logger_file_path, "w+") as f:
#     f.write("")  # 清空日志

# def _output_log_to_file(log_text):
#     with open(_logger_file_path, "a+") as f:
#         f.write(log_text)

# 输出日志
def show_log(*args, **kwargs):
    global _app
    args_str = "\n".join(["{}".format(arg) for arg in args]) + "\n"
    if kwargs.get("is_output_file", False):
        # try:
        #     _output_log_to_file(args_str)
        #     if kwargs.get("is_print_when_output", True):
        #         print(args_str)
        # except:
        print(args_str)
        return
    if _app is None:
        print(args_str)
    else:
        _app.show_log(args_str)


if __name__ == "__main__":
    if not re.search(r"res[/\\]?$", RES_PATH):
        print("Invalid Res Path[{}]!".format(RES_PATH))
    print("Try to search gim files in scn by path[{}].".format(RES_PATH))

    # scn_path = os.path.join(RES_PATH, "world/ly_gb_01/ly_gb_01.scn")
    # smpd = ScnModelPosData(scn_path)
    # print(len(smpd.model_pos_dict))
    # for file_path in smpd.model_pos_dict:
    #     if file_path == os.path.abspath(os.path.join(RES_PATH, "levelsets/sc_zc/wj/sc_zc_yd_menkuang_01a.gim")):
    #         model_pos_data = ModelPosData(file_path, smpd.model_pos_dict[file_path])
    #         is_enable = model_pos_data.check_count_by_real_time(300, 5)
    #         model_pos_data.check_and_set_enable_hw(is_enable, is_save=True)

    # scn_path = os.path.join(RES_PATH, "scene/dungeon/dixiatongdao/dixiatongdao.scn")
    # all_gim_path = ScnModelPosHandler.get_all_gim_path_by_scn_path(scn_path, 300, 5)
    # print("========= gim_path =========", len(all_gim_path))

    # gim_path = os.path.join(RES_PATH, "models\dungeon\people\land\people_land_rock_suishiqiang_a.gim")
    # mpld = ModelPosData(gim_path, [])

    # scn_path_list = get_all_useful_scn_path_list()
    # print(len(scn_path_list))

    run_app()
