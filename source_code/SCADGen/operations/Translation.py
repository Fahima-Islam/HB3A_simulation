from __future__ import absolute_import

from .Transformation import Transformation
import xml.etree.ElementTree as ET

class Translation(Transformation):

    def __init__(self, vector):
        """
        Stores the component for the translation and
        the translation directions in member variables
        self.body and self.vector.
        """
        Transformation.__init__(self)
        from . import unit_parser, length_unit
        _convert = lambda x: self._convertToLength(vector.get(x))
        beam, transversal, vertical = map(_convert, "beam transversal vertical".split())
        self.vector = []
        self.vector.append(beam)
        self.vector.append(transversal)
        self.vector.append(vertical)
        """self.vector = []
        v = vector[1:-1]
        comma1 = v.find(",")
        comma2 = v[comma1+1:].find(",") + comma1 + 1
        self.vector.append(float(v[:comma1].replace(" ", "")))
        self.vector.append(float(v[comma1+1:comma2].replace(" ", "")))
        self.vector.append(float(v[comma2+1:].replace(" ", "")))"""
        return

    def __str__(self):
        """
        Returns a string containing the SCAD code
        for the translation.
        """
        return """translate([{0!s}, {1!s}, {2!s}]) {{
    {3!s}
}}""".format(self.vector[0], self.vector[1], self.vector[2], self.body)

    def __eq__(self, rhs):
        """
        Returns true if the two Translation operations are equal. Returns false otherwise.
        """
        if type(self) != type(rhs):
            return False
        elif self.body != rhs.body or self.vector != rhs.vector:
            return False
        else:
            return True

    def __ne__(self, rhs):
        return not (self == rhs)
