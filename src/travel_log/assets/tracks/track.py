from dataclasses import dataclass

from travel_log.assets.abstract_asset import AbstractAsset

TRACKS_ALLOWED_EXTENSIONS = ['gpx']


@dataclass
class Track(AbstractAsset):
    """
    A GPS track. More methods will be added to retrieve stats (such as time moving, distance travelled, etc)
    """

    @classmethod
    def allowed_extensions(cls) -> list[str]:
        return TRACKS_ALLOWED_EXTENSIONS
