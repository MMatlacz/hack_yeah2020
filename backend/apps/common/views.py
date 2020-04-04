from typing import (
    Callable,
    ClassVar,
    Iterable,
    Mapping,
    Optional,
    Union,
)

from flask import (
    Response,
    request,
)
from flask.views import MethodView

IterableOfDecorators = Iterable[Callable]
MethodDecorators = Union[
    Mapping[str, IterableOfDecorators],
    IterableOfDecorators,
]


class APIView(MethodView):
    """Custom ``flask.views.MethodView`` subclass.

    Following class is improved copy of `flask_restful.Resource`.

    Attributes
    ----------
    method_decorators
        decorators that will be applied on methods.
        When set to mapping, keys are HTTP methods' names and values are
        iterables of decorators that will be applied to proper method.
        If ``method_decorators`` are set to list then decorators
        will be applied to *every* HTTP methods' method.

    """

    method_decorators: ClassVar[Optional[MethodDecorators]] = None

    def dispatch_request(self, *args, **kwargs) -> Response:
        # Taken from flask and flask-restful
        # noinspection PyUnresolvedReferences
        method = getattr(self, request.method.lower(), None)
        # If the request method is HEAD and we don't have a handler for it
        # retry with GET.
        if method is None and request.method == 'HEAD':
            method = getattr(self, 'get', None)

        message = f'Unimplemented method {request.method}'
        assert method is not None, message  # noqa: S101

        decorators = self.method_decorators or []
        if isinstance(decorators, Mapping):
            decorators = decorators.get(request.method.lower(), [])

        for decorator in decorators:
            method = decorator(method)

        return method(*args, **kwargs)
