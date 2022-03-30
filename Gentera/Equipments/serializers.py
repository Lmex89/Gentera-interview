from rest_framework import serializers
from . import models as dmodels


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = dmodels.Unit
        fields = ('id', 'unit_str')

class GetTypeDeviceSerialzer(serializers.ModelSerializer):
    
    class Meta:
        model = dmodels.TypeDevice
        fields = ('id', 'name_type')

class GetStatusDeviceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = dmodels.StatusDevice
        fields = ('id','status','description')


class DeviceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = dmodels.Device
        fields = '__all__'
        

class GetDeviceSerializerDetail(serializers.ModelSerializer):
    
    
    class Meta:
        model = dmodels.Device
        fields = '__all__'
        depth = 1
        

class GetBitacoraSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = dmodels.Bitacora
        fields = '__all__'
        depth = 1


class BitacoraSerializer(serializers.ModelSerializer):

    class Meta:
        model = dmodels.Bitacora
        fields = '__all__'

        extra_kwargs = {
            "device": {"required": True},
            "current_potency": {"required": True, "min_value" : 0},
            "type_device": {"required": True}
        }
