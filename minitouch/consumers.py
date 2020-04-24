from channels.generic.websocket import WebsocketConsumer
import socket,struct
from django_redis import get_redis_connection
import socket,struct
con = get_redis_connection('default')
class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port=''
        self.max_x=''
        self.max_y=''
        self.device=''
        self.devoce_json={}

    def connect(self):
        self.accept()


    def disconnect(self, close_code):
        print("minitouch 离开")
        self.close()



    def receive(self, text_data):
        import json
        res=json.loads(text_data)
        # self.port=1111

        if "device"  in res:

            self.device = res['device']
            redis_res = json.loads(con.get(self.device))
            self.devoce_json=redis_res

            self.port = int(redis_res['touchport'])
            self.max_x=redis_res['max_x']
            self.max_y = redis_res['max_y']

        else:

            operation=res['operation']
            x_P=res['xP']
            y_p=res['yP']
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.connect(("localhost", self.port))
            res=c.recv(1024)

            try:
                res = bytes.decode(res)
                print(res, "……………………………………………………………………")
                _, contacts, self.max_x, self.max_y, pressure = (res).split("\n")[1].split(' ')
                self.devoce_json['max_x']=self.max_x
                self.devoce_json ['max_y']= self.max_y
                con.set(self.device,json.dumps(self.devoce_json))
            except:
                print("异常了",res)



            x = int(int(x_P)*(int(self.max_x) / 377))
            y = int(int(y_p)*(int(self.max_y) / 724))

            f = "d 0 {} {} 50\nc\nu 0\nc\n ".format(x, y)
            if operation=="down":
                f="d 0 {} {} 50\nc\n ".format( x,y)

            elif operation=="up":
                f="u 0\nc\n"

            else:
                f="m 0 {} {} 50\nc\n ".format( x,y)
            print(f)
            f = (f.encode('utf-8'))

            c.sendall(f)
            c.close()




