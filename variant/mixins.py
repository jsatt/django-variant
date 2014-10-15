from collections import defaultdict
from .utils import get_experiment_variant


class VariantTestMixin(object):
    experiments = []

    def __init__(self, *args, **kwargs):
        super(VariantTestMixin, self).__init__(*args, **kwargs)
        self.variants = defaultdict(lambda: None)

    def dispatch(self, request, *args, **kwargs):
        self.set_variants()
        return super(VariantTestMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['variants'] = self.variants
        return super(VariantTestMixin, self).get_context_data(**kwargs)

    def set_variants(self):
        for exp in self.experiments:
            variant = get_experiment_variant(self.request, exp)
            if variant:
                self.variants[exp] = variant
