from . import views
from django.conf.urls import url
urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^test', views.test, name='test'),
    url(r'^getdevice', views.get_devices, name='getdevice'),
    url(r'^stfdevice', views.stf_deivce, name='rundevice'),
    url(r'^physicaldevice', views.physical, name='physicaldevice'),
    url(r'^uixml', views.Ui_Xml, name='uixml'),
    url(r'^get_hitstory_apk', views.get_hitstory_apk, name='get_hitstory_apk'),
    url(r'^uploadFile', views.uploadFile, name='uploadFile'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'^install_apk', views.install_apk, name='install_apk'),


]