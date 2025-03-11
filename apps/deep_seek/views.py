from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.deep_seek.serializers import SendMessageSerializer
from apps.deep_seek.services import test_deep_sekk


# Create your views here.
class DeepSeekAPIView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(request_body=SendMessageSerializer())
    def post(self, request):
        data = request.data
        serializer = SendMessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        test_deep_sekk(serializer.validated_data.get('message'))
        return Response(status=status.HTTP_200_OK)
