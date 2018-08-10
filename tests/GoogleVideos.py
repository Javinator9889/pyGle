#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
import unittest
import pprint

from pyGle import PyGle
from pyGle.values import (GooglePages,
                          GoogleImages,
                          AvailableColors,
                          GoogleVideos)

PyGle.version()


class BuiltInSearchTest(unittest.TestCase):
    def setUp(self):
        self.search = PyGle(enable_history=True, use_session_cookies=True)
        page = GooglePages()
        page.searchVideos()
        self.search.withSearchingAtDifferentGooglePages(page)
        self.printer = pprint.PrettyPrinter(indent=4)

    def __search(self):
        ft = self.search.doSearch()
        self.printer.pprint(ft.result())

    def test_search(self):
        self.search.withQuery("test")
        self.__search()

    def test_search_with_params(self):
        params = GoogleVideos()
        params.withShortDuration()
        params.withHighQualityVideos()
        params.withSubtitles()
        self.search.withQuery("test").withVideoParams(params)
        self.__search()

    def test_fail_search_no_image_params(self):
        params = GoogleImages()
        params.setColor(AvailableColors.Orange)
        self.search.withImageParams(params).withQuery("test")
        self.__search()
