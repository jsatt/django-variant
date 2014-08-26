# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import mox

from variant import models


class ExperimentModelTests(TestCase):
    def setUp(self):
        self.experiment = models.Experiment(
            name='test_1', variants='variant A\nvariant B \n variant C')
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_get_variants(self):
        variants = self.experiment.get_variants()
        self.assertSequenceEqual(
            variants, ['variant A', 'variant B', 'variant C'])
        self.assertSequenceEqual(
            self.experiment._variant_cache,
            ['variant A', 'variant B', 'variant C'])

    def test_get_variants_memoized(self):
        self.experiment._variant_cache = [
            'variant A', 'variant B', 'variant C', 'variant D']
        variants = self.experiment.get_variants()
        self.assertSequenceEqual(
            variants, ['variant A', 'variant B', 'variant C', 'variant D'])
        self.assertSequenceEqual(
            self.experiment._variant_cache,
            ['variant A', 'variant B', 'variant C', 'variant D'])

    def test_choose_variants(self):
        self.mock.StubOutWithMock(self.experiment, 'get_variants')
        self.mock.StubOutWithMock(models.random, 'choice')
        self.experiment.get_variants().AndReturn(
            ['variant A', 'variant B', 'variant C'])
        models.random.choice(
            ['variant A', 'variant B', 'variant C']).AndReturn('variant B')

        self.mock.ReplayAll()
        choice = self.experiment.choose_variant()
        self.mock.VerifyAll()

        self.assertEqual(choice, 'variant B')
