from dataclasses import dataclass
from functools import cached_property
from typing import Optional

import exif
from travel_log.assets.abstract_asset import AbstractAsset
from travel_log.models.coordinates import Coordinates
from travel_log.utils.geospatial_utils import convert_degrees_to_decimal

PICTURES_ALLOWED_EXTENSIONS = ['jpg', 'jpeg']


@dataclass
class Picture(AbstractAsset):
    """
    A picture. Can have coordinates on the EXIF metadata.
    """

    is_exif_coordinates_ignored: bool = False

    @classmethod
    def allowed_extensions(cls) -> list[str]:
        return PICTURES_ALLOWED_EXTENSIONS

    @cached_property
    def exif(self) -> dict:
        # The library returns an object, but we want a dict
        with open(self.path, 'rb') as file:
            image = exif.Image(file)

        return {attribute: image.get(attribute) for attribute in image.list_all()}

    @property
    def coordinates(self) -> Optional[Coordinates]:
        """
        :return: a pair of Coordinates (longitude, latitude) where the picture was taken, if
        available. Else, None.
        """

        if self.is_exif_coordinates_ignored:
            return None

        return self._exif_coordinates

    @cached_property
    def _exif_coordinates(self) -> Optional[Coordinates]:
        try:
            longitude = convert_degrees_to_decimal(
                self.exif['gps_longitude'], self.exif['gps_latitude_ref']
            )
            latitude = convert_degrees_to_decimal(
                self.exif['gps_latitude'], self.exif['gps_longitude_ref']
            )

            return Coordinates(longitude, latitude)
        except KeyError:
            return None

    def remove_exif_coordinates(self) -> None:
        """
        Actually removes the EXIF coordinates from the underlying file.
        Useful to use on thumbnails and processed pictures.

        If this is a read only object, an exception is raised.
        """
        if self.is_read_only:
            raise RuntimeError('Abort! Trying to remove exif coordinates from a read_only asset.')

        print(f'Removing EXIF coordinates for Picture {self.path}')

        with open(self.path, 'rb') as file:
            image = exif.Image(file)

        del image.gps_latitude
        del image.gps_longitude

        with open(self.path, 'wb') as file:
            file.write(image.get_file())

    def ignore_exif_coordinates(self) -> None:
        """
        Does not remove the EXIF coordinates from the underlying file, but
        instead only hide it in this object. Useful to use on original pictures.
        """
        self.is_exif_coordinates_ignored = True
