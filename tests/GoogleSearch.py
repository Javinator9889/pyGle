#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
import unittest

from pyGle import PyGle


class BuiltInSearchTest(unittest.TestCase):
    def setUp(self):
        self.search = PyGle(enable_history=True, use_session_cookies=True)


