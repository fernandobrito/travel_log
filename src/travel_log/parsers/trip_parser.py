import operator
import os

import yaml

from travel_log.models.highlight import Highlight
from travel_log.models.privacy_zone import PrivacyZone
from travel_log.models.trip import Trip
from travel_log.models.trip_day import TripDay
from travel_log.parsers.trip_day_parser import TripDayParser


class TripParser:
    @classmethod
    def parse_folder(cls, folder_path: str) -> Trip:
        trip_metadata = cls.parse_trip_metadata(folder_path)

        trip_days: list[TripDay] = []
        highlights: list[Highlight] = []
        privacy_zones: list[PrivacyZone] = []

        for sub_folder in os.listdir(folder_path):
            # we only want folders, not files
            if not os.path.isdir(os.path.join(folder_path, sub_folder)):
                print(f'Skipping not dir {sub_folder}')
                continue

            # also skip hidden folders
            if sub_folder.startswith('.'):
                print(f'Skipping hidden {sub_folder}')
                continue

            # make absolute path (sub_folder is only the name of the folder)
            sub_folder_full_path = os.path.join(folder_path, sub_folder)

            trip_day = TripDayParser.parse_folder(sub_folder_full_path)
            trip_days.append(trip_day)

            # check if there are highlights described
            if trip_day.metadata.get('highlights'):
                for highlight in trip_day.metadata['highlights']:
                    if highlight.get('picture'):
                        picture = trip_day.find_picture_by_filename(highlight['picture'].split('/')[-1])
                    else:
                        picture = None

                    highlights.append(
                        Highlight(from_date=trip_day.date, name=highlight['name'], summary=highlight['summary'],
                                  picture=picture))

        trip_days = sorted(trip_days, key=operator.attrgetter('date'))
        highlights = sorted(highlights, key=operator.attrgetter('from_date'))

        for privacy_zone in trip_metadata.get('privacy_zones', []):
            privacy_zones.append(PrivacyZone(**privacy_zone))

        trip = Trip(title=trip_metadata['title'], trip_days=trip_days, summary=trip_metadata['summary'],
                    highlights=highlights, privacy_zones=privacy_zones)

        return trip

    @staticmethod
    def parse_trip_metadata(folder_path):
        with open(os.path.join(folder_path, 'trip.yaml')) as file:
            return yaml.full_load(file)
