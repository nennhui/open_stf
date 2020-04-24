from django.shortcuts import render

# Create your views here.
import  requests

from userapp.models import  *
import json
from django.core import serializers
def insert_apk(apk_name,apk_size,apk_version,apk_addr):
    userinfo=History_apk()
    userinfo.apk_name=apk_name
    userinfo.apk_size=apk_size
    userinfo.apk_version=apk_version
    userinfo.apk_addr=apk_addr
    userinfo.save()

def select_apk():
    rs=History_apk.objects.order_by('-id')[:10].values()
    rs = list(rs)
    return rs

def insert_device(device):
    device_cpu="adb -s {} shell getprop ro.product.cpu.abi ".format(device)  #cpu型号
    device_sdk="adb -s {} shell getprop ro.build.version.sdk ".format(device) #版本号
    device_brand="adb -s {} shell getprop ro.product.brand ".format(device)  #品牌
    device_model="adb -s {} shell getprop ro.product.model ".format(device)     #手机型号
    device_size = "adb -s {} shell wm size ".format(device)  # 分辨率

    devices.device_cpu=device_cpu
    devices.device_sdk=device_sdk
    devices.device_brand=device_brand
    devices.device_model=device_model
    devices.device_size=device_size
    devices.save()

