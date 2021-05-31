from dataclasses import dataclass
from functools import cached_property
from typing import Optional

import exif

from travel_log.assets.abstract_asset import AbstractAsset
from travel_log.models.coordinates import Coordinates
from travel_log.utils.coordinates_utils import convert_degrees_to_decimal

PICTURES_ALLOWED_EXTENSIONS = ['jpg', 'jpeg']


@dataclass
class Picture(AbstractAsset):
    """
    A picture. Can have coordinates on the EXIF metadata.
    """

    @classmethod
    def allowed_extensions(cls) -> list[str]:
        return PICTURES_ALLOWED_EXTENSIONS

    @cached_property
    def exif(self) -> dict:
        # The library returns an object, but we want a dict
        with open(self.path, 'rb') as file:
            image = exif.Image(file)

        return {attribute: image.get(attribute) for attribute in image.list_all()}

    @cached_property
    def coordinates(self) -> Optional[Coordinates]:
        """
        :return: a pair of Coordinates (longitude, latitude) where the picture was taken, if available. Else, None.
        """
        try:
            longitude = convert_degrees_to_decimal(self.exif['gps_longitude'], self.exif['gps_latitude_ref'])
            latitude = convert_degrees_to_decimal(self.exif['gps_latitude'], self.exif['gps_longitude_ref'])

            return Coordinates(longitude, latitude)
        except KeyError:
            return None
