import os
import shutil

from jinja2 import FileSystemLoader, Environment

from travel_log.assets.pictures.picture_resizer import PictureResizer
from travel_log.models.privacy_zone import PrivacyZone
from travel_log.models.trip import Trip

CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))


def render_pages_to_files(folder_path, trip: Trip):
    template_file_name = 'index.html'

    file_loader = FileSystemLoader(os.path.join(CURRENT_FOLDER, 'templates'))
    env = Environment(loader=file_loader)

    template = env.get_template(template_file_name)
    rendered = template.render(trip=trip)

    with open(os.path.join(folder_path, template_file_name), 'w') as file:
        file.write(rendered)


def copy_static_files(folder_path):
    shutil.copytree(os.path.join(CURRENT_FOLDER, 'static', 'css'), os.path.join(folder_path, 'css'))
    shutil.copytree(os.path.join(CURRENT_FOLDER, 'static', 'js'), os.path.join(folder_path, 'js'))
    shutil.copytree(os.path.join(CURRENT_FOLDER, 'static', 'images'), os.path.join(folder_path, 'images'))


def copy_pictures(folder_path, cache_path, trip: Trip):
    pictures_folder_path = os.path.join(folder_path, 'pictures')

    os.makedirs(pictures_folder_path)

    for trip_day in trip.trip_days:
        trip_day_pictures_folder_path = os.path.join(pictures_folder_path, trip_day.date_iso)
        os.makedirs(trip_day_pictures_folder_path)
        os.makedirs(os.path.join(trip_day_pictures_folder_path, 'full'))
        os.makedirs(os.path.join(trip_day_pictures_folder_path, 'thumbnail'))

        for picture in trip_day.pictures:
            full_output_path = os.path.join(trip_day_pictures_folder_path, 'full', picture.filename)
            PictureResizer.generate_full_size(picture, full_output_path,
                                              cache_folder=cache_path)
            inside_zone = PrivacyZone.apply_many_on_processed_picture(trip.privacy_zones, full_output_path)
            if inside_zone:
                picture.ignore_exif_coordinates()

            thumbnail_output_path = os.path.join(trip_day_pictures_folder_path, 'thumbnail', picture.filename)
            PictureResizer.generate_thumbnail(picture, thumbnail_output_path,
                                              cache_folder=cache_path)
            inside_zone = PrivacyZone.apply_many_on_processed_picture(trip.privacy_zones, thumbnail_output_path)
            if inside_zone:
                picture.ignore_exif_coordinates()

            '''
            The behavior above with pictures is a bit tricky to follow.
            
            We need to do 2 things:
            1) Remove the EXIF coordinates from the processed files (thumbnail and full)
            that are moved to the output folder. This is done with the 
            PrivacyZone.apply_many_on_processed_picture) method.
            
            2) The Trip object (or to be more precise, TripDays), has reference to Picture
            objects that are actually referencing the original pictures (not copied to the output
            folder). Those Picture objects are the ones used in the templates, and from those we
            need to "hide" the EXIF coordinates from the object, but we don't want to modify
            the original files. This is done with the picture.ignore_exif_coordinates().
            '''


def copy_tracks(folder_path, trip: Trip):
    tracks_folder_path = os.path.join(folder_path, 'tracks')

    os.makedirs(tracks_folder_path)

    for trip_day in trip.trip_days:
        trip_day_tracks_folder_path = os.path.join(tracks_folder_path, trip_day.date_iso)
        os.makedirs(trip_day_tracks_folder_path)

        for picture in trip_day.tracks:
            track_output_path = os.path.join(trip_day_tracks_folder_path, picture.filename)
            shutil.copyfile(picture.path, track_output_path)

            PrivacyZone.apply_many_on_processed_track(trip.privacy_zones, track_output_path)


def generate_website(trip: Trip, folder_path, cache_path):
    """
    The entry point to generate the website.
    It will copy static files related to the website per se, copy the user assets and
    use the website templates to render the final output.

    :param folder_path: a folder path where the website will be generated
    :param cache_path: a folder path that can be used as a storage cache for some operations
    :param trip: the trip
    :return:
    """
    # remove existing folder
    shutil.rmtree(folder_path, ignore_errors=True)

    # create a new empty folder
    os.makedirs(folder_path)

    # create or copy files
    copy_static_files(folder_path)
    copy_pictures(folder_path, cache_path, trip)
    copy_tracks(folder_path, trip)
    render_pages_to_files(folder_path, trip)
