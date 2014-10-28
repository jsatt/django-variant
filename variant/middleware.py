# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
import six

from .utils import get_experiment_cookie_name


class VariantMiddleware(object):
    def process_request(self, request):
        request.variant_experiments = {}

    def process_response(self, request, response):
        experiments = getattr(request, 'variant_experiments', {})

        for name, variant in six.iteritems(experiments):
            if variant:
                cookie_name = get_experiment_cookie_name(name)
                response.set_cookie(
                    cookie_name, variant,
                    max_age=getattr(
                        settings, 'VARIANT_MAX_COOKIE_AGE', 2592000),
                    secure=getattr(settings, 'VARIANT_SECURE_COOKIE', False))

        return response
