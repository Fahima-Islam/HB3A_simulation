from __future__ import absolute_import

from .Nary import Nary

class Union(Nary):

    def __init__(self):
        """
        Stores the n components for the Union
        operation in a member list self.comps and
        self.comp2.
        """
        Nary.__init__(self)
        return

    def __str__(self):
        """
        Returns a string containing the SCAD
        code for implementing the Union.
        """
        tmp_str="""union() {\n"""
        for comp in self.comps:
            tmp_str=tmp_str+"""    {0!s}\n""".format(comp)
        tmp_str=tmp_str+"""}"""
        return tmp_str
