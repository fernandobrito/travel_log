import os

import click

from travel_log.parsers.trip_parser import TripParser
from travel_log.website.website_generator import generate_website

CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.option('--input-folder', help='The folder with your trip assets')
@click.option(
    '--output-folder',
    default='../../output/website/',
    help='The folder where the website will be generated',
)
def main(input_folder, output_folder):
    trip = TripParser.parse_folder(input_folder)

    output_path = os.path.join(CURRENT_FOLDER, output_folder)
    cache_path = os.path.join(CURRENT_FOLDER, '../../output/.cache')
    generate_website(trip, output_path, cache_path)


if __name__ == '__main__':
    main()
