# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from .utils import get_experiment_cookie_name


class VariantMiddleware(object):
    def process_request(self, request):
        request.variant_experiments = {}

    def process_response(self, request, response):
        for name, variant in request.variant_experiments.iteritems():
            if variant:
                cookie_name = get_experiment_cookie_name(name)
                response.set_cookie(
                    cookie_name, variant,
                    max_age=getattr(
                        settings, 'VARIANT_MAX_COOKIE_AGE', 2592000),
                    secure=getattr(settings, 'VARIANT_SECURE_COOKIE', False))

        return response
