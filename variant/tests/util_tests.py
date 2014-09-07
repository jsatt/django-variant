# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.client import RequestFactory

from variant import utils
from variant.models import Experiment

try:
    from unittest import mock
except ImportError:
    import mock


class GetExperimentVariantTest(TestCase):
    def setUp(self):
        self.experiment = Experiment.objects.create(
            name='test_experiment', active=True)
        self.request = RequestFactory()
        self.request.variant_experiments = {}
        self.request.COOKIES = {}
        self.choose_variant_patcher =  mock.patch(
            'variant.models.Experiment.choose_variant')
        self.get_variants_patcher =  mock.patch(
            'variant.models.Experiment.get_variants')
        self.get_cookie_name_patcher = mock.patch(
            'variant.utils.get_experiment_cookie_name')
        self.mock_choose_variant = self.choose_variant_patcher.start()
        self.mock_get_variants = self.get_variants_patcher.start()
        self.mock_get_cookie_name = self.get_cookie_name_patcher.start()

    def tearDown(self):
        self.choose_variant_patcher.stop()
        self.get_variants_patcher.stop()
        self.get_cookie_name_patcher.stop()

    def test_first_visit(self):
        self.mock_get_cookie_name.return_value = 'dvc_test_experiment'
        self.mock_choose_variant.return_value = 'variant B'

        variant = utils.get_experiment_variant(self.request, 'test_experiment')

        self.mock_get_cookie_name.assert_called_once_with('test_experiment')
        self.mock_choose_variant.assert_called_once_with()
        self.assertEqual(variant, 'variant B')
        self.assertEqual(
            self.request.variant_experiments['test_experiment'], 'variant B')

    def test_invalid_experiment(self):
        variant = utils.get_experiment_variant(
            self.request, 'other_experiment')

        self.assertEqual(self.mock_choose_variant.call_count, 0)
        self.assertEqual(self.mock_get_cookie_name.call_count, 0)
        self.assertEqual(self.mock_get_variants.call_count, 0)
        self.assertIs(variant, None)
        self.assertIs(
            self.request.variant_experiments['other_experiment'], None)

    def test_cookie_set(self):
        self.request.COOKIES['dvc_test_experiment'] = 'variant A'
        self.mock_get_cookie_name.return_value = 'dvc_test_experiment'
        self.mock_get_variants.return_value = ['variant A', 'variant B']

        with self.settings(VARIANT_SETTINGS={'EXPERIMENT_COOKIE': 'dvc_{}'}):
            variant = utils.get_experiment_variant(
                self.request, 'test_experiment')

        self.mock_get_cookie_name.assert_called_once_with('test_experiment')
        self.mock_get_variants.assert_called_once_with()
        self.assertEqual(variant, 'variant A')
        self.assertEqual(
            self.request.variant_experiments['test_experiment'], 'variant A')

    def test_cookie_set_invalid_variant(self):
        self.request.COOKIES['dvc_test_experiment'] = 'variant C'
        self.mock_get_cookie_name.return_value = 'dvc_test_experiment'
        self.mock_get_variants.return_value = ['variant A', 'variant B']
        self.mock_choose_variant.return_value = 'variant A'

        with self.settings(VARIANT_SETTINGS={'EXPERIMENT_COOKIE': 'dvc_{}'}):
            variant = utils.get_experiment_variant(
                self.request, 'test_experiment')

        self.mock_get_cookie_name.assert_called_once_with('test_experiment')
        self.mock_get_variants.assert_called_once_with()
        self.mock_choose_variant.assert_called_once_with()
        self.assertEqual(variant, 'variant A')
        self.assertEqual(
            self.request.variant_experiments['test_experiment'], 'variant A')

    def test_variant_cached(self):
        self.request.variant_experiments['test_experiment'] = 'variant A'

        variant = utils.get_experiment_variant(self.request, 'test_experiment')

        self.assertEqual(self.mock_choose_variant.call_count, 0)
        self.assertEqual(self.mock_get_cookie_name.call_count, 0)
        self.assertEqual(self.mock_get_variants.call_count, 0)
        self.assertEqual(variant, 'variant A')

    def test_middleware_missing(self):
        delattr(self.request, 'variant_experiments')

        self.assertRaisesMessage(
            ImproperlyConfigured,
            'VariantMiddleware must be enabled to use Variant experiments.',
            utils.get_experiment_variant, self.request, 'test_experiment')

        self.assertEqual(self.mock_choose_variant.call_count, 0)
        self.assertEqual(self.mock_get_cookie_name.call_count, 0)
        self.assertEqual(self.mock_get_variants.call_count, 0)


class GetExperimentCookieNameTest(TestCase):
    @mock.patch('variant.utils.slugify')
    def test_get_cookie_name(self, mock_slugify):
        mock_slugify.return_value = 'dvc_experiment-1'

        with self.settings(VARIANT_EXPERIMENT_COOKIE='dvc_{}'):
            cookie_name = utils.get_experiment_cookie_name('experiment 1')

        mock_slugify.assert_called_once_with('dvc_experiment 1')
        self.assertEqual(cookie_name, 'dvc_experiment-1')
