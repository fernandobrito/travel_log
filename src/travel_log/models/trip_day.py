# Represents a day. Will hold all assets, metadata, etc
import datetime
import operator
import os.path
from dataclasses import dataclass, field
from typing import Optional, Mapping

import yaml

from travel_log.assets.pictures.picture import Picture
from travel_log.assets.tracks.track import Track


@dataclass
class TripDay:
    """
    A day in a trip. Can have assets, modeled metadata (such as summary) and flexible metadata defined
    by the user.
    """
    date: datetime.date
    pictures: list[Picture] = field(default_factory=list)
    tracks: list[Track] = field(default_factory=list)
    metadata: Mapping = field(default_factory=dict)

    summary: Optional[str] = None

    @classmethod
    def from_folder_path(cls, folder_path) -> 'TripDay':
        folder_name = os.path.basename(folder_path)
        date = datetime.date.fromisoformat(folder_name)
        trip_day = cls(date)

        trip_day.pictures = sorted(Picture.from_folder_path(folder_path), key=operator.attrgetter('filename'))
        trip_day.tracks = sorted(Track.from_folder_path(folder_path), key=operator.attrgetter('filename'))

        try:
            with open(os.path.join(folder_path, 'day.yaml')) as file:
                trip_day.metadata = yaml.full_load(file)

            trip_day.summary = trip_day.metadata['summary']
        except FileNotFoundError:
            pass

        print(trip_day)

        return trip_day

    @property
    def date_iso(self):
        return self.date.isoformat()
