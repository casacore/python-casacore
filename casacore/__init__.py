__version__ = "3.6.0a1"
__mincasacoreversion__ = "3.1.1"

import os

# If environment variable `AIPSPATH` is not set, then set it to the directory
# containing the `.aipsrc` file that is distributed with this package.
# This `.aipsrc` file uses the environment `CASACORE_DATA`, which should point
# to the directory containing the casacore data files.
if "AIPSPATH" not in os.environ:
    root = os.path.dirname(__file__)
    os.environ["AIPSPATH"] = root
    os.environ["CASACORE_DATADIR"] = os.path.join(root, "data")
