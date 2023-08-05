import inspect
import itertools

from hestia.exceptions import HestiaException
from hestia.imports import import_string

try:
    from django.utils.functional import LazyObject, empty  # pylint:disable=import-error
except ImportError:
    raise HestiaException('This module depends on django.')


class InvalidService(Exception):
    pass


class Service(object):
    __all__ = ()
    is_setup = False

    def validate(self):
        """Validate the settings for this backend (i.e. such as proper connection info).

        Raise ``InvalidService`` if there is a configuration error.
        """

    def setup(self):
        """Initialize this service."""
        self.is_setup = True


class LazyServiceWrapper(LazyObject):
    """Lazyily instantiates a Polyaxon standard service class.

    >>> LazyServiceWrapper(BaseClass, 'path.to.import.Backend', {})

    Provides an ``expose`` method for dumping public APIs to a context, such as module locals:

    >>> service = LazyServiceWrapper(...)
    >>> service.expose(locals())
    """

    def __init__(self, backend_base, backend_path, options):
        super(LazyServiceWrapper, self).__init__()
        self.__dict__.update(
            {
                '_backend_base': backend_base,
                '_backend_path': backend_path,
                '_options': options,
            }
        )

    def __getattr__(self, name):
        if self._wrapped is empty:  # pylint:disable=attribute-defined-outside-init
            self._setup()
        return getattr(self._wrapped, name)

    def _setup(self):
        backend = import_string(self._backend_path)
        assert issubclass(backend, Service)
        instance = backend(**self._options)
        self._wrapped = instance  # pylint:disable=attribute-defined-outside-init

    def expose(self, context):
        base = self._backend_base
        for key in itertools.chain(base.__all__, ('validate', 'setup')):
            if inspect.isfunction(getattr(base, key)):
                # pylint:disable=unnecessary-lambda
                # pylint:disable=undefined-variable
                context[key] = (lambda f: lambda *a, **k: getattr(self, f)(*a, **k))(key)
            else:
                context[key] = getattr(base, key)
