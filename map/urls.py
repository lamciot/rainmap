from django.urls import path
from . import views

# URLConf
urlpatterns = [
    # path('hello/',views.say_hello,name='main'),
    # path('map/',views.get_mx_data, name='get_mx_data'),
    path('main/',views.main, name='get_mx_data'),
    path('generate-map/', views.generate_map, name='generate_map'),
]
