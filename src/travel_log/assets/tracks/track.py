from dataclasses import dataclass, field

import gpxpy.gpx

from travel_log.assets.abstract_asset import AbstractAsset

TRACKS_ALLOWED_EXTENSIONS = ['gpx']


@dataclass
class Track(AbstractAsset):
    """
    A GPS track. More methods will be added to retrieve stats (such as time moving, distance travelled, etc)
    """

    """
    Used to check if the file was modified and needs to be saved.
    """
    is_dirty: bool = False

    _data: gpxpy.gpx.GPX = field(default=None, init=False, repr=False, compare=False)

    @classmethod
    def allowed_extensions(cls) -> list[str]:
        return TRACKS_ALLOWED_EXTENSIONS

    @property
    def data(self):
        """
        Returns a gpxpy object with the parsed track data.
        """

        with open(self.path, 'r') as file:
            return gpxpy.parse(file)

    @data.setter
    def data(self, value):
        self.is_dirty = True
        self._data = value

    def persist_data(self) -> bool:
        """
        Saves the underlying data property (if it was defined using the setter) back
        in the file. If the data property has never been updated (aka this object is
        not dirty), nothing happens.

        If this is a read only object, an exception is raised.

        :return: True if the file was saved or False if it was not (not dirty)
        """
        if self.is_read_only:
            raise RuntimeError('Abort! Trying to modify a read_only asset.')

        if self.is_dirty:
            print(f'Overwriting Track {self.path}')

            self._data.nsmap['gpx_style'] = 'http://www.topografix.com/GPX/gpx_style/0/2'

            with open(self.path, 'w') as file:
                file.write(self._data.to_xml())

            return True

        return False
