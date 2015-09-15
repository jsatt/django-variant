from django.test import TestCase
import mock

from variant.jinja import experiment_variant


class ExperimentVariantTest(TestCase):
    def test_get_variant(self):
        request = mock.MagicMock()
        context = {'request': request}
        with mock.patch('variant.jinja.get_experiment_variant') as get_var:
            get_var.return_value = 'sample_variant'

            variant = experiment_variant(context, 'experiment1')

        get_var.assert_called_once_with(request, 'experiment1', make_decision=False)
        self.assertEqual(variant, 'sample_variant')

    def test_get_variant_none(self):
        request = mock.MagicMock()
        context = {'request': request}
        with mock.patch('variant.jinja.get_experiment_variant') as get_var:
            get_var.return_value = None

            variant = experiment_variant(context, 'experiment1')

        get_var.assert_called_once_with(
            request, 'experiment1', make_decision=False)
        self.assertEqual(variant, None)

    def test_get_variant_wo_request(self):
        context = {}
        with mock.patch('variant.jinja.get_experiment_variant') as get_var:
            variant = experiment_variant(context, 'experiment1')

        self.assertEqual(get_var.call_count, 0)
        self.assertEqual(
            variant._undefined_hint, 'request must be defined in Context')
