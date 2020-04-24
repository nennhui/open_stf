from django.shortcuts import render,render_to_response
from django.utils.safestring import mark_safe
# Create your views here.
import json,os
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from run_sft import  devices_info,adb_cmd
from  userapp.views import insert_apk,select_apk
import time
from django_redis import get_redis_connection
import socket,struct
con = get_redis_connection('default')
def standardRes():
    res = {}
    res['status'] = 0
    res['info'] = 'success'
    res['data'] = ''
    return res
def index(request):
    return render(request,"index.html")

"""
:param 获取设备在minitouch 中的最大最小值
"""
def get_maxx_maxy(port):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(("localhost", port))
    res = c.recv(1024)
    res = bytes.decode(res)
    _, contacts, max_x, max_y, pressure = (res).split("\n")[1].split(' ')
    print(max_x,max_y,"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

def stf_deivce(request):
    res=standardRes()
    devicename=request.POST['device']



    if not con.exists('capport'):
            con.set("capport","10000")
            con.set("touchport", "20000")
            capport = "10000"
            touchport = '20000'


    if not con.exists(devicename):

        capport = int(con.get("capport")) + 1
        touchport = int(con.get("touchport")) + 1
        con.set("capport", capport)
        con.set("touchport", touchport)
        con.set(devicename, json.dumps({"capport": capport,
                                        "touchport": touchport,
                                        "islock": "1",
                                        "max_x":"",
                                        "max_y":""
                                        })
                )

    else:
        redis_res = json.loads(con.get(devicename))
        capport = redis_res['capport']
        touchport = redis_res['touchport']

    adb_cmd(devicename,capport,touchport).start_cap()
    adb_cmd(devicename,capport,touchport).start_touch()
    # get_maxx_maxy(touchport)
    return JsonResponse(res
    )



def get_devices(request):
    res=standardRes()
    devices = devices_info()
    res['data']=devices[0]
    res['count'] = devices[1]
    # return JsonResponse(res
    # )
    return JsonResponse(
        {
            "code": 200,
            "message": "查询成功",
            "data":devices[0],
            "count":devices[1]
        })
def room(request, room_name):
    return render(request, 'test.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def test(request):
    return render(request, 'test1.html')
def physical (request):
    """
        获取命令，进行物理操作
    """
    code=request.POST.get('cmd')
    os.system("adb shell input keyevent {}".format(code))
    return JsonResponse({"code":200}
    )

class Keycode():
    home="KEYCODE_HOME"
    menu="187"
    back='KEYCODE_BACK'
    light='224'    #唤起屏幕
    dark='223'     #锁屏


def Ui_Xml(request):
    res = standardRes()
    cmd="adb shell uiautomator dump --compressed"
    os.system(cmd)
    devicename='123'
    cmd="adb pull /sdcard/window_dump.xml {}".format("123.xml")
    print(cmd,"cmd")
    os.system(cmd)
    with open("123.xml",'r',encoding='utf-8') as f:
        res['data'] = f.read()

    return JsonResponse(res
    )

def Activity_Package():
    res = standardRes()
    cmd = "adb shell dumpsys window | findstr mCurrentFocus"
    activity = os.popen(cmd).readlines()[0].split('u0')[1].split('/')[0]
    package = os.popen(cmd).readlines()[0].split('u0')[1].split('/')[1].split('}')[0]
    res['data']={"activity":activity,"package":package}
    return JsonResponse(res
    )

def uploadFile(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        path=os.path.join("E:\\apk", str(time.time())+myFile.name)
        # rsname=str(time.time())+myFile.name
        destination = open(path, 'wb+')  # 打开特定的文件进行二进制的写操作

        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        insert_apk(myFile.name,myFile.size,"123",path)
        # install_apk(path)
        return JsonResponse(
            {
                "code":200,
                "message":"提交成功",
                "data":{},
        })


def install_apk(request):
    # print("adb install {} ".format(path))
    if request.method == "POST":  # 请求方法为POST时，进行处理
        path=request.POST.get('data')
        print(path)
        rs=os.system("adb install -r {} ".format(path))
        print(rs,"安装日志")
    return JsonResponse(
        {
            "code": 200,
            "message": "安装成功",
            "data": {},
        })

def get_hitstory_apk(request):
    rs = select_apk()
    return JsonResponse(
        {
            "code": 200,
            "message": "查询成功",
            "data": {"data": rs},
        })