from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('hello/',views.say_hello,name='main'),
    path('map/',views.get_mx_data, name='get_mx_data')
]
