# -*- coding: utf-8 -*-
import json

from django.conf import settings
from rest_framework.parsers import ParseError
import six

from djangorestframework_camel_case2.settings import api_settings
from djangorestframework_camel_case2.util import underscoreize


class CamelCaseJSONParser(api_settings.PARSER_CLASS):
    json_underscoreize = api_settings.JSON_UNDERSCOREIZE

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            data = stream.read().decode(encoding)
            return underscoreize(json.loads(data), **self.json_underscoreize)
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))
