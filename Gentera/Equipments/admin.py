from django.contrib import admin

# Register your models here.
from .models import Unit,Device,TypeDevice,StatusDevice
admin.site.register(Unit)
admin.site.register(Device)
admin.site.register(TypeDevice)
admin.site.register(StatusDevice)

