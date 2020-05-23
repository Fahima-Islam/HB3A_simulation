from __future__ import absolute_import

import pyre.units
unit_parser = pyre.units.parser()
length_unit = unit_parser.parse('1*mm')

def remove_length_unit(x):
    x + length_unit # make sure unit is right
    return x/length_unit

from .Block import Block
from .Cone import Cone
from .Cylinder import Cylinder
from .Pyramid import Pyramid
from .Sphere import Sphere
from .Torus import Torus
