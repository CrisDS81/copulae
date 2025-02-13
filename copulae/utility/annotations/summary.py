import wrapt

from copulae.copula import BaseCopula
from copulae.copula.exceptions import NotFittedError
from copulae.copula.summary import SummaryType

__all__ = ['select_summary']


@wrapt.decorator
def select_summary(method, instance: BaseCopula, args, kwargs) -> SummaryType:
    """
    Attempts to cast output to a DataFrame if applicable. Class instance must have '_columns' attribute
    """
    category = args[0] if len(args) > 0 else kwargs.get('category', 'copula')
    if category == 'copula':
        return method(*args, **kwargs)
    elif category == 'fit':
        fit_smry = getattr(instance, "_fit_smry", None)
        if fit_smry is None:
            raise NotFittedError
        return fit_smry
    else:
        raise ValueError("Summary category must be either 'copula' or 'fit'")
