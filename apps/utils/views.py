from rest_framework.settings import api_settings


class MultipleSerializersMixin:
    serializers = {}

    def get_serializer_class(self):
        if hasattr(self, 'serializers'):
            if self.action in self.serializers:
                return self.serializers[self.action]
        return self.serializer_class


class BaseViewSet(MultipleSerializersMixin):
    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}