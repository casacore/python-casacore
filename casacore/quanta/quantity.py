from six import string_types
from ._quanta import QuantVec
from ._quanta import Quantity
from ._quanta import from_string, from_dict, from_dict_v


def is_quantity(q):
    """Indicate whether the object is a valid quantity"""
    return isinstance(q, QuantVec) or isinstance(q, Quantity)


# Quantity returns new Quantities, so we need to insert these
# functions into Quantity
def new_get_value(quant, *args):
    val = QuantVec._get_value(quant, *args)
    if len(val) == 1:
        return val[0]
    else:
        return val


QuantVec.get_value = new_get_value


def to_string(quant, fmt="%0.5g"):
    val = quant.get_value()
    if hasattr(val, "__len__"):
        fmt = "[" + ", ".join([fmt % i for i in val]) + "] %s"
        return fmt % quant.get_unit()
    fmt += " %s"
    return fmt % (val, quant.get_unit())


QuantVec.to_string = to_string
Quantity.to_string = to_string
QuantVec.__str__ = to_string
Quantity.__str__ = to_string


# QuantVec.__repr__ = to_string
# Quantity.__repr__ = to_string


def quantity(*args):
    """Create a quantity. This can be from a scalar or vector.

    Example::

      q1 = quantity(1.0, "km/s")
      q2 = quantity("1km/s")
      q1 = quantity([1.0,2.0], "km/s")

    """
    if len(args) == 1:
        if isinstance(args[0], string_types):
            # use copy constructor to create quantity from string
            return Quantity(from_string(args[0]))
        elif isinstance(args[0], dict):
            if hasattr(args[0]["value"], "__len__"):
                return QuantVec(from_dict_v(args[0]))
            else:
                return Quantity(from_dict(args[0]))
        elif isinstance(args[0], Quantity) or isinstance(args[0], QuantVec):
            return args[0]
        else:
            raise TypeError("Invalid argument type for")
    else:
        if hasattr(args[0], "__len__"):
            return QuantVec(*args)
        else:
            return Quantity(*args)
