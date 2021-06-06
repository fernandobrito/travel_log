import datetime
from dataclasses import dataclass
from typing import Optional

from travel_log.assets.pictures.picture import Picture


@dataclass
class Highlight:
    """
    A highlight, created to mark events such as a special place visited. Can also model multiple day events,
    such as a 3 days hike in a longer trip.
    """
    name: str

    from_date: datetime.date

    summary: Optional[str] = None
    picture: Optional[Picture] = None
    to_date: Optional[datetime.date] = None

    def __post_init__(self):
        if not self.to_date:
            self.to_date = self.from_date
