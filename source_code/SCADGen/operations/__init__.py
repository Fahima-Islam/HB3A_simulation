from __future__ import absolute_import

import pyre.units
unit_parser = pyre.units.parser()
length_unit = unit_parser.parse("1*mm")
angle_unit = unit_parser.parse("1*deg")

from .Binary import Binary
from .Difference import Difference
from .Dilation import Dilation
from .Intersection import Intersection
from .Reflection import Reflection
from .Rotation import Rotation
from .Transformation import Transformation
from .Translation import Translation
from .Union import Union

def remove_length_unit(x):
    x + length_unit
    return x/length_unit

def remove_angle_unit(x):
    x + angle_unit
    return x/angle_unit

def dilation(attrs):
    assert(attrs[0].tag == "scale")
    return Dilation(float(attrs[0].text))

def reflection(attrs):
    assert(attrs[0].tag == "vector")
    return Reflection(attrs[0].text)

def reversal(attrs):
    raise NotImplementedError("Reversal is not yet implemented.")

def rotation(attrs):
    assert(len(attrs) >= 2)
    assert((attrs[0].tag == "angle" and attrs[1].tag == "axis")
        or (attrs[0].tag == "axis" and attrs[1].tag == "angle"))
    angle = None
    axis = None
    if attrs[0].tag == "angle":
        angle = attrs[0]
        axis = attrs[1]
    else:
        angle = attrs[1]
        axis = attrs[0]
    return Rotation(angle.text, axis)

def translation(attrs):
    assert(attrs[0].tag == "vector")
    return Translation(attrs[0])

unary_dict = { "dilation" : dilation, "reflection" : reflection, "reversal" : reversal, "rotation" : rotation, "translation" : translation }
