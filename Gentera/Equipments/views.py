from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from common.pagination import CustomNumberPagination

from . import models as dmodels
from . import serializers as dserializers
from django.db.models import F,Sum

class DeviceList(APIView):
    
    model = dmodels.Device
    
    def get(self, request):
        
        all_items = dmodels.Device.objects.all()
        custom_pagination = CustomNumberPagination()
        items_paginated = custom_pagination.paginate_queryset(
            all_items, request)
        serializer = dserializers.DeviceSerializer(items_paginated, many=True)
        return custom_pagination.get_paginated_response(serializer.data)
        
    def post(self, request):
        
        pot = float(request.data['potency'])
        if pot < 0 :
            return Response(
                dict(
                    sucess=False,
                    errors=[("Equipment can not have potency negatgive")]
                    ),
                status=status.HTTP_400_BAD_REQUEST
                )
            
        serializer = dserializers.DeviceSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                dict(
                    sucess=True,
                    data=serializer.data
                    ),
                status=status.HTTP_200_OK
                )
            
        return Response(
            dict(
                sucess=False,
                errors=[x[0] for x in serializer.errors.values()]
                ),
            status=status.HTTP_400_BAD_REQUEST
            )
        
class DeviceDetail(APIView):
    model = dmodels.Device
    
    def get(self, request, pk):
        
        item = dmodels.Device.objects.filter(pk=pk).first()
        
        if item is None:
            return Response(
                dict(
                    sucess=False,
                    errors=["invalid id Device"]
                )
            )
        serializer = dserializers.DeviceSerializer(item)
        
        return Response(
            dict(
                sucess=True,
                data=serializer.data
                ),
            status=status.HTTP_200_OK
            )
        
        
    def put(self, request,pk):
        
        item = dmodels.Device.objects.filter(pk=pk).first()

        if item is None:
            return Response(
                dict(
                    sucess=False,
                    errors=["invalid id Device"]
                    ),
                status=status.HTTP_400_BAD_REQUEST
                )
        serializer = dserializers.DeviceSerializer(
            item, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
        
            return Response(
                dict(
                    sucess=True,
                    data=serializer.data
                    ),
                status=status.HTTP_200_OK
                )
            
        return Response(
            dict(
                sucess=False,
                errors=[serializer.errors]
                ),
            status=status.HTTP_400_BAD_REQUEST
            )
        
    def delete(self, request, pk):
        
        item = dmodels.Device.objects.filter(pk=pk).first()

        if item is None:
            return Response(
                dict(
                    sucess=False,
                    errors=["invalid id Device"]
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        item.delete()
        
        return Response(
            dict(
                sucess=True,
                ),
            status=status.HTTP_204_NO_CONTENT
            )

class DevicePerTypeList(APIView):
    
    model = dmodels.TypeDevice
    
    def get(self,request, pk):
        
        all_devices_per_type = dmodels.Device.objects.fitler(type_device=pk).select_related(
            'type_device'
        )
        serializer = dserializers.DeviceSerializer(all_devices_per_type,many=True)
        
        return Response(
            dict(
                sucess=True,
                data=serializer.data
                ),
            status=status.HTTP_200_OK
            )
    
class BitacoraList(APIView):
    model = dmodels.Bitacora
    
    def get(self, request):
        
        all_items_bitacora = dmodels.Bitacora.objects.all()
        
        custom_pagination = CustomNumberPagination()
        items_paginated = custom_pagination.paginate_queryset(
            all_items_bitacora, request)
        serializer = dserializers.GetBitacoraSerializer(all_items_bitacora, many=True)
        return custom_pagination.get_paginated_response(serializer.data)


        
    def post(self, request):
        
        request_data = request.data 
        serializer = dserializers.BitacoraSerializer(data=request_data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    dict(
                        sucess=True,
                        data=serializer.data
                        ),
                    status=status.HTTP_200_OK
                    )
            return Response(
                dict(
                    sucess=False,
                    errors=[serializer.errors]
                    ),
                status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as error:
            return Response(
                dict(
                    sucess=False,
                    errors=[str(error)]
                    ),
                status=status.HTTP_400_BAD_REQUEST
                )

class BitacoraPerDevice(APIView):
    model = dmodels.Bitacora
    
    def get(self, request, pk):
        
        item_bitacora = dmodels.Bitacora.objects.filter(device=pk)
        serializer = dserializers.GetBitacoraSerializer(
            item_bitacora, many=True)
        return Response(
            dict(
                sucess=True,
                data=serializer.data
                ),
            status=status.HTTP_200_OK
            )

class BitacoraPerTypeDevice(APIView):
    model = dmodels.Bitacora

    def get(self, request, pk):

        item_bitacora = dmodels.Bitacora.objects.filter(type_device=pk)
        serializer = dserializers.GetBitacoraSerializer(
            item_bitacora, many=True)
        return Response(
            dict(
                sucess=True,
                data=serializer.data
            ),
            status=status.HTTP_200_OK
        )

def get_total_energy(device: dmodels.Device) -> dict:
    
    return dmodels.Bitacora.objects.filter(
        device=device
    ).aggregate(
        total_energy=Sum(F('current_potency'))
    )


class TotalEnergyPerDeviceList(APIView):
    
    model = dmodels.Bitacora
    
    def get(self, request):
                       
        all_devices = dmodels.Device.objects.all().distinct()
        data =[]
        for device in all_devices:
            bitacora_device = get_total_energy(device=device)
            data.append(
                {'device': device.pk, 'total_energy':bitacora_device.get('total_energy')}
                )
        
        return Response(
            dict(
                sucess=True,
                data=data
                ),
            status=status.HTTP_200_OK
            )
            

class TotalEnergyPerDeviceDetail(APIView):
    model = dmodels.Bitacora
    
    def get(self, request, pk):
        device_item = dmodels.Device.objects.filter(pk=pk).first()
        
        if device_item is None:
            return Response(
                dict(
                    sucess=False,
                    errors=["Id Device invalid"]
                    ),
                status=status.HTTP_400_BAD_REQUEST
                )
            
        bitacora_device = get_total_energy(device=device_item)
        data = {
            'device': device_item.pk,
            'total_energy': bitacora_device.get('total_energy')
            }
        return Response(
            dict(
                sucess=True,
                data=data
                ),
            status=status.HTTP_200_OK
            )
