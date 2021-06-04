import os
import shutil
from hashlib import md5
from pathlib import Path

from PIL import Image

from travel_log.assets.pictures.picture import Picture

THUMBNAIL_SIZE = (150, 150)
FULL_SIZE = (1600, 1600)


class PictureResizer:
    @classmethod
    def generate_full_size(cls, picture: Picture, output_path: str, *, cache_folder: str = None) -> None:
        """
        Generates a thumbnail and saves it with the same original filename on the
        given output_folder.

        For the caching behavior, see the `generate_thumbnail` docs.

        """
        cls._generate_with_cache(picture, output_path, FULL_SIZE, cache_folder=cache_folder,
                                 cache_prefix='full')

    @classmethod
    def generate_thumbnail(cls, picture: Picture, output_path: str, *, cache_folder: str = None) -> None:
        """
        Generates a thumbnail and saves it with the same original filename on the
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

        cls._generate_with_cache(picture, output_path, THUMBNAIL_SIZE, cache_folder=cache_folder,
                                 cache_prefix='thumbnail')

    @classmethod
    def _generate_with_cache(cls, picture: Picture, output_path: str, size, *,
                             cache_folder: str = None, cache_prefix: str = None) -> None:
        if cache_folder:
            original_full_path = os.path.join(picture.path, picture.filename)
            hashed_path = md5(original_full_path.encode())

            cached_full_path = os.path.join(cache_folder, hashed_path.hexdigest(), cache_prefix or '', picture.filename)

            try:
                shutil.copyfile(cached_full_path, output_path)
                print(f'[Picture] Cache for {picture.filename} used')
                return
            except FileNotFoundError:
                try:
                    os.makedirs(Path(cached_full_path).parent)
                except FileExistsError:
                    pass

                cls._generate_resized(picture, cached_full_path, size)
                print(f'[Picture] Cache for {picture.filename} generated')

                shutil.copyfile(cached_full_path, output_path)
                return

        cls._generate_resized(picture, size, output_path)

    @staticmethod
    def _generate_resized(picture: Picture, full_output_path: str, size: tuple[int, int]) -> None:
        """
        Internal method used to actually generate and save the resized image.
        Extracted to an internal method to allow for reuse within the cache logic.

        :param full_output_path: path with filename
        :return: None
        """

        # If you are not explicit with EXIF, pillow will not preserve it
        # https://stackoverflow.com/a/17047039/3950305
        image = Image.open(picture.path)
        image.thumbnail(size)
        exif = image.info['exif']
        image.save(full_output_path, optimize=True, exif=exif)
