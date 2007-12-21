from pyrap_quanta._quanta import Quantity
from pyrap_quanta._quanta import QuantVec
from pyrap_quanta._quanta import from_string, from_dict, from_dict_v

def is_quantity(q):
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

def to_string(quant):
    return "%s %s" % (str(quant.get_value()), quant.get_unit())
QuantVec.__str__ = to_string
Quantity.__str__ = to_string

def quantity(*args):
    if len(args) == 1:
        if isinstance(args[0], str):
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

