from copy import copy
from dataclasses import dataclass
from typing import Iterable

import geopy.distance

from travel_log.assets.pictures.picture import Picture
from travel_log.assets.tracks.track import Track
from travel_log.models.coordinates import Coordinates


@dataclass
class PrivacyZone:
    """
    A privacy zone is a circular zone (coordinates + radius) with a name.

    It is used to process pictures EXIF geolocation and tracks with the intent of not
    disclosing the exact location of a place (eg: your home's location).
    """
    name: str
    lat: float
    lng: float
    radius: int

    @property
    def coordinates(self) -> Coordinates:
        return Coordinates(latitude=self.lat, longitude=self.lng)

    def _is_point_inside(self, point: Coordinates) -> bool:
        distance = geopy.distance.geodesic(
            [point.latitude, point.longitude],
            [self.coordinates.latitude, self.coordinates.longitude]
        ).kilometers

        return distance <= self.radius

    def is_picture_inside(self, picture: Picture) -> bool:
        if not picture.coordinates:
            return False

        return self._is_point_inside(picture.coordinates)

    @staticmethod
    def apply_many_on_processed_picture(privacy_zones: Iterable['PrivacyZone'], path: str) -> bool:
        '''
        Takes many privacy zones and a path to a picture and check if the picture has
        EXIF geolocation and if it lies inside any privacy zone. If it does, the
        EXIF geolocation is removed and the method returns True.

        :param privacy_zones: a list of privacy zones
        :param path: the path to a picture
        :return: whether the picture lies inside a privacy zone
        '''
        picture = Picture(path)
        picture.is_read_only = False

        for privacy_zone in privacy_zones:
            if privacy_zone.is_picture_inside(picture):
                print(f'Picture inside {privacy_zone.name}')
                picture.remove_exif_coordinates()
                return True

        return False

    def process_track(self, input_track: Track) -> Track:
        """
        Checks if any segment of the track starts or ends inside a privacy zone.
        If it does, the track is cropped where necessary.

        :param input_track:
        :return: the track (either original or modified)
        """

        track_data = input_track.data

        points_removed = 0

        for track in track_data.tracks:
            for segment in track.segments:
                for point in copy(segment.points):
                    point_coordinates = Coordinates(latitude=point.latitude, longitude=point.longitude)

                    if self._is_point_inside(point_coordinates):
                        segment.points.remove(point)
                        points_removed += 1

        if points_removed > 0:
            print(
                f'Track {input_track.filename} had points {points_removed} removed from inside "{self.name}" privacy zone')

            input_track.data = track_data

        return input_track

    @staticmethod
    def apply_many_on_processed_track(privacy_zones: Iterable['PrivacyZone'], path: str) -> bool:
        track = Track(path)
        track.is_read_only = False

        for privacy_zone in privacy_zones:
            track = privacy_zone.process_track(track)

        return track.persist_data()
