from __future__ import absolute_import

import xml.etree.ElementTree as ET
from .Component import Component

class Sphere(Component):

    def __init__(self, xml_elem):
        """
        Gets the radius for the sphere from
        its line in the XML file (xml line).
        The contents of this line are acessed with
        the xml.etree.ElementTree.Element object, xml_elem.
        """
        _convert = lambda x: self._convertToLength(xml_elem.get(x))
        self.radius = _convert("radius")
        return 

    def __str__(self):
        """
        Returns a string containing the SCAD
        code for this sphere objec.
        """
        return "sphere(r = {0!s}, $fn=100);".format(self.radius)

    def __eq__(self, rhs):
        """
        Returns true if the two Sphere components are equal. Returns false otherwise.
        """
        if type(self) != type(rhs):
            return False
        elif self.radius != rhs.radius:
            return False
        else:
            return True

    def __ne__(self, rhs):
        return not (self == rhs)
