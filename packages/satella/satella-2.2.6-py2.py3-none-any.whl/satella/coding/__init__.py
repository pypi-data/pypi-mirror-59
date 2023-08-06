"""
Just useful objects to make your coding nicer every day
"""

from .algos import merge_dicts
from .concurrent import Monitor, RMonitor
from .decorators import precondition, for_argument, PreconditionError
from .fun_static import static_var
from .recast_exceptions import rethrow_as, silence_excs

__all__ = [
    'Monitor', 'RMonitor', 'merge_dicts',
    'for_argument',
    'precondition', 'PreconditionError',
    'rethrow_as', 'silence_excs',
    'static_var'
]
