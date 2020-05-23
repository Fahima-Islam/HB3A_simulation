from __future__ import absolute_import

import xml.etree.ElementTree as ET
from .Component import Component

class GeneralizedCone(Component):

    def __init__(self, xml_elem):
        """
        Gets the major/minor axis values, scale, and height for the
        Generalized Cone from the attributes from its XML line.
        These attributes are accessed with the xml.etree.ElementTree
        Element object, xml_elem.
        """
        self.major = xml_elem.get("major")
        self.minor = xml_elem.get("minor")
        self.scale = xml_elem.get("scale")
        self.height = xml_elem.get("height")
        return

    def __str__(self):
        raise NotImplementedError("The OpenSCAD implementation for a Generalized Cone is not yet implemented.")
