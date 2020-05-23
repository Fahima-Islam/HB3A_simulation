from __future__ import absolute_import

from .Transformation import Transformation

class Reflection(Transformation):

    def __init__(self, vector):
        """
        Stores the component for the Reflection and
        the normal vector of the reflection plane in
        member variables self.body and self.vector.
        """
        Transformation.__init__(self)
        self.vector = []
        v = vector[1:-1]
        comma1 = v.find(",")
        comma2 = v[comma1+1:].find(",") + comma1 + 1
        self.vector.append(float(v[:comma1].replace(" ", "")))
        self.vector.append(float(v[comma1+1:comma2].replace(" ", "")))
        self.vector.append(float(v[comma2+1:].replace(" ", "")))
        return

    def __str__(self):
        """
        Returns a string containing the SCAD
        code for the reflection.
        """
        return """mirror([{0!s}, {1!s}, {2!s}]) {{
    {3!s}
}}""".format(self.vector[0], self.vector[1], self.vector[2], self.body)

    def __eq__(self, rhs):
        """
        Returns true if the two Reflection objects are equal. Returns false otherwise.
        """
        if type(self) != type(rhs):
            return False
        elif self.body != rhs.body or self.vector != rhs.vector:
            return False
        else:
            return True

    def __ne__(self, rhs):
        return not (self == rhs)
