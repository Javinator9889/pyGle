#
#                py-google-search  Copyright (C) 2018  Javinator9889
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#

__version__ = "v1.21b"
__version_code__ = 91


def print_ver_info():
    import sys

    print("pyGle {0}".format(__version__))
    print("Python {0}".format(sys.version.replace("\n", ' ')))
