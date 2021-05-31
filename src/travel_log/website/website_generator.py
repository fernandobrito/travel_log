import os
import shutil

from jinja2 import FileSystemLoader, Environment

from travel_log.assets.pictures.picture_resizer import PictureResizer
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
        os.makedirs(os.path.join(trip_day_pictures_folder_path, 'original'))
        os.makedirs(os.path.join(trip_day_pictures_folder_path, 'thumbnail'))

        for picture in trip_day.pictures:
            shutil.copyfile(picture.path, os.path.join(trip_day_pictures_folder_path, 'original', picture.filename))

            thumbnail_output_folder = os.path.join(trip_day_pictures_folder_path, 'thumbnail')
            PictureResizer.generate_thumbnail(picture, thumbnail_output_folder,
                                              cache_folder=cache_path)


def copy_tracks(folder_path, trip: Trip):
    tracks_folder_path = os.path.join(folder_path, 'tracks')

    os.makedirs(tracks_folder_path)

    for trip_day in trip.trip_days:
        trip_day_tracks_folder_path = os.path.join(tracks_folder_path, trip_day.date_iso)
        os.makedirs(trip_day_tracks_folder_path)

        for picture in trip_day.tracks:
            shutil.copyfile(picture.path, os.path.join(trip_day_tracks_folder_path, picture.filename))


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
