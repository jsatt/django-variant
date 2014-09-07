# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from variant import models

try:
    from unittest import mock
except ImportError:
    import mock


class ExperimentModelTests(TestCase):
    def setUp(self):
        self.experiment = models.Experiment(
            name='test_1', variants='variant A\nvariant B \n variant C')

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

    @mock.patch('variant.models.random')
    @mock.patch('variant.models.Experiment.get_variants')
    def test_choose_variants(self, mock_get_variants, mock_random):
        mock_get_variants.return_value = [
            'variant A', 'variant B', 'variant C']
        mock_random.choice.return_value = 'variant B'

        choice = self.experiment.choose_variant()

        self.experiment.get_variants.assert_called_once_with()
        models.random.choice.assert_called_once_with(
            ['variant A', 'variant B', 'variant C'])
        self.assertEqual(choice, 'variant B')
