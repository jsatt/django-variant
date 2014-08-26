# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.client import RequestFactory
import mox

from variant import utils
from variant.models import Experiment


class GetExperimentVariantTest(TestCase):
    def setUp(self):
        self.experiment = Experiment.objects.create(
            name='test_experiment', active=True)
        self.request = RequestFactory()
        self.request.variant_experiments = {}
        self.request.COOKIES = {}
        self.mock = mox.Mox()
        self.mock.StubOutWithMock(Experiment, 'get_variants')
        self.mock.StubOutWithMock(Experiment, 'choose_variant')
        self.mock.StubOutWithMock(utils, 'get_experiment_cookie_name')

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_first_visit(self):
        utils.get_experiment_cookie_name('test_experiment').AndReturn(
            'dvc_test_experiment')
        Experiment.choose_variant().AndReturn('variant B')

        self.mock.ReplayAll()
        variant = utils.get_experiment_variant(self.request, 'test_experiment')
        self.mock.VerifyAll()

        self.assertEqual(variant, 'variant B')
        self.assertEqual(
            self.request.variant_experiments['test_experiment'], 'variant B')

    def test_invalid_experiment(self):
        self.mock.ReplayAll()
        variant = utils.get_experiment_variant(
            self.request, 'other_experiment')
        self.mock.VerifyAll()

        self.assertIs(variant, None)
        self.assertIs(
            self.request.variant_experiments['other_experiment'], None)

    def test_cookie_set(self):
        self.request.COOKIES['dvc_test_experiment'] = 'variant A'
        utils.get_experiment_cookie_name('test_experiment').AndReturn(
            'dvc_test_experiment')
        Experiment.get_variants().AndReturn(['variant A', 'variant B'])

        self.mock.ReplayAll()
        with self.settings(VARIANT_SETTINGS={'EXPERIMENT_COOKIE': 'dvc_{}'}):
            variant = utils.get_experiment_variant(
                self.request, 'test_experiment')
        self.mock.VerifyAll()

        self.assertEqual(variant, 'variant A')
        self.assertEqual(
            self.request.variant_experiments['test_experiment'], 'variant A')

    def test_cookie_set_invalid_variant(self):
        self.request.COOKIES['dvc_test_experiment'] = 'variant C'
        utils.get_experiment_cookie_name('test_experiment').AndReturn(
            'dvc_test_experiment')
        Experiment.get_variants().AndReturn(['variant A', 'variant B'])
        Experiment.choose_variant().AndReturn('variant A')

        self.mock.ReplayAll()
        with self.settings(VARIANT_SETTINGS={'EXPERIMENT_COOKIE': 'dvc_{}'}):
            variant = utils.get_experiment_variant(
                self.request, 'test_experiment')
        self.mock.VerifyAll()

        self.assertEqual(variant, 'variant A')
        self.assertEqual(
            self.request.variant_experiments['test_experiment'], 'variant A')

    def test_variant_cached(self):
        self.request.variant_experiments['test_experiment'] = 'variant A'

        self.mock.ReplayAll()
        variant = utils.get_experiment_variant(self.request, 'test_experiment')
        self.mock.VerifyAll()

        self.assertEqual(variant, 'variant A')

    def test_middleware_missing(self):
        delattr(self.request, 'variant_experiments')

        self.mock.ReplayAll()
        self.assertRaisesMessage(
            ImproperlyConfigured,
            'VariantMiddleware must be enabled to use Variant experiments.',
            utils.get_experiment_variant, self.request, 'test_experiment')
        self.mock.VerifyAll()


class GetExperimentCookieNameTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_get_cookie_name(self):
        self.mock.StubOutWithMock(utils, 'slugify')
        utils.slugify('dvc_experiment 1').AndReturn('dvc_experiment-1')

        self.mock.ReplayAll()
        with self.settings(VARIANT_EXPERIMENT_COOKIE='dvc_{}'):
            cookie_name = utils.get_experiment_cookie_name('experiment 1')
        self.mock.VerifyAll()

        self.assertEqual(cookie_name, 'dvc_experiment-1')
