from typing import NamedTuple

from flask import current_app

import googlemaps

from typing_extensions import Final

WARSAW_CITY_CENTER_COORDINATES: Final = (52.237049, 21.017532)


class GeoCodingResult(NamedTuple):
    address: str
    latitude: float
    longitude: float


def geolocation_from(address: str) -> GeoCodingResult:
    google_maps_client = googlemaps.Client(
        key=current_app.config['GOOGLE_MAPS_API_KEY'],
    )
    geo_results = google_maps_client.geocode(address, language='pl')
    geo_result = next(iter(geo_results), {})
    if not geo_result:
        # NOTE: returns Warsaw center as safe backup
        return GeoCodingResult(address, *WARSAW_CITY_CENTER_COORDINATES)
    location = geo_result['geometry']['location']
    return GeoCodingResult(
        geo_result['formatted_address'],
        location['lat'],
        location['lng'],
    )
