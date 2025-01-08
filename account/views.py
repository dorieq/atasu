from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from account.serializers import UserSerializer, UserPFPSerializer
from .models import UserModel
from utils.pagination import PageNumberAsLimitOffset
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from drf_yasg.utils import swagger_auto_schema

class UserViewSet(GenericViewSet):
    queryset = UserModel.objects.all()
    pagination_class = PageNumberAsLimitOffset
    parser_classes = [MultiPartParser]

    @action(["get"], detail=False)
    def get_me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(["get"], detail=False)
    def get_users(self, request):
        users = UserModel.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=UserPFPSerializer)
    @action(["post"], detail=False)
    def change_pfp(self, request):
        user = request.user
        user.pfp = request.data['pfp']
        user.save()
        return Response("Updated")