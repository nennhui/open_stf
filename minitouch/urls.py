from . import views
from django.conf.urls import url
urlpatterns = [
url(r'^touch/', views.touch, name='touch'),
url(r'^test/', views.test, name='test'),
]