from django.test import TestCase
from django.views.generic import TemplateView
import mock

from variant import mixins


class VariantTestMixinTest(TestCase):
    class TestView(mixins.VariantTestMixin, TemplateView):
        pass

    def setUp(self):
        self.view = self.TestView()

    def test_init(self):
        self.assertEqual(self.view.variants, {})

    def test_dispatch(self):
        request = mock.MagicMock()
        with mock.patch(
                'django.views.generic.TemplateView.'
                'dispatch') as super_dispatch:
            with mock.patch(
                    'variant.mixins.VariantTestMixin.'
                    'set_variants') as set_variant_mock:
                self.view.dispatch(request)

        set_variant_mock.assertCalledOnce()
        super_dispatch.assertCalledOnce()

    def test_get_context_data(self):
        self.view.variants = {'test1': 'old', 'test2': 'new'}
        with mock.patch(
                'django.views.generic.TemplateView.'
                'get_context_data') as super_ctx:
            self.view.get_context_data()

        super_ctx.assert_called_once_with(
            variants={'test1': 'old', 'test2': 'new'})

    def test_set_variants(self):
        self.view.experiments = ['experiment1', 'test2', 'disabled']
        request = self.view.request = mock.MagicMock()
        with mock.patch('variant.mixins.get_experiment_variant') as get_var:
            get_var.side_effect = ['variant1', 'otherthing', None]

            self.view.set_variants()

        self.assertEqual(
            get_var.mock_calls,
            [mock.call(request, 'experiment1'),
             mock.call(request, 'test2'),
             mock.call(request, 'disabled')])
        self.assertEqual(
            self.view.variants,
            {'experiment1': 'variant1', 'test2': 'otherthing'})

    def test_set_variants_wo_experiments(self):
        self.view.experiments = []
        with mock.patch('variant.mixins.get_experiment_variant') as get_var:
            self.view.set_variants()

        self.assertEqual(get_var.call_count, 0)
        self.assertEqual(self.view.variants, {})
