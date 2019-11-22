from channels.generic.websocket import WebsocketConsumer
import json
import time
import qrcode
import io
import base64

consumerList = [];

class webConsumer(WebsocketConsumer):
    def connect(self):
        self.accept();
        print("connect webConsumer:", self, id(self));
        consumerList.append(self);
        self.send(text_data=json.dumps({"message":id(self)}))

    def disconnect(self, close_code):
        print("disconnect webConsumer:", self);
        consumerList.remove(self);
        pass

    def receive(self, text_data):
        resp = {};
        text_data_json = json.loads(text_data)
        print("text_data:", text_data)
        # 请求二维码
        if text_data_json.get("header", "") == "qrcode":
            resp["header"] = "qrcode";
            qr = qrcode.QRCode(version=10)
            qr.add_data("https://github.com/pytoolsip")
            qr.make(fit=True);
            img = qr.make_image()
            img_buffer = io.BytesIO()
            img.save(img_buffer, 'png')
            imgB64 = base64.b64encode(img_buffer.getvalue())
            img_buffer.close()
            resp["resp"] = imgB64.decode()
        # 返回消息
        message = '信息：' + text_data_json.get('message', resp.get("resp", ""))
        resp["message"] = message;
        self.send(text_data=json.dumps(resp))

        for c in consumerList:
            c.send(text_data=json.dumps({
                'message': '转发->' + message
            }))
        
        if text_data_json.get('message', "") == ":quit()":
            self.close();


# Base WebSocket Consumer
class BaseConsumer(WebsocketConsumer):
    """docstring for BaseConsumer"""
    def __init__(self, *args, baseName = "", **kw):
        super(BaseConsumer, self).__init__(*args, **kw);
        self.__baseName = baseName;
        self.__listeners = {};
        pass;

    def connect(self):
        self.accept();
        if hasattr(self, "onConnect"):
            getattr(self, "onConnect")();
        pass;

    def disconnect(self, close_code):
        if hasattr(self, "onClose"):
            getattr(self, "onClose")(close_code);
        pass;

    def getBaseName(self, suffix = ""):
        return self.__baseName + suffix;

    def updateCtx(self, ctx):
        self.notify("WS_onUpdateCtx", ctx);
        pass;

    def receive(self, text_data):
        data = json.loads(text_data);
        # 校验数据
        if "req" not in data:
            self.notify("WS_onError", "Error! No Req!");
            return;
        if "ctx" not in data:
            self.notify("WS_onError", "Error! No Ctx!");
            return;
        if "msg" not in data:
            self.notify("WS_onError", "Error! No Msg!");
            return;
        # 处理数据
        reqName = data["req"];
        resp, status = {}, "success";
        if reqName in self.__listeners:
            ctx = data["ctx"];
            # 校验上下文内容
            if hasattr(self, "onCheckCtx"):
                if getattr(self, "onCheckCtx")(ctx):
                    resp = self.__listeners[reqName](ctx, data["msg"]);
                else:
                    status = "failure";
            else:
                resp = self.__listeners[reqName](ctx, data["msg"]);
        else:
            status = "failure";
        # 发送消息
        if "resp" in data and data["resp"]:
            self.notify(data["resp"], resp, status = status);
        pass;

    def notify(self, resp, msg, status = "success"):
        self.send(text_data=json.dumps({
            "resp" : resp,
            "msg" : msg,
            "status" : status,
        }));
        pass;

    def register(self, name, func):
        self.__listeners[name] = func;
        pass;

    def unregister(self, name):
        if name in self.__listeners:
            self.__listeners.pop(name);
        pass;


import uuid;

global _LOGIN_ID_DICT;
_LOGIN_ID_DICT = {}; # 登录ID相关表

# Login WebSocket Consumer
class LoginConsumer(BaseConsumer):
    """docstring for LoginConsumer"""
    def __init__(self, *args, **kw):
        super(LoginConsumer, self).__init__(*args, baseName = "", **kw);
        self.__loginID = "";
        self.initListener();
        pass;
    
    def initListener(self):
        for name in ["ReqQrcode"]:
            self.register(name, getattr(self, name));
        pass;

    def __delLoginID__(self):
        global _LOGIN_ID_DICT;
        if self.__loginID in _LOGIN_ID_DICT:
            if self in _LOGIN_ID_DICT[self.__loginID]:
                _LOGIN_ID_DICT[self.__loginID].remove(self);
        pass;

    def __updateLoginID__(self, lid):
        self.__delLoginID__();
        self.__loginID = lid;
        global _LOGIN_ID_DICT;
        if self.__loginID not in _LOGIN_ID_DICT:
            _LOGIN_ID_DICT[self.__loginID] = [];
        _LOGIN_ID_DICT[self.__loginID].append(self);
        pass;

    def onCheckCtx(self, ctx):
        if self.__loginID not in _LOGIN_ID_DICT:
            return False;
        if self.__loginID != ctx.get("loginID", ""):
            return False;
        return True;

    def onClose(self, closeCode):
        self.__delLoginID__();
        pass;
    
    def ReqLoginID(self, ctx, msg):
        # 获取新loginID
        lid = ctx.get("loginID", "");
        if not lid:
            lid = uuid.uuid1();
        global _LOGIN_ID_DICT;
        while lid not in _LOGIN_ID_DICT:
            lid = uuid.uuid1();
        # 更新loginID
        self.__updateLoginID__(lid);
        pass;
    
    def ReqQrcode(self, ctx, msg):
        # 生成二维码
        qr = qrcode.QRCode(version=10);
        # 根据self.__loginID和time.time()生成md5值，保存到redis中，期限为expires
        expires = 120;
        qr.add_data(json.dumps({"login_id" : self.__loginID, "timestamp" : time.time()}));
        qr.make(fit=True);
        img = qr.make_image();
        # 生成base64码
        imgBuffer = io.BytesIO();
        img.save(imgBuffer, "png");
        imgB64 = base64.b64encode(imgBuffer.getvalue());
        imgBuffer.close();
        # 返回数据
        return {
            "qrcode" : imgB64.decode(),
            "expires" : expires,
        };

    def onLogin(self, token):
        self.notify("OnLogin", {"login_token" : token});


# App WebSocket Consumer
class AppConsumer(BaseConsumer):
    """docstring for AppConsumer"""
    def __init__(self, *args, **kw):
        super(AppConsumer, self).__init__(*args, baseName = "", **kw);
        self.initListener();
        pass;
    
    def initListener(self):
        for name in ["LoginWeb", "Login"]:
            self.register(name, getattr(self, name));
        pass;

    def onCheckCtx(self, ctx):
        ctx.user = None;
        token = msg.get("app_token", "");
        # todo:校验token，并获取用户数据
        return True;

    def LoginWeb(self, ctx, msg):
        login_md5 = msg.get("login_md5", "");
        # todo:根据login_md5从redis中获取loginID
        loginID = "";
        if loginID not in _LOGIN_ID_DICT:
            return;
        # 解码App的token为用户名和密码
        uname, upwd = msg.get("app_token", "");
        # todo:验证用户名和密码，并生成网页用的token
        token = "";
        if True: # 如果登录成功，则发送给对应ID的所有登录socket
            for ws in _LOGIN_ID_DICT[loginID]:
                ws.onLogin(token);
        pass;
    
    def Login(self, ctx, msg):
        uname, upwd = msg.get("uname", ""), msg.get("upwd", "");
        # todo:验证用户名和密码，并生成App用的token
        token = "";
        return {
            "app_token" : token,
        };
    
    def Follow(self, ctx, msg):
        if not ctx.user:
            return {"isSuccess" : False};
        return {"isSuccess" : True};