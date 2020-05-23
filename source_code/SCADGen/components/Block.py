from __future__ import absolute_import

import xml.etree.ElementTree as ET
from .Component import Component

class Block(Component):

    def __init__(self, xml_elem):
        """
        Gets width, height, and thickness from the
        `diagonal` tag in the XML file. This tag is
        accessed with the xml.etree.ElementTree.Element
        object, xml_elem.
        """
        _convert = lambda x: self._convertToLength(xml_elem.get(x))
        thickness, width, height = map(_convert, "thickness width height".split())
        self.x, self.y, self.z = thickness, width, height
        return 

    def __str__(self):
        """
        Returns a string containing the SCAD
        code for this block/cube object.
        """
        return "cube([{0!s}, {1!s}, {2!s}], center=true);".format(self.x, self.y, self.z)

    def __eq__(self, rhs):
        """
        Returns true if two components are equal Blocks. Returns false otherwise.
        """
        if type(self) != type(rhs):
            return False
        elif self.x != rhs.x or self.y != rhs.y or self.z != rhs.z:
            return False
        else:
            return True

    def __ne__(self, rhs):
        return not (self == rhs)
