import os
import shutil
from hashlib import md5
from pathlib import Path

from PIL import Image

from travel_log.assets.pictures.picture import Picture

THUMBNAIL_SIZE = (150, 150)


class PictureResizer:
    @classmethod
    def generate_thumbnail(cls, picture: Picture, output_path: str, *, cache_folder: str = None) -> None:
        """
        Generates a thumbnail and save it with the same original filename on the
        given output_folder.

        If a cache folder is provided, it first looks for a cached thumbnail there before
        generating one. If the cache exists, the cached version is copied to the output_folder.

        To preserve the original filename in the cache but still avoid naming conflicts with
        the same filename from different trip days, we add the cached thumbnail on a subfolder.
        The original path (with filename) is hashed to create the subfolder name and the cached
        thumbnail is stored there with the original file name.

        :param picture: the picture to be resized
        :param output_path: str with a path (including file name) where the picture should be saved
        :param cache_folder: optional path to a cache folder
        :return: none
        """

        if cache_folder:
            original_full_path = os.path.join(picture.path, picture.filename)
            hashed_path = md5(original_full_path.encode())

            cached_full_path = os.path.join(cache_folder, hashed_path.hexdigest(), picture.filename)

            try:
                shutil.copyfile(cached_full_path, output_path)
                print(f'[Picture] Cache for {picture.filename} used')
                return
            except FileNotFoundError:
                os.makedirs(Path(cached_full_path).parent)

                cls._generate_thumbnail(picture, cached_full_path)
                print(f'[Picture] Cache for {picture.filename} generated')

                shutil.copyfile(cached_full_path, output_path)

        cls._generate_thumbnail(picture, output_path)

    @staticmethod
    def _generate_thumbnail(picture: Picture, full_output_path: str) -> None:
        """
        Internal method used to actually generate and save the thumbnail.
        Extracted to an internal method to allow for reuse within the cache logic.

        :param full_output_path: path with filename
        :return: None
        """
        image = Image.open(picture.path)
        image.thumbnail(THUMBNAIL_SIZE)
        image.save(full_output_path)
