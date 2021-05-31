# Represents a day. Will hold all assets, metadata, etc
import datetime
import os.path
from dataclasses import dataclass, field
from typing import Optional, Any

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

    summary: Optional[str] = None
    metadata: Optional[Any] = None

    @classmethod
    def from_folder_path(cls, folder_path) -> 'TripDay':
        folder_name = os.path.basename(folder_path)
        date = datetime.date.fromisoformat(folder_name)
        trip_day = cls(date)

        trip_day.pictures = Picture.from_folder_path(folder_path)
        trip_day.tracks = Track.from_folder_path(folder_path)

        with open(os.path.join(folder_path, 'day.yaml')) as file:
            trip_day.metadata = yaml.full_load(file)

        trip_day.summary = trip_day.metadata['summary']

        print(trip_day)

        return trip_day

    @property
    def date_iso(self):
        return self.date.isoformat()
