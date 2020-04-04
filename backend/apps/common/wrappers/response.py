import json

from typing import (
    Any,
    Callable,
    ClassVar,
)

from flask import Response

from typing_extensions import Final

JSON_MEDIA_TYPE: Final[str] = 'application/json'


class JSONResponse(Response):
    """Response with JSON decoded ``.data``.

    Attributes
    ----------
    json_decoder
        callable used to decode request's data to JSON payload

    """

    default_mimetype: ClassVar[str] = JSON_MEDIA_TYPE
    json_decoder: ClassVar[Callable] = staticmethod(json.dumps)  # noqa: WPS421

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_data(self.response)

    def set_data(self, value: Any) -> None:
        is_json_media_type = self.headers['Content-Type'] == JSON_MEDIA_TYPE
        already_decoded_types = (str, bytes, bytearray)
        if is_json_media_type and not isinstance(value, already_decoded_types):
            value = self.json_decoder(value)
        super().set_data(value)

    data = property(
        Response.get_data,
        set_data,
        doc='A descriptor that calls :meth:`get_data` and :meth:`set_data`.',
    )
