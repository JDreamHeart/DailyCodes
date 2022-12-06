# -*- coding: utf-8 -*-

import os
import re
import sys
import json
try:
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
except:
    from Tkinter import *
    from Tkinter import ttk
    import tkMessageBox as messagebox


# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
# res文件路径
RES_PATH = os.path.abspath(os.path.join(CURRENT_PATH, ".."))

DefaultConfig = {
    # "start_way_text_config": {},
    "start_way_order": ["normal", "fast", "unisdk"],
    "server_dict": {
        # "0": {
        #     "normal": "--ip=xxx --port=xx",
        #     "fast": "-dlogin:xxx@xx",
        # },
        # "1": {
        #     "unisdk": "--ip=xxx --port=xx --verify_flag=??",
        # },
    },
    "server_key_group": [
        # {
        #     "name": "test",
        #     "keys": ["0"],
        # },
    ],
}

DefaultSaveConfig = {
    "default_server_key": "",
    "default_server_group_idx": 0,
    "default_start_way": "",
    "default_test_account": "",
}

DefaultStartWayTextConfig = {
    "normal": "正常启动（选服）",
    "fast": "快速启动（直接选角）",
    "unisdk": "UniSDK启动",
}

DefaultTestStartWayConfig = [
    "normal",
    "fast",
]

ConfigPath = "start_client_config.json"
SaveConfigPath = "data/start_client_save_config.json"

# 获取配置
def readCfg(json_path, default_cfg={}):
    cfg = default_cfg;
    if os.path.exists(json_path):
        with open(json_path, "rb") as f:
            cfg = json.load(f);
    return cfg;


# 保存配置
def saveCfg(cfg, json_path):
    with open(json_path, "wb") as f:
        f.write(json.dumps(cfg, sort_keys=True, indent=2, separators=(',', ':')).encode("utf-8"));


# 运行命令
def runCmd(cmd):
    code = os.system(cmd);
    if code != 0:
        raise Exception("Run cmd failed! [code:{}]".format(code))


class MainApp(Tk):
    AppTitle = "启动客户端"
    AppSize = (900, 400)

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
        if not messagebox.askokcancel(title="退出启动客户端程序", message="是否确认退出启动客户端程序？"):
            return
        self.destroy()

    def show_log(self, log):
        self._win.output_text(log)


class MainWin(Frame):
    def __init__(self, app):
        Frame.__init__(self, app)
        self._app = app
        self.pack(expand=YES, fill=BOTH)
        
        self._cfg = readCfg(ConfigPath, DefaultConfig)
        self._save_cfg = readCfg(SaveConfigPath, DefaultSaveConfig)
        self._key_group_cfg = self._cfg.get("server_key_group", [])
        self._start_way_text_cfg = self._cfg.get("start_way_text_config", DefaultStartWayTextConfig)

        self._server_keys = tuple(self._cfg.get("server_dict", {}).keys())
        self._cur_server_cfg = []  # 当前选中服务器的配置
        self._cur_start_ways = []  # 当前选中服务器的可启动方式

        self._init_win()

    def _init_win(self):
        self._create_server_key_group()
        self._create_params_frame()
        self._create_ctrl_frame()

        self._refresh_server_key_combobox()

        self._output_text = Text(self, width=MainApp.AppSize[0], height=300)
        self._output_text.pack(side=TOP, fill=X, padx=5, pady=5)

    def _get_srv_cfg(self, srv_key):
        return self._cfg.get("server_dict", {}).get(srv_key, {})

    def _get_start_way_text(self, srv_key):
        return self._start_way_text_cfg.get(srv_key, srv_key)

    def _create_combobox(self, parent, text, is_expand_cmb, *args, **kwargs):
        field = Frame(parent)
        field.pack(side=LEFT, fill=X, padx=5, pady=5)

        lab = Label(field, text=text, anchor=W)
        lab.pack(side=LEFT)
        cmb = ttk.Combobox(field, *args, **kwargs)
        if is_expand_cmb:
            cmb.pack(side=LEFT, expand=YES, fill=X)
        else:
            cmb.pack(side=LEFT, fill=X)
        return cmb
    
    def _create_entry(self, parent, text, is_expand_entry, *args, **kwargs):
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
        frame = Frame(self, borderwidth = 1, relief = GROOVE)
        frame.pack(side=TOP, fill=X, padx=5, pady=5)
        
        Label(frame, text="【请选择服务器和启动方式】 ").pack(side=LEFT)

        key_var = StringVar()
        self._key_cmb = self._create_combobox(frame, "服务器：", False, textvariable=key_var)
        self._key_cmb.bind("<<ComboboxSelected>>", self._on_change_server)

        start_way_var = StringVar()
        self._start_way_cmb = self._create_combobox(frame, "启动方式：", False, textvariable=start_way_var)
        self._start_way_cmb.bind("<<ComboboxSelected>>", self._on_change_start_way)

        self._test_account_var = StringVar()
        self._test_account_var.set(self._save_cfg.get("default_test_account", ""))
        self._test_account_entry = self._create_entry(frame, "默认测试账号：", False, textvariable=self._test_account_var)

        return frame
    
    def _create_ctrl_frame(self):
        frame = Frame(self, borderwidth = 1, relief = GROOVE);
        frame.pack(side=TOP, fill=X, padx=10, pady=10);

        self._ctrl_btn = Button(frame, width = 40, command=self._on_handle)
        self._ctrl_btn["text"] = "启动"
        self._ctrl_btn.pack(side=TOP, pady=10)

        return frame

    def _get_start_way(self):
        start_way_idx = self._start_way_cmb.current()
        if 0 <= start_way_idx < len(self._cur_start_ways):
            return self._cur_start_ways[start_way_idx]
        return ""

    def _refresh_test_account_entry(self, start_way):
        if start_way in DefaultTestStartWayConfig:
            self._test_account_entry.pack(side=TOP, fill=X, padx=5, pady=5);
            return
        self._test_account_entry.forget()

    def _create_server_key_group(self):
        frame = Frame(self, borderwidth = 1, relief = GROOVE)
        frame.pack(side=TOP, fill=X, padx=5, pady=5)

        self._key_group_idx = IntVar()

        default_index = self._save_cfg.get("default_server_group_idx", 0)
        if 0 <= default_index <= len(self._key_group_cfg):
            self._key_group_idx.set(default_index)
        else:
            self._key_group_idx.set(0)
        
        for i, key_group in enumerate(self._key_group_cfg):
            Radiobutton(frame, text=key_group.get("name", "Unknow"), variable=self._key_group_idx, value=i, command=self._refresh_server_key_combobox).pack(side=LEFT, padx=10, anchor=W)

        # 显示所有
        Radiobutton(frame, text="All", variable=self._key_group_idx, value=len(self._key_group_cfg), command=self._refresh_server_key_combobox).pack(side=LEFT, padx=10, anchor=W)

    def _refresh_server_key_combobox(self, *args):
        key_group_idx = self._key_group_idx.get()
        self._save_config("default_server_group_idx", key_group_idx)

        if 0 <= key_group_idx < len(self._key_group_cfg):
            srv_keys = self._key_group_cfg[key_group_idx].get("keys", [])
        else:
            srv_keys = self._server_keys
        # 刷新选项
        self._key_cmb["value"] = tuple(srv_keys)
        # 默认选项
        default_index = -1
        for i, srv_key in enumerate(srv_keys):
            if srv_key == self._save_cfg.get("default_server_key", ""):
                default_index = i
                break
        if default_index < 0 and len(srv_keys) > 0:
            default_index = 0
        if default_index >= 0:
            self._key_cmb.current(default_index)
        else:
            self._key_cmb.set("")
        self._on_change_server()

    def _on_change_server(self, *args):
        server_key = self._key_cmb.get()
        self._save_config("default_server_key", server_key)

        self._cur_server_cfg = self._get_srv_cfg(server_key)
        self._cur_start_ways = []

        default_index = -1
        start_way_values = []
        for start_way in self._cfg.get("start_way_order", self._cur_server_cfg.keys()):
            if start_way in self._cur_server_cfg:
                if start_way == self._save_cfg.get("default_start_way", ""):
                    default_index = len(start_way_values)
                start_way_values.append(self._get_start_way_text(start_way))
                self._cur_start_ways.append(start_way)

        self._start_way_cmb["value"] = tuple(start_way_values)

        if default_index < 0 and len(start_way_values) > 0:
            default_index = 0
        if default_index >= 0:
            self._start_way_cmb.current(default_index)
        else:
            self._start_way_cmb.set("")
        self._on_change_start_way()

    def _on_change_start_way(self, *args):
        start_way = self._get_start_way()
        self._save_config("default_start_way", start_way)

        self._refresh_test_account_entry(start_way)

    def _save_config(self, key, val):
        if self._save_cfg.get(key, None) == val:
            return False
        self._save_cfg[key] = val
        saveCfg(self._save_cfg, SaveConfigPath)
        return True

    def _set_default_test_account(self, test_account):
        if self._save_config("default_test_account", test_account):
            with open("auto_fill", "w") as f:
                f.write(test_account);

    def _on_handle(self):
        if not self._key_cmb.get():
            messagebox.showerror(title="参数错误", message="请选择服务器！")
            return
        if not self._cur_server_cfg:
            messagebox.showerror(title="参数错误", message="服务器配置（{}）不能为空！".format(self._cur_server_cfg))
            return

        if not self._start_way_cmb.get():
            messagebox.showerror(title="参数错误", message="请选择启动方式！")
            return
        if not self._cur_start_ways:
            messagebox.showerror(title="参数错误", message="启动方式配置（{}）错误！".format(self._cur_start_ways))
            return

        # 保存测试账号信息
        self._set_default_test_account(self._test_account_var.get())

        # 运行启动指令
        start_way = self._get_start_way()
        runCmd("start client_x64\client.exe {}".format(self._cur_server_cfg[start_way]))

        # 输出日志
        self.output_text("正在启动客户端[{}]...".format(self._cur_server_cfg[start_way]))

    def output_text(self, text):
        self._output_text.insert(END, text)
        self._output_text.insert(END, "\n")
        self._output_text.see(END)


_app = None
def run_app():
    global _app
    # 加载程序
    _app = MainApp()
    # 运行程序
    _app.mainloop()


if __name__ == "__main__":
    run_app()