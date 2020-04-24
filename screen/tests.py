from django.test import TestCase
import socket,struct
# Create your tests here.
class minitouch():
    BUFFER_SIZE = 4096

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.host, self.port))

    def consume(self):

        f = "d 0 600 2300 50\nc\nu 0\nc\n  "
        # f = "d 0 400 600 100\nc\nu 0\nc\n  "
        f = (f.encode('utf-8'))
        print(f)
        self.__socket.send(f)

    def click(self,x,y):
        f="d 0 {} {} 50\nc\nu 0\nc\n  ".format( x, y)
        f = (f.encode('utf-8'))
        print(f)
        self.__socket.send(f)
    def dowm(self):
        req = struct.pack('ss', )
        self.__socket.send(req)
    def up(self):
        req = struct.pack('l', b"u 0 100 100 500 \n")
        self.__socket.send(req)
