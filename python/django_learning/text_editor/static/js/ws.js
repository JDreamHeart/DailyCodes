$(function(){
    var _appUrl = "";
    var _appName = "";
    var BaseWS = function(name, url, ctx = {}) {
        this._baseName = name;
        this._ws = new WebSocket("ws://" + url);
        this._ctx = ctx; // 上下文内容
        this._listeners = {}; // 消息监听表
        this._listenerIndex = 0; // 消息监听下标
        self.init();
    };
    BaseWS.prototype.newListenerIndex = function() {
        this._listenerIndex ++;
        return this._listenerIndex;
    };
    BaseWS.prototype.getBaseName = function(suffix = "") {
        return this._baseName + suffix;
    };
    BaseWS.prototype.init = function() {
        var self = this;
        // 初始化webSocket
        self._ws.onopen = function(e) {
            if (self.hasOwnProperty("onOpen")) {
                self.onOpen(self);
            }
        };
        self._ws.onclose = function(e) {
            if (self.hasOwnProperty("onClose")) {
                self.onClose(self);
            }
        };
        self._ws.onmessage = function(e) {
            var data = JSON.parse(e.data);
            if (data.hasOwnProperty("resp") && data.hasOwnProperty("status") && data.hasOwnProperty("msg")) {
                var respName = data["resp"];
                if (self._listeners.hasOwnProperty(respName)) {
                    for (fid in self._listeners[respName]) {
                        self._listeners[respName][fid](data["status"], data["msg"]);
                    }
                }
            }
        };
        // 注册基本事件
        self.register("WS_onUpdateCtx", function(status, data){
            for (let key in data) {
                self._ctx[key] = data[key];
            }
        });
        self.register("WS_onError", function(status, data){
            console.error(data);
        });
    };
    BaseWS.prototype.isopen = function() {
        return this._ws.readyState == this._ws.OPEN;
    };
    BaseWS.prototype.close = function() {
        if (this.isopen()) {
            this._ws.close();
            return
        }
    };
    BaseWS.prototype.request = function(reqFuncName, msg, respFuncName) {
        var self = this;
        if (!self.isopen()) {
            console.log("request failed!");
            return
        }
        // 发送消息
        self._ws.send(JSON.stringify({
            "req": reqFuncName,
            "ctx": self._ctx,
            "msg": msg,
            "resp": respFuncName,
        }));
    };
    BaseWS.prototype.register = function(name, func) {
        var self = this;
        if (!self._listeners.hasOwnProperty(name)) {
            self._listeners[name] = {};
        }
        self._listeners[name][self.newListenerIndex()] = func;
    };
    BaseWS.prototype.unregister = function(name, fid) {
        var self = this;
        if (!self._listeners.hasOwnProperty(name)) {
            return false;
        }
        // 移除对应名称的监听表
        if (fid < 0) {
            delete self._listeners[name];
            return true;
        }
        // 移除指定函数
        if (self._listeners[name].hasOwnProperty(fid)) {
            delete self._listeners[name][fid];
            return true;
        }
        return false;
    };
});