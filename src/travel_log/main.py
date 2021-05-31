import operator
import os

import yaml

from travel_log.models.highlight import Highlight
from travel_log.models.trip import Trip
from travel_log.models.trip_day import TripDay
from travel_log.website.website_generator import generate_website

CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))


def parse_folder(folder_path: str) -> Trip:
    trip_metadata = parse_trip_metadata(folder_path)
    trip_days: list[TripDay] = []
    highlights: list[Highlight] = []

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

        trip_day = TripDay.from_folder_path(sub_folder_full_path)
        trip_days.append(trip_day)

        # check if there are highlights described
        if trip_day.metadata.get('highlights'):
            for highlight in trip_day.metadata['highlights']:
                highlights.append(
                    Highlight(from_date=trip_day.date, name=highlight['name'], summary=highlight['summary']))

    trip_days = sorted(trip_days, key=operator.attrgetter('date'))
    highlights = sorted(highlights, key=operator.attrgetter('from_date'))

    trip = Trip(title=trip_metadata['title'], trip_days=trip_days, summary=trip_metadata['summary'],
                highlights=highlights)

    return trip


def parse_trip_metadata(folder_path):
    with open(os.path.join(folder_path, 'trip.yaml')) as file:
        return yaml.full_load(file)


trip = parse_folder('/Users/brito/personal/travel_log/test/sample_project')

output_path = os.path.join(CURRENT_FOLDER, '../../output/website')
cache_path = os.path.join(CURRENT_FOLDER, '../../output/.cache')
generate_website(trip, output_path, cache_path)
