class Nary:

    def __init__(self):
        self.comps = []
        self.num_comps = 0
        return

    def isComp(self):
        return False

    def addComp(self, component):
        self.comps.append(component)
        self.num_comps += 1

    def __eq__(self, rhs):
        """
        Returns true if two Nary opeations are equal. Returns false otherwise.
        """
        if type(self) != type(rhs):
            return False
        for compl, compr in zip(self.comps, rhs.comps):
            if compl != compr:
                return False
        return True

    def __ne__(self, rhs):
        return not (self == rhs)

    def __getitem__(self, index):
        return self.comps[index]
