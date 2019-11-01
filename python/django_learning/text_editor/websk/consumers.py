from channels.generic.websocket import WebsocketConsumer
import json

consumerList = [];

class webConsumer(WebsocketConsumer):
    def connect(self):
        self.accept();
        print("connect webConsumer:", self);
        consumerList.append(self);

    def disconnect(self, close_code):
        print("disconnect webConsumer:", self);
        consumerList.pop(self);
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = '信息：' + text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

        for c in consumerList:
            c.send(text_data=json.dumps({
                'message': '转发->' + message
            }))