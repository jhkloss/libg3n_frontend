from .library import Library
from .variation_point import VariationPoint

import json

class ConfigGenerator:

    FUNCTION_TEMPLATE = 'function {name}: {type}\n\t{value}\n'

    CLASS_TEMPLATE = 'class {name}:\n {properties}\n'

    PROPERTY_TEMPLATE = '\tproperty {name}: {type}\n'

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
                print(classes)
                for key, properties in classes.items():
                    variation_point = library.get_variation_point(key)

                    if variation_point:
                        result += self.parse_variation_point(variation_point, properties)

        return result

    def parse_variation_point(self, variation_point: VariationPoint, value: any) -> str:
        print(variation_point.type)
        print(variation_point.TYPE.FUNCTION)

        result = ''

        if variation_point.type == variation_point.TYPE.FUNCTION:
            result = self.FUNCTION_TEMPLATE.format(
                name=variation_point.id,
                type='return',
                value=value
            )
        elif variation_point.type == variation_point.TYPE.CLASS:
            properties = ''

            # Value is dict of properties
            for key, type in value.items():
                properties += self.PROPERTY_TEMPLATE.format(name=key, type=type)

            result = self.CLASS_TEMPLATE.format(name=variation_point.id, properties=properties)

        result += '\n'
        return result

    def get_config_file(self, content: str):
        pass