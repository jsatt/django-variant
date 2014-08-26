# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory
import mox

from variant import middleware


class VariantMiddlewareTests(TestCase):
    def setUp(self):
        self.middleware = middleware.VariantMiddleware()
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_process_request(self):
        request = RequestFactory()
        self.middleware.process_request(request)
        self.assertDictEqual(request.variant_experiments, {})

    def test_process_response(self):
        request = RequestFactory()
        request.variant_experiments = {
            'experiment 1': 'variant a',
            'experiment 2': None,
            'experiment 3': 'other variant'}
        mock_response = self.mock.CreateMockAnything()
        self.mock.StubOutWithMock(middleware, 'get_experiment_cookie_name')
        middleware.get_experiment_cookie_name(
            'experiment 1').InAnyOrder().AndReturn('dvc_experiment-1')
        mock_response.set_cookie(
            'dvc_experiment-1', 'variant a', max_age=2600,
            secure=True).InAnyOrder()
        middleware.get_experiment_cookie_name(
            'experiment 3').InAnyOrder().AndReturn('dvc_experiment-3')
        mock_response.set_cookie(
            'dvc_experiment-3', 'other variant', max_age=2600,
            secure=True).InAnyOrder()

        self.mock.ReplayAll()
        with self.settings(
                VARIANT_EXPERIMENT_COOKIE='dvc_{}',
                VARIANT_MAX_COOKIE_AGE=2600, VARIANT_SECURE_COOKIE=True):
            response = self.middleware.process_response(request, mock_response)
        self.mock.VerifyAll()

        self.assertEqual(response, mock_response)
