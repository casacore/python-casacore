from pyrap_quanta._quanta import Quantity
from  pyrap_quanta._quanta import from_string, from_dict


# Quantity returns new Quantities, so we need to insert these
# functions into Quantity
def new_get_value(quant, *args):
    val = Quantity._get_value(quant, *args)
    if len(val) == 1:
	return val[0]
    else:
	return val
Quantity.get_value = new_get_value

def to_string(quant):
    return "%s %s" % (str(quant.get_value()), quant.get_unit())
Quantity.__str__ = to_string

# the c++ constuctor doesn't take strings, so use a global method and 
# add to constructor here.
class quantity(Quantity):
    def __init__(self, *args):
	if len(args) == 1:
	    if isinstance(args[0], str):
		# use copy constructor to create quantity from string
		Quantity.__init__(self, from_string(args[0]))
	    elif isinstance(args[0], dict):
		Quantity.__init__(self, from_dict(args[0]))
	else:
	    Quantity.__init__(self, *args)
