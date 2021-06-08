# Represents a day. Will hold all assets, metadata, etc
import datetime
from dataclasses import dataclass, field
from typing import Optional, Mapping

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

    @property
    def date_iso(self):
        return self.date.isoformat()

    def find_picture_by_filename(self, filename):
        return next(picture for picture in self.pictures if picture.filename == filename)
