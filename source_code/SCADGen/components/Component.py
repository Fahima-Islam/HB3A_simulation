class Component:

    def __init__(self):
        return

    def isComp(self):
        return True

    def _convertToLength(self, s):
        "convert a string to a number without unit. the length unit is defined in __init__.py"
        from . import unit_parser, remove_length_unit
        if s[-1].isalpha():
            return remove_length_unit(unit_parser.parse(s))
        else:
            return float(s)
