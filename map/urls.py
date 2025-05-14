from django.urls import path
from . import views

# URLConf
urlpatterns = [
    # path('hello/',views.say_hello,name='base'),
    # path('map/',views.get_mx_data, name='get_mx_data'),
    path('base/',views.base, name='base'),
    path('map/', views.generate_map, name='generate_map'),
    path('map-image/', views.get_map_image, name='get_map_image'),
]
