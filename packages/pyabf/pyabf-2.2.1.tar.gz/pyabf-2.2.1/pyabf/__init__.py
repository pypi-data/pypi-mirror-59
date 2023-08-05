"""
pyABF - A Python interface to files in the Axon Binary Format (ABF)
    by Scott Harden

Documentation and code examples, and more can be found at:
    https://github.com/swharden/pyABF
"""

__version__ = '2.2.1'

import sys

if sys.version_info < (3, 6):
    sys.stdout.write("ERROR: pyabf "+__version__+" requires Python 3.6 or newer.\n")
    sys.stdout.write("pyabf 2.1.10 was the last version to support Python 2.7 and Python 3.5\n")
    sys.exit(1)

from pyabf.abf import ABF
from pyabf.atf import ATF

def info():
    """display information about the pyabf package."""
    import os
    _pyabfFolder = os.path.abspath(os.path.dirname(__file__))
    print("pyabf %s was imported from %s" % (__version__, _pyabfFolder))

def help():
    """launch the pyABF project page in a browser."""
    import webbrowser
    webbrowser.open("http://github.com/swharden/pyABF")