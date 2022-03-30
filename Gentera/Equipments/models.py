# sourcery skip: avoid-builtin-shadow
from django.db import models
import uuid
# Create your models here.

class Unit(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    unit_str = models.CharField(max_length=255, null=True, blank=True)

class TypeDevice(models.Model):
    
    AEROGENERATOR = 0
    CELLS = 1
    TURBINE_ENGINES = 2
    NAME_CHOICE = (
        (AEROGENERATOR, 'Autogenerator'),
        (CELLS, 'cells'),
        (TURBINE_ENGINES, 'Turbine engine'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name_type = models.PositiveSmallIntegerField(choices=NAME_CHOICE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class StatusDevice(models.Model):
    
    ON_OPERATION = 0
    MAINTENANCE = 1
    STATUS_CHOICE = (
        (ON_OPERATION, 'on_operation'),
        (MAINTENANCE, 'maintenance'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Device(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name =models.CharField(max_length=255, null=True, blank=True)
    potency = models.IntegerField(default=0)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    type_device = models.ForeignKey(TypeDevice, on_delete=models.SET_NULL, null=True)
    status_device = models.ForeignKey(StatusDevice,on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Bitacora(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)
    type_device = models.ForeignKey(TypeDevice, on_delete=models.SET_NULL, null=True)
    current_potency = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        if self.device.status_device.status == 1 :
            raise ValueError("device status on maintenance cannot have a Bitacora as input")
        if self.current_potency < 0 :
            raise ValueError(
                f"Current potency value needs to be positive number, {self.current_potency} invalid input")
        
        super(Bitacora, self).save(*args, **kwargs)