from django.urls import path
from Equipments import views


urlpatterns = [
    # GET List of all Devices and POST a device
    path('device/', views.DeviceList.as_view()), 
    # GET,PUT, DELETE pk:device
    path('device/<uuid:pk>', views.DeviceDetail.as_view()), 
    # GET all devices by type pk : TypeDevice
    path('device/<uuid:pk>/type_device', views.DevicePerTypeList.as_view()),
    # GET and POST Bitacora items
    path('bitacora/', views.BitacoraList.as_view()), 
    # GET bitacora per pk Device
    path('bitacora/<uuid:pk>/device', views.BitacoraPerDevice.as_view()),
    # GET bitacora per pk TypeDevice
    path('bitacora/<uuid:pk>/type_device',views.BitacoraPerTypeDevice.as_view()),
    # GET bitacora per pk TypeDevice
    path('bitacora/<uuid:pk>/type_device',
         views.BitacoraPerTypeDevice.as_view()),
    #GET List
    path('bitacora-total-energy',
         views.TotalEnergyPerDeviceList.as_view()),
    # GET pk Device
    path('bitacora-total-energy/<uuid:pk>',
         views.TotalEnergyPerDeviceDetail.as_view()),
    
]
