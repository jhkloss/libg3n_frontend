import os.path
import shutil

from .library import Library
from .variation_point import VariationPoint
from config.module_config import CONFIG_CLASSES

from libg3n import Generator, GeneratorConfigKeys

import json

class ConfigGenerator:

    FUNCTION_TEMPLATE = 'function {name}: {type}\n\t"{value}"\n'

    CLASS_TEMPLATE = 'class {name}\n {properties}\n'

    PROPERTY_TEMPLATE = '\tproperty {name}: {type}\n'

    root_path = "/"

    def __init__(self, root_path: str):
        self.root_path = root_path

    def parse(self, library: Library,  config_values: dict) -> str:

        result = ''

        # Parse Functions
        for key, value in config_values.items():

            variation_point = library.get_variation_point(key)

            if variation_point:
                result += self.parse_variation_point(variation_point, value)

        if 'classes' in config_values:
            classes = json.loads(config_values['classes'])

            if classes:
                for key, properties in classes.items():
                    variation_point = library.get_variation_point(key)

                    if variation_point:
                        result += self.parse_variation_point(variation_point, properties)

        return result

    def parse_variation_point(self, variation_point: VariationPoint, value: any) -> str:

        result = ''

        if variation_point.type == variation_point.TYPE.FUNCTION:
            result = self.FUNCTION_TEMPLATE.format(
                name=variation_point.id,
                type='return',
                value=value
            )
            result += '\n'

        elif variation_point.type == variation_point.TYPE.CLASS:
            properties = ''

            # Value is dict of properties
            for key, type in value.items():
                properties += self.PROPERTY_TEMPLATE.format(name=key, type=type)

            result = self.CLASS_TEMPLATE.format(name=variation_point.id, properties=properties)

        return result

    def get_config_file(self, library: Library, config_values: dict, uid: str = '', create_folder: bool = False) -> (str, str):

        # Handle custom uid
        if not uid:
            uid = library.get_library_uid()

        content = self.parse(library, config_values)
        file_name = uid + '.gen'
        folder_path = ''

        # Handle custom folder
        if create_folder:
            folder_path = library.get_library_tmp_directory(base_path=self.root_path, uid=uid)
            path = folder_path + file_name
        else:
            path = self.root_path + '/tmp/' + file_name
        
        with open(path, mode='w+') as f:
            f.write(content)

        if os.path.exists(path):
            return path, folder_path

    def generate_library(self, library: Library, config_values: dict) -> (str, str):

        # Generate uid for the generation process
        uid = library.get_library_uid()

        config_path, folder_path = self.get_config_file(library, config_values, uid=uid, create_folder=True)

        if config_path and folder_path:

            if library.language in CONFIG_CLASSES:
                config = CONFIG_CLASSES[library.language](config_path)

                if config:

                    # Create Generation Config
                    # TODO: Remove Function skip
                    generation_config = {
                        GeneratorConfigKeys.OUTPUT_DIR: folder_path,
                        GeneratorConfigKeys.CLASS_SUBFOLDER: 'classes',
                        GeneratorConfigKeys.CLASS_PREFIX: 'class_',
                        GeneratorConfigKeys.COPY_LIBRARY_FILES: True,
                        #GeneratorConfigKeys.SKIP_FUNCTIONS: True
                    }

                    # Get generator instance
                    generator = Generator()

                    # Load generator config
                    generator.load_config(generation_config)

                    # Generate the library files
                    generator.generate(library.libg3n_library, config)

                    # Get the Archive path
                    archive_path = folder_path + uid

                    # Create the archive
                    archive = shutil.make_archive(base_name=archive_path, format="zip", root_dir=folder_path)

                    return 'generated.zip', archive
