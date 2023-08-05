"""
    pint
    ~~~~

    Pint is Python module/package to define, operate and manipulate
    **physical quantities**: the product of a numerical value and a
    unit of measurement. It allows arithmetic operations between them
    and conversions from and to different units.

    :copyright: 2016 by Pint Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import sys

import pkg_resources

from .context import Context
from .errors import (
    DefinitionSyntaxError,
    DimensionalityError,
    OffsetUnitCalculusError,
    RedefinitionError,
    UndefinedUnitError,
    UnitStrippedWarning,
)
from .formatting import formatter
from .measurement import Measurement
from .quantity import Quantity
from .registry import LazyRegistry, UnitRegistry
from .unit import Unit
from .util import logger, pi_theorem

try:
    from pintpandas import PintArray, PintType

    del PintType
    del PintArray

    _HAS_PINTPANDAS = True
except ImportError:
    _HAS_PINTPANDAS = False
    _, _pintpandas_error, _ = sys.exc_info()

try:  # pragma: no cover
    __version__ = pkg_resources.get_distribution("pint").version
except Exception:  # pragma: no cover
    # we seem to have a local copy not installed without setuptools
    # so the reported version will be unknown
    __version__ = "unknown"


#: A Registry with the default units and constants.
_DEFAULT_REGISTRY = LazyRegistry()

#: Registry used for unpickling operations.
_APP_REGISTRY = _DEFAULT_REGISTRY


def _unpickle(cls, *args):
    """Rebuild object upon unpickling.
    All units must exist in the application registry.

    Parameters
    ----------
    cls : Quantity, Magnitude, or Unit
    *args

    Returns
    -------
    object of type cls

    """
    from .unit import UnitsContainer

    for arg in args:
        # Prefixed units are defined within the registry
        # on parsing (which does not happen here).
        # We need to make sure that this happens before using.
        if isinstance(arg, UnitsContainer):
            for name in arg:
                _APP_REGISTRY.parse_units(name)

    return cls(*args)


def set_application_registry(registry):
    """Set the application registry, which is used for unpickling operations
    and when invoking pint.Quantity or pint.Unit directly.

    Parameters
    ----------
    registry : pint.UnitRegistry
    """
    if not isinstance(registry, (LazyRegistry, UnitRegistry)):
        raise TypeError("Expected UnitRegistry; got %s" % type(registry))
    global _APP_REGISTRY
    logger.debug("Changing app registry from %r to %r.", _APP_REGISTRY, registry)
    _APP_REGISTRY = registry


def get_application_registry():
    """Return the application registry. If :func:`set_application_registry` was never
    invoked, return a registry built using :file:`defaults_en.txt` embedded in the pint
    package.

    Returns
    -------
    pint.UnitRegistry
    """
    return _APP_REGISTRY


def test():
    """Run all tests.

    Returns
    -------
    unittest.TestResult
    """
    from .testsuite import run

    return run()


# Enumerate all user-facing objects
# Hint to intersphinx that, when building objects.inv, these objects must be registered
# under the top-level module and not in their original submodules
__all__ = (
    "Context",
    "Measurement",
    "Quantity",
    "Unit",
    "UnitRegistry",
    "DefinitionSyntaxError",
    "DimensionalityError",
    "OffsetUnitCalculusError",
    "RedefinitionError",
    "UndefinedUnitError",
    "UnitStrippedWarning",
    "formatter",
    "get_application_registry",
    "set_application_registry",
    "pi_theorem",
    "__version__",
)
