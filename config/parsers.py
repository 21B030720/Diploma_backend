import re

from django.http import QueryDict
from nested_multipart_parser.drf import DRF_OPTIONS
from nested_multipart_parser.parser import NestedParser as NestPars
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser

from config import settings


class NestedParser(NestPars):
    def __init__(self, data):
        # merge django settings to default DRF_OPTIONS ( special parser options in on parser)
        options = {
            **DRF_OPTIONS,
            **getattr(settings, "DRF_NESTED_MULTIPART_PARSER", {}),
        }
        super().__init__(data, options)

    def convert_value(self, value):
        if isinstance(value, list) and len(value) == 1:
            return value[0]
        if isinstance(value, list) and len(value) > 0:
            return value
        return value

    @property
    def validate_data(self):
        data = super().validate_data

        # return dict ( not conver to querydict)
        if not self._options["querydict"]:
            return data

        dtc = QueryDict(mutable=True)
        dtc.update(data)
        dtc.mutable = False
        return dtc


class DrfNestedParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):

        clsDataAndFile = super().parse(stream, media_type, parser_context)

        data = dict(clsDataAndFile.data)
        files = dict(clsDataAndFile.files)

        new_data = {}
        new_files = {}

        data_keys_to_remove = []
        files_keys_to_remove = []

        for key in data:
            has_non_empty_brackets = re.search('\[[^\[\]]+\]', key)

            if '[]' in key and has_non_empty_brackets and isinstance(data[key], list):
                data_keys_to_remove.append(key)
                for i in range(len(data[key])):
                    new_key = key.replace("[]", f"[{i}]")
                    new_data[new_key] = data[key][i]

            elif '[]' in key and isinstance(data[key], list):
                data_keys_to_remove.append(key)
                for i in range(len(data[key])):
                    new_data[f'{key.replace("[]", "")}[{i}]'] = data[key][i]

        for key in data_keys_to_remove:
            data.pop(key)

        for key in files:
            if '[]' in key and isinstance(files[key], list):
                files_keys_to_remove.append(key)
                for i in range(len(files[key])):
                    new_files[f'{key.replace("[]", "")}[{i}]'] = files[key][i]

        for key in files_keys_to_remove:
            files.pop(key)

        data = {**data, **new_data, **files, **new_files}

        parser = NestedParser(data)
        if parser.is_valid():
            response = parser.validate_data
            return response
        raise ParseError(parser.errors)
