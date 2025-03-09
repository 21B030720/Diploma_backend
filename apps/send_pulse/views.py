from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.send_pulse.models import UserCode


# Create your views here.
class ConfirmEmailAPIView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        code = self.request.query_params.get('code')
        user_code = UserCode.objects.filter(user_id=user_id, code=code).first()
        if not user_code:
            raise ValidationError("Given link is expired or invalid, please contact support.")
        elif user_code and user_code.is_confirmed:
            raise ValidationError("You have already successfully confirmed the email.")

        user_code.is_confirmed = True
        user_code.save(update_fields=['is_confirmed'])

        user = user_code.user
        client_user = user.client_user
        client_user.is_email_valid = True
        client_user.save(update_fields=['is_email_valid'])

        return Response({"message": "You have successfully confirmed the email."})
