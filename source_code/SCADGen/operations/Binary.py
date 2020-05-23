from __future__ import absolute_import

from .Nary import Nary

class Binary(Nary):

    def __init__(self):
        Nary.__init__(self)
        return

    def isComp(self):
        return False

    def addComp(self, component):
        if self.num_comps < 2:
            Nary.addComp(self, component)
        else:
            raise AttributeError("A binary operation cannot have more than 2 components.")
