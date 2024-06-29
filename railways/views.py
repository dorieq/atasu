from math import sin, cos, sqrt, atan2, radians
import random
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from .models import Order, Train, Station
from .serializers import OrderSerializer


class OrderViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    @action(detail=False, methods=['post'])
    def cost(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid()
        start_location = Station.objects.filter(name=serializer.data['start_location']['name']).first()
        R = 6373.0
        trains = Train.objects.all()
        answer = random.randint(3000000, 7000000)
        count = serializer.data['count']
        for t in trains:
            lat1 = radians(start_location.x_axis)
            lon1 = radians(start_location.y_axis)
            lat2 = radians(t.end_location.x_axis)
            lon2 = radians(t.end_location.y_axis)

            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            if (t.count >= count):
                answer = round(min(answer, distance * count * 1000))
            if (distance == 0):
                answer = round(min(answer, count * (10000)))
        return Response(answer)