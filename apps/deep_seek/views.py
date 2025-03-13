from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.deep_seek.serializers import SendMessageSerializer
from apps.deep_seek.services import get_message_from_assistant
from apps.utils.swagger_params import openai_library_param


# Create your views here.
class OpenAiAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=SendMessageSerializer(),
                         responses={
                             200: SendMessageSerializer(),
                         },
                         manual_parameters=[
                             openai_library_param
                         ])
    def post(self, request):
        library_name = request.data.get('library', 'openai')
        data = request.data
        serializer = SendMessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data.get('message')
        result = get_message_from_assistant(message, library_name)
        serializer = SendMessageSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
