import shutil
from tempfile import NamedTemporaryFile

from pytest import fixture
from travel_log.models.privacy_zone import PrivacyZone

from test.conftest import path_on_sample_project

'''
When working with files in this test suite, we need a way to prevent the test of actually
modifying our original assets.

Either we: 1) Mock the destructive methods, like: > with patch.object(Picture,
'remove_exif_coordinates', return_value=None, autospec=True) as mock_method:

2) Create a temporary copy for each test and work on that.

Below, we follow the 2nd approach.
'''


@fixture
def privacy_zone_ristafallet():
    details = {'name': 'Ristafallet waterfall', 'lat': 63.3123834, 'lng': 13.3511221, 'radius': 3}
    return PrivacyZone(**details)


class TestPrivacyFilterOnImage:
    @fixture
    def image_path_close_to_ristafallet(self):
        original_path = path_on_sample_project('2021-05-07/day5-p1.jpeg')

        with NamedTemporaryFile() as temp_file:
            shutil.copy(original_path, temp_file.name)
            yield temp_file.name

    @fixture
    def image_path_far_from_ristafallet_waterfall(self):
        original_path = path_on_sample_project('2021-05-07/day5-p3.jpeg')

        with NamedTemporaryFile() as temp_file:
            shutil.copy(original_path, temp_file.name)
            yield temp_file.name

    def test_privacy_filter_is_applied_if_close(
        self, image_path_close_to_ristafallet, privacy_zone_ristafallet
    ):
        applied = PrivacyZone.apply_many_on_processed_picture(
            [privacy_zone_ristafallet], image_path_close_to_ristafallet
        )

        assert applied

    def test_privacy_filter_is_not_applied_if_far(
        self, image_path_far_from_ristafallet_waterfall, privacy_zone_ristafallet
    ):
        applied = PrivacyZone.apply_many_on_processed_picture(
            [privacy_zone_ristafallet], image_path_far_from_ristafallet_waterfall
        )

        assert not applied


class TestPrivacyFilterOnTrack:
    @fixture
    def track_path_close_to_ristafallet(self):
        original_path = path_on_sample_project('2021-05-07/car.gpx')

        with NamedTemporaryFile() as temp_file:
            shutil.copy(original_path, temp_file.name)
            yield temp_file.name

    @fixture
    def track_path_far_from_ristafallet(self):
        original_path = path_on_sample_project('2021-05-03/car.gpx')

        with NamedTemporaryFile() as temp_file:
            shutil.copy(original_path, temp_file.name)
            yield temp_file.name

    def test_privacy_filter_is_applied_if_close(
        self, track_path_close_to_ristafallet, privacy_zone_ristafallet
    ):
        applied = PrivacyZone.apply_many_on_processed_track(
            [privacy_zone_ristafallet], track_path_close_to_ristafallet
        )

        assert applied

    def test_privacy_filter_is_not_applied_if_far(
        self, track_path_far_from_ristafallet, privacy_zone_ristafallet
    ):
        applied = PrivacyZone.apply_many_on_processed_track(
            [privacy_zone_ristafallet], track_path_far_from_ristafallet
        )

        assert not applied
