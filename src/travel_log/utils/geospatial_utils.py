def convert_degrees_to_decimal(dms: tuple[float, float, float], reference: str) -> float:
    """
    Convert coordinates from (degrees, minutes, seconds) to a decimal representation.
    EXIF stores coordinates in the former format.
    
    Adapted from https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3

    :param dms: tuple with (degrees, minutes, seconds)
    :param reference: str with N, S, W or E
    :return: decimal representation of the coordinates
    """
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 60.0 / 60.0

    if reference in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 6)
