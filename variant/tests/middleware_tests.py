# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory

from variant import middleware

try:
    from unittest import mock
except ImportError:
    import mock


class VariantMiddlewareTests(TestCase):
    def setUp(self):
        self.middleware = middleware.VariantMiddleware()

    def test_process_request(self):
        request = RequestFactory()
        self.middleware.process_request(request)
        self.assertDictEqual(request.variant_experiments, {})

    @mock.patch('variant.middleware.get_experiment_cookie_name')
    def test_process_response(self, mock_cookie_name):
        request = RequestFactory()
        request.variant_experiments = {
            'experiment 1': 'variant a',
            'experiment 2': None,
            'experiment 3': 'other variant'}

        def mock_cookie_name_side_effect(key):
            if key == 'experiment 1':
                return 'dvc_experiment-1'
            elif key == 'experiment 3':
                return 'dvc_experiment-3'
        mock_cookie_name.side_effect = mock_cookie_name_side_effect
        mock_response = mock.Mock()

        with self.settings(
                VARIANT_EXPERIMENT_COOKIE='dvc_{}',
                VARIANT_MAX_COOKIE_AGE=2600, VARIANT_SECURE_COOKIE=True):
            response = self.middleware.process_response(request, mock_response)

        mock_cookie_name.assert_has_calls(
            (mock.call('experiment 1'), mock.call('experiment 3')),
            any_order=True)
        mock_response.set_cookie.assert_has_calls((
            mock.call('dvc_experiment-1', 'variant a', max_age=2600,
                      secure=True),
            mock.call('dvc_experiment-3', 'other variant', max_age=2600,
                      secure=True),),
            any_order=True)
        self.assertEqual(response, mock_response)
