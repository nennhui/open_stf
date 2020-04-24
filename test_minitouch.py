#coding:utf-8
import os
import subprocess

class adb_cmd():
    def __init__(self):
        self.devices=[]

    def get_devices(self):
        cmd="adb devices"
        cmd_respone=os.popen(cmd).readlines()
        print((cmd_respone))

        for  devices in cmd_respone:
            try :
                if devices.split('\t')[1]:
                    self.devices.append(devices.split('\t')[0])
            except:
                pass
        print(self.devices)
    def deivce_Api(self):
        self.get_devices()
        port=1717
        port1=1111
        for device  in self.devices:
            #获取手机android api
            # cmd_api='adb -s '+device +' shell getprop ro.build.version.sdk'
            # cmd_respone=os.popen(cmd_api).readlines()
            # device_api=(cmd_respone[0].split('\n')[0])
            # #获取手机内核系统
            # cmd_prop="adb -s "+device+" shell getprop ro.product.cpu.abi"
            # cmd_respone=os.popen(cmd_prop).readlines()
            # device_type=(cmd_respone[0].split('\n')[0])
            #
            #
            # #推送minitouch到手机
            # cmd_push_minitouch= "adb -s " + device + " push" + " ./stf/stf_libs/" + device_type + "/minitouch"+" /data/local/tmp"
            # cmd_respone = os.popen(cmd_push_minitouch).readlines()
            #
            # #添加执行权限
            #
            # os.popen("adb shell chmod 777 /data/local/tmp/minitouch")
            #
            # #开启端口映射

            # cmd_touch_forward="adb -s " + device + " forward  tcp:"+str(port1) +" localabstract:minitouch"
            # cmd_respone = os.popen(cmd_touch_forward)
            # port1 += port1

            #获取手机分辨率

            cmd_run_minitouch=" adb -s " + device + " shell  /data/local/tmp/minitouch"
            # print("www",cmd_run_minitouch)
            os.popen(cmd_run_minitouch)
import socket
class minitouch():
    BUFFER_SIZE = 4096

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.host, self.port))

    def click(self,x,y):
        f='d 0 {} {} 50\nc\nu 0\nc\n'.format( x, y)
        f = (f.encode('utf-8'))
        print(self.__socket.recv(1024))
        self.__socket.sendall(f)
        print( self.__socket.recv(1024))






if __name__=="__main__":
    adb_cmd().deivce_Api()
    mc = minitouch('localhost', 1111)
    mc.click(400,600)