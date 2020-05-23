from __future__ import absolute_import

from .Nary import Nary

class Intersection(Nary):

    def __init__(self):
        """
        Stores the components for the Intersection
        in member variables self.comp1 self.comp2.
        """
        Nary.__init__(self)
        return

    def __str__(self):
        """
        Returns a string containing the SCAD
        code for implementing an intersection.
        """
        tmp_str = """intersection() {\n"""
        for comp in self.comps:
            tmp_str = tmp_str + """    {0!s}\n""".format(comp)
        tmp_str = tmp_str + """}"""
        return tmp_str
