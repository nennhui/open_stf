from django.db import models

# Create your models here.

class UsersInfo(models.Model):
 #创建表的字段
 username = models.CharField(max_length=16) #创建一个字段，类型为字符串类型，最大长度为16
 password = models.CharField(max_length=32) #创建一个字段，类型为字符串类型，最大长度为32



class History_apk(models.Model):
    apk_name=models.CharField(max_length=1000)
    apk_version=models.CharField(max_length=100)
    apk_size=models.CharField(max_length=100,null=True)
    apk_addr = models.ImageField( upload_to='apk',null=True)
    createtime=models.DateTimeField(auto_now_add=True,null=True)



class devices(models.Model):
    device_brand=models.CharField(max_length=100,null=True)
    device_model=models.CharField(max_length=100,null=True)
    device_size=models.CharField(max_length=100,null=True)
    device_cpu = models.CharField( max_length=100,null=True)
    device_sdk=models.CharField( max_length=100,null=True)
    status=models.IntegerField( default=0)
    createtime=models.DateTimeField(auto_now_add=True,null=True)


