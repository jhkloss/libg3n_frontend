import glob
import os
import time
import uuid

import yaml

from libg3n.model.libg3n_library import Libg3nLibrary
from logic.variation_point import VariationPoint
from config.module_config import MODULE_CONFIG


class Library:

    LIBRARY_CONFIG_FILE_NAME = 'libconf.yaml'

    name: str
    id: str
    version: str
    author: str
    institution: str

    path: str

    language: str = 'unknown'
    files: list = []
    number_of_files: int = 0

    libg3n_library: Libg3nLibrary

    def __init__(self, id: str, path: str):
        self.id = id
        self.path = path
        self.variation_points = []

        self.import_lib_config()

        for file in glob.iglob(self.path + '/**/*.*', recursive=True):
            self.files.append(file)
            self.number_of_files += 1

    def get_file_tree(self, path) -> (list, list):

        directories = []
        files = []

        for element in os.scandir(path):
            if element.is_dir():
                directories.append(element.name)
            else:
                date = time.ctime(os.path.getmtime(element.path))
                files.append({'name': element.name,'date': date})

        directories.sort()

        return directories, files

    def get_variation_point(self, id: str) -> any:
        for point in self.variation_points:
            if point.id == id:
                return point
        return None

    def get_library_uid(self):
        uid = uuid.uuid1()
        return str(uid)

    def get_library_tmp_directory(self, base_path: str = '', uid: str = '') -> str:

        # Handle custom uid
        if not uid:
            uid = self.get_library_uid()

        path = base_path + '/tmp/' + uid
        os.mkdir(path)

        if os.path.isdir(path):
            # Add tailing slash
            return path + '/'

        raise Exception('Could not create output directory!')

    def import_lib_config(self):

        path = self.path + '/' + self.LIBRARY_CONFIG_FILE_NAME

        if os.path.exists(path):
            with open(path) as file:
                config = yaml.safe_load(file)

                print(config)

                if 'name' in config:
                    self.name = config['name']

                if 'version' in config:
                    self.version = config['version']

                if 'author' in config:
                    self.author = config['author']

                if 'institution' in config:
                    self.institution = config['institution']

                if 'language' in config:
                    self.language = config['language']

                    if self.language in MODULE_CONFIG:
                        self.libg3n_library = MODULE_CONFIG[self.language](self.path)

                if 'variation-points' in config:

                    for element in config['variation-points']:

                        variation_point = VariationPoint(element['point'])

                        self.variation_points.append(variation_point)