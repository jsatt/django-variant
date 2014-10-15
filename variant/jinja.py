import jinja2

from .utils import get_experiment_variant


@jinja2.contextfunction
def experiment_variant(context, experiment):
    try:
        request = context['request']
    except KeyError:
        return jinja2.Undefined('request must be defined in Context')
    return get_experiment_variant(request, experiment, make_decision=False)
