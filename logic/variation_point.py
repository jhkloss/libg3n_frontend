from enum import Enum, auto


class VariationPoint:

    class TYPE(Enum):
        FUNCTION = auto()
        CLASS = auto()

    class FORM_TYPE(Enum):
        INPUT = auto()
        CHECKBOX = auto()
        SLIDER = auto()
        CODE = auto()

    id: str
    name: str
    description: str

    # Variation Point Type
    type: TYPE

    # Form Element Type
    form: FORM_TYPE

    # Properties dict for Class Variation points
    properties = {}

    def __init__(self, element: dict):
        if 'id' in element:
            self.id = element['id']
        if 'type' in element:
            self.type = self._parse_type(element['type'])
        if 'name' in element:
            self.name = element['name']
        if 'form' in element:
            self.form = element['form']
        if 'desc' in element:
            self.description = element['desc']
        if 'properties' in element:
            self.properties = element['properties']

    def _parse_type(self, type_str: str) -> TYPE:
        if type_str == 'function':
            return self.TYPE.FUNCTION
        elif type_str == 'class':
            return self.TYPE.CLASS

    def _parse_form_type(self, form_type_str: str) -> FORM_TYPE:
        pass