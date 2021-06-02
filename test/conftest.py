import os

CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))


def path_on_sample_project(path):
    return os.path.join(CURRENT_FOLDER, '_sample_project', path)
