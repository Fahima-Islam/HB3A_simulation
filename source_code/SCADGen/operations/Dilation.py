from __future__ import absolute_import

from .Transformation import Transformation

class Dilation(Transformation):

    def __init__(self, scale):
        """
        Stores the component for the Dilation and
        the scaling factor in member variables
        self.body and self.scale.
        """
        Transformation.__init__(self)
        self.scale = scale
        return

    def __str__(self):
        """
        Returns a string containing the SCAD
        code for the dilation.
        """
        return """scale([{0!s}, {0!s}, {0!s}]) {{
    {1!s}
}}""".format(self.scale, self.body)

    def __eq__(self, rhs):
        """
        Returns true if the two Dilation operations are equal. Returns false otherwise.
        """
        if type(self) != type(rhs):
            return False
        elif self.body != rhs.body or self.scale != rhs.scale:
            return False
        else:
            return True

    def __ne__(self, rhs):
        return not (self == rhs)
