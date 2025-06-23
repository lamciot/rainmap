from django.urls import path
from . import views

# URLConf
urlpatterns = [
    # path('hello/',views.say_hello,name='base'),
    # path('map/',views.get_mx_data, name='get_mx_data'),
    path('base/',views.show_map, name='base'),
    path('login/',views.login, name='login'),
    path('login/base',views.login_base, name='login_base'),
    path('register/',views.register, name='register'),
    path('form/',views.add_form, name='add_form'),

]
