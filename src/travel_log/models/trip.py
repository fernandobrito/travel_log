import datetime
from dataclasses import dataclass, field
from typing import Optional

from travel_log.models.highlight import Highlight
from travel_log.models.trip_day import TripDay


@dataclass
class Trip:
    """
    A trip is the main entity represented on each execution of this entire project. It serves as a parent object
    to all assets (mostly through TripDay) and other models.
    """
    title: str
    trip_days: list[TripDay]
    highlights: list[Highlight] = field(default_factory=list)

    summary: Optional[str] = None

    def highlights_on_date(self, date: datetime.date) -> list[Highlight]:
        # TODO: add support to a highlight with a date range

        return list(highlight for highlight in self.highlights if highlight.from_date == date)
