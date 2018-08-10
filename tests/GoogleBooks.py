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
                          GoogleBooks)


class BuiltInSearchTest(unittest.TestCase):
    def setUp(self):
        self.search = PyGle(enable_history=True, use_session_cookies=True)
        page = GooglePages()
        page.searchBooks()
        self.search.withSearchingAtDifferentGooglePages(page)
        self.printer = pprint.PrettyPrinter(indent=4)

    def __search(self):
        ft = self.search.doSearch()
        self.printer.pprint(ft.result())

    def test_search_books(self):
        self.search.withQuery("test")
        self.__search()

    def test_search_books_with_params(self):
        params = GoogleBooks()
        params.searchOnlyBooks()
        params.searchOnlyBooksWithPreview()
        self.search.withQuery("test").withBookParams(params)
        self.__search()
