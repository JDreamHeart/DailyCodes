from channels.generic.websocket import WebsocketConsumer
import json

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