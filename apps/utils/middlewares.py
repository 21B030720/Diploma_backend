from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.utils.translation import gettext as _
from rest_framework_simplejwt.exceptions import TokenError


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 400:

            if isinstance(response.data, dict):
                messages = response.data
                error_messages = []
                recursion_check_of_exception(messages, error_messages)
                error = '; '.join(error_messages)
                response = Response(data={'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()

            if len(response.data) == 1 and isinstance(response.data, list):
                response = Response(data={'detail': response.data[0]}, status=status.HTTP_400_BAD_REQUEST)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()

            if isinstance(response.data, list):
                messages = response.data
                error_messages = []
                recursion_check_of_exception(messages, error_messages)

                errors_message = '; '.join(error_messages)
                response = Response(data={'detail': errors_message}, status=status.HTTP_400_BAD_REQUEST)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()


            elif len(response.data) > 1 and isinstance(response.data, dict):
                messages = [str(message[0]) for message in response.data.values()]
                error = ' '.join(messages)
                response = Response(data={'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
        return response


def recursion_check_of_exception(messages, error_messages, outer_key=''):
    if isinstance(messages, dict):
        for key, value in messages.items():
            current_messages = value
            if isinstance(current_messages, list):
                for current_message in current_messages:
                    recursion_check_of_exception(current_message, error_messages, key)
            elif isinstance(current_messages, dict):
                recursion_check_of_exception(current_messages, error_messages)
            else:
                error_messages.append(key + ': ' + str(_(current_messages)))
    else:
        if isinstance(messages, list):
            for message in messages:
                recursion_check_of_exception(message, error_messages)
        else:
            error_messages.append(outer_key + ': ' + _(messages))
