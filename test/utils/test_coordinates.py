from travel_log.utils.coordinates_utils import convert_degrees_to_decimal


def test_coordinates_conversion():
    # From MacOS Finder EXIF browser:
    # longitude: 18° 16' 16,002" E
    # latitude 62° 56' 7,002" N

    # Converting with: https://www.fcc.gov/media/radio/dms-decimal
    # longitude: 18.271112
    # latitude: 62.935278

    # From EXIF Python library:
    # 'gps_longitude': (18.0, 16.0, 16.0)
    # 'gps_longitude_ref': 'E'
    # 'gps_latitude': (62.0, 56.0, 7.0)
    # 'gps_latitude_ref': 'N'

    # Converting with: https://www.fcc.gov/media/radio/dms-decimal
    # longitude: 18.271111 (0.000001 diff)
    # latitude: 62.935278

    longitude = (18.0, 16.0, 16.0)
    longitude_ref = 'E'

    latitude = (62.0, 56.0, 7.0)
    latitude_ref = 'N'

    assert convert_degrees_to_decimal(longitude, longitude_ref) == 18.271111
    assert convert_degrees_to_decimal(latitude, latitude_ref) == 62.935278
