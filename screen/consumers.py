from channels.generic.websocket import WebsocketConsumer
import json,six
from io import  BytesIO
import socket,struct
from collections import OrderedDict
import  threading,ctypes
import inspect
from run_sft import adb_cmd
from django_redis import get_redis_connection
import socket,struct
con = get_redis_connection('default')
class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.t=""
    def connect(self):
        self.accept()
        print("cap 链接")

    def disconnect(self, close_code):
        print(type(self.t),"……")
        if type(self.t)==type('str'):
            return 0
        print("关闭时", self.t)
        if not  self.t.is_alive():
            return 0
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.t.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.t.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
        self.close()


    def receive(self, text_data):
        port=int(json.loads(con.get(text_data))['capport'])
        print(port,"************************************")
        t=threading.Thread(target=self.send_cap,args=(self,port,))
        t.start()
        self.t=t
        import os
        print("存入",self.t,os.getpid())

    def send_cap(self,xx,port):
        Minicap('localhost', port, Banner()).consume(xx)


class Banner:
    def __init__(self):
        self.__banner = OrderedDict(
            [('version', 0),
             ('length', 0),
             ('pid', 0),
             ('realWidth', 0),
             ('realHeight', 0),
             ('virtualWidth', 0),
             ('virtualHeight', 0),
             ('orientation', 0),
             ('quirks', 0)
             ])
    def __setitem__(self, key, value):
        self.__banner[key] = value
    def __getitem__(self, key):
        return self.__banner[key]
    def keys(self):
        return self.__banner.keys()
    def __str__(self):
        return str(self.__banner)
class Minicap(object):
    BUFFER_SIZE = 4096
    def __init__(self, host, port,banner):
        self.host = host
        self.port = port
        self.banner = banner
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.host, self.port))
    def consume(self,s):
        print("#############################################################")
        readBannerBytes = 0
        bannerLength = 24
        readFrameBytes = 0
        frameBodyLength = 0
        data = []
        while 1:
            chunk = self.__socket.recv(self.BUFFER_SIZE)
            cursor = 0
            buf_len = len(chunk)
            while cursor < buf_len:
                if readBannerBytes < bannerLength:
                    map(lambda i, val: self.banner.__setitem__(self.banner.keys()[i], val),
                        [i for i in range(len(self.banner.keys()))], struct.unpack("<2b5ibB", chunk))
                    cursor = buf_len
                    readBannerBytes = bannerLength
                elif readFrameBytes < 4:
                    frameBodyLength += (struct.unpack('B', six.int2byte(chunk[cursor]))[0] << (readFrameBytes * 8)) >> 0
                    cursor += 1
                    readFrameBytes += 1
                else:
                    if buf_len - cursor >= frameBodyLength:
                        data.extend(chunk[cursor:cursor + frameBodyLength])
                        buffer = BytesIO()
                        buffer.write(bytes(data))
                        s.send( bytes_data = buffer.getvalue())

                        cursor += frameBodyLength
                        frameBodyLength = readFrameBytes = 0
                        data = []
                    else:
                        data.extend(chunk[cursor:buf_len])
                        frameBodyLength -= buf_len - cursor
                        readFrameBytes += buf_len - cursor
                        cursor = buf_len
