class Transformation:

    def __init__(self):
        self.body = None;
        return

    def isComp(self):
        return False

    def _convertToLength(self, s):
        from . import unit_parser, remove_length_unit
        if s[-1].isalpha():
            return remove_length_unit(unit_parser.parse(s))
        else:
            return float(s)

    def _convertToAngle(self, s):
        from . import unit_parser, remove_angle_unit
        if s[-1].isalpha():
            return remove_angle_unit(unit_parser.parse(s))
        else:
            return float(s)
