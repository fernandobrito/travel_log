import datetime
import operator
import os

import yaml

from travel_log.assets.pictures.picture import Picture
from travel_log.assets.tracks.track import Track
from travel_log.models.trip_day import TripDay


class TripDayParser:
    @staticmethod
    def parse_folder(folder_path) -> TripDay:
        folder_name = os.path.basename(folder_path)
        date = datetime.date.fromisoformat(folder_name)
        trip_day = TripDay(date)

        trip_day.pictures = sorted(Picture.from_folder_path(folder_path), key=operator.attrgetter('filename'))
        trip_day.tracks = sorted(Track.from_folder_path(folder_path), key=operator.attrgetter('filename'))

        try:
            with open(os.path.join(folder_path, 'day.yaml')) as file:
                trip_day.metadata = yaml.full_load(file)

            trip_day.summary = trip_day.metadata.get('summary')
        except FileNotFoundError:
            pass

        print(trip_day)

        return trip_day
