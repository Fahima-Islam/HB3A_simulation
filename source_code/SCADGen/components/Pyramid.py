from __future__ import absolute_import

import xml.etree.ElementTree as ET
from .Component import Component

class Pyramid(Component):

    def __init__(self, xml_elem):
        """
        Gets the base dimensions and height for the cone
        from the attributes from its XML line. These attributes
        are accessed with the xml.etree.ElementTree object,
        xml_elem. This will likely need to be changed later
        once the "formal" xml format is added to pyre.
        """
        _convert = lambda x: self._convertToLength(xml_elem.get(x))
        self.x, self.y, self.z = map(_convert, "thickness width height".split())
        return;

    def __str__(self):
        """
        Returns a string containing the SCAD code for this
        Cone object.
        """
        return """polyhedron(
    points=[ [{0!s},{1!s},-{2!s}], [{0!s},-{1!s},-{2!s}],
             [-{0!s},-{1!s},-{2!s}], [-{0!s},{1!s},-{2!s}], [0,0,0] ],
    faces=[ [0,1,4], [1,2,4], [2,3,4], [3,0,4], [1,0,3], [2,1,3] ]
);""".format((self.x/2), (self.y/2), self.z)

    def __eq__(self, rhs):
        """
        Returns true if the two Pyramids are equal. Returns false otherwise.
        """
        if type(self) != type(rhs):
            return False
        elif self.x != rhs.x or self.y != rhs.y or self.z != rhs.z:
            return False
        else:
            return True

    def __ne__(self, rhs):
        return not (self == rhs)
