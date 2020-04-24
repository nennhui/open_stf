#coding:utf-8
import os
import subprocess


def devices_info():
    cmd = "adb devices"
    cmd_respone = os.popen(cmd).readlines()
    print((cmd_respone))

    list=[]
    count=0
    for device in cmd_respone:
        try:
            if device.split('\t')[1]!='\n':
                devices = {}
                devices['device']=device.split('\t')[0]
                devices['stauts']=device.split('\t')[1]
                list.append(devices)
                count+=1
        except:
            # print(devices)
            pass

    return list,count
class adb_cmd():
    def __init__(self,devices_name,capport,touchport):
        self.devices_name=devices_name
        self.capport=str(capport)
        self.touchport=str(touchport)
        cmd_prop = "adb -s " + devices_name+ " shell getprop ro.product.cpu.abi"
        cmd_respone = os.popen(cmd_prop).readlines()
        print(cmd_respone,"调试")
        self.device_type = (cmd_respone[0].split('\n')[0])


    def start_cap(self):
        # 获取手机android api
        cmd_api = 'adb -s ' + self.devices_name + ' shell getprop ro.build.version.sdk'
        cmd_respone = os.popen(cmd_api).readlines()
        device_api = (cmd_respone[0].split('\n')[0])

        # 推送minicap文件到手机
        cmd_push_minicap_so = "adb -s " + self.devices_name + " push" + " ./stf/minicap_so/android-" + device_api + "/" + self.device_type + "/minicap.so" + " /data/local/tmp"
        cmd_respone = os.popen(cmd_push_minicap_so).readlines()
        cmd_push_minicap = "adb -s " + self.devices_name + " push" + " ./stf/stf_libs/" + self.device_type + "/minicap" + " /data/local/tmp"
        cmd_respone = os.popen(cmd_push_minicap).readlines()

        # 添加执行权限
        os.popen("adb  -s " + self.devices_name + "  shell chmod 777 /data/local/tmp/minicap")
        os.popen("adb  -s " + self.devices_name + " shell chmod 777 /data/local/tmp/minicap.so")

        cmd_cap_forward = "adb -s " + self.devices_name + " forward  tcp:" + self.capport + " localabstract:minicap"
        print("xkxkxxxxkx",cmd_cap_forward)
        cmd_respone = os.popen(cmd_cap_forward).readlines()

        cmd_px = "adb -s " + self.devices_name + " shell wm size"
        print("px",cmd_px)
        cmd_respone = os.popen(cmd_px).readlines()[0].split('\n')[0]
        print("输出",cmd_respone)
        device_px = ((cmd_respone).split(":")[1].split('\r')[0].split(' ')[1])
        # 运行minicap
        cmd_run_minicap = " adb -s " + self.devices_name + " shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P %s@%s/0" % (
        device_px, device_px)
        print("www", cmd_run_minicap)
        cmd_respone = os.popen(cmd_run_minicap)

    def start_touch(self):
        # 获取手机内核系统
        print("系统",self.device_type)
        #推送文件到手机
        cmd_push_minitouch = "adb -s " + self.devices_name + " push" + " ./stf/stf_libs/" + self.device_type + "/minitouch" + " /data/local/tmp"
        cmd_respone = os.popen(cmd_push_minitouch).readlines()
        os.popen("adb -s " + self.devices_name + " shell chmod 777 /data/local/tmp/minitouch")

        cmd_run_minitouch = " adb -s " + self.devices_name + " shell  /data/local/tmp/minitouch"

        os.popen(cmd_run_minitouch)


        cmd_touch_forward = "adb -s " + self.devices_name + " forward  tcp:" + self.touchport + " localabstract:minitouch"
        print("www", cmd_touch_forward)
        cmd_respone = os.popen(cmd_touch_forward)
if __name__=="__main__":
    cm=adb_cmd(devices_info())
    cm.start_cap()
    cm.start_touch()
    # get_devices()

