from rest_framework import serializers
from .models import (Order, Station)

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['name']

class OrderSerializer(serializers.ModelSerializer):
    start_location = StationSerializer()
    end_location = StationSerializer()
    class Meta:
        model = Order
        fields = '__all__'