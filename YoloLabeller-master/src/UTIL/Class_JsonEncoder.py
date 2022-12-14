'''
Created on 26 abr. 2021

@author: Fran y Edu
@comment: Clase que gestiona la codificacion de la Json de salida
'''


import json


class CompactJSONEncoder(json.JSONEncoder):
    
    
    """A JSON Encoder that puts small containers on single lines."""
    CONTAINER_TYPES = (list, tuple, dict)
    """Container datatypes include primitives or other containers."""
    MAX_WIDTH = 1999
    """Maximum width of a container that might be put on a single line."""
    MAX_ITEMS = 99
    """Maximum number of items in container that might be put on single line."""
    INDENTATION_CHAR = " "
    """Number of spaces for each level """
    INDENTATION = 4


    def __init__(self, *args, **kwargs):
        self.indentation_level = 0


    def encode(self, o):
        
        """Encode JSON object *o* with respect to single line lists."""
        if isinstance(o, (list, tuple)):
            return "[" + ", ".join(self.encode(el) for el in o) + "]"
            #return "[" + (",\n" + self.indent_str).join(self.encode(el) for el in o) + "]"
        elif isinstance(o, dict):
            if o:
                self.indentation_level += 1
                output = [self.indent_str + json.dumps(k)+":"+ self.encode(v) for k, v in o.items()]
                self.indentation_level -= 1
                return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"
            else:
                return "{}"
        elif isinstance(o, float):  # Use scientific notation for floats, where appropiate
            return format(o, '.8f')
        elif isinstance(o, str):
            o = o.replace("\n", "\\n")
            o = '"' + o + '"'
            return o
        else:
            return json.dumps(o)


    def _put_on_single_line(self, o):
        return self._primitives_only(o) and len(o) <= self.MAX_ITEMS and len(str(o)) - 2 <= self.MAX_WIDTH


    def _primitives_only(self, o):
        if isinstance(o, (list, tuple)):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o)
        elif isinstance(o, dict):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o.values())


    @property
    def indent_str(self):
        return self.INDENTATION_CHAR*(self.indentation_level * self.INDENTATION)

    
