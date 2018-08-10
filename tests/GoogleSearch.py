#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
import unittest
import pprint

from pyGle import PyGle


class BuiltInSearchTest(unittest.TestCase):
    def setUp(self):
        self.search = PyGle(enable_history=True, use_session_cookies=True)
        self.printer = pprint.PrettyPrinter(indent=4)

    def __search(self):
        ft = self.search.doSearch()
        self.printer.pprint(ft.result())

    def test_do_normal_search(self):
        self.search.withQuery("test")
        self.__search()

    def test_search_with_lang(self):
        from pyGle.values import Languages
        from pyGle.values.AvailableLanguages import AvailableLanguages

        lang = Languages()
        lang.setLanguage(AvailableLanguages.English)

        self.search.withQuery("test").withResultsLanguage(lang)
        self.__search()

    def test_search_with_interface_lang(self):
        from pyGle.values import Languages, AvailableLanguages, InterfaceLanguages

        lang = Languages()
        lang.setLanguage(AvailableLanguages.English)

        self.search.withQuery("test").withResultsLanguage(lang)\
            .withInterfaceLanguage(InterfaceLanguages.InterfaceLanguages.English)
        self.__search()

    def test_search_dates(self):
        from pyGle.values import Dates

        date = Dates()
        date.setFirstDate(10, 10, 2010)
        date.setSecondDate(10, 11, 2018)

        self.search.withQuery("test").withSortByUpdateTime()
        self.__search()

        self.search.withQuery("test").withSearchBetweenTwoDates(date)
        self.__search()

    def test_words_in_order(self):
        self.search.withQuery("test").withWordsInSpecificOrderSearch(["speed", "test"])
        self.__search()

    def test_words_in_result(self):
        self.search.withQuery("test").withOneOrMoreWordsInResult(["speed"])
        self.__search()

    def test_with_words_excluded(self):
        self.search.withQuery("test").withExcludedWords(["speed"])
        self.__search()

    def test_with_timelimit(self):
        from pyGle.values import TimeLimit

        limit = TimeLimit()
        limit.setDay()
        self.search.withQuery("test").withTimeLimit(limit)
        self.__search()
        limit.setMonth()
        self.search.withQuery("test").withTimeLimit(limit)
        self.__search()
        limit.setMonths(3)
        self.search.withQuery("test").withTimeLimit(limit)
        self.__search()
        limit.setYear()
        self.search.withQuery("test").withTimeLimit(limit)
        self.__search()

    def test_with_synonymous_searching_word(self):
        self.search.withQuery("test").withSynonymousSearchingToAWord("prueba")
        self.__search()

    def test_search_with_results_at_country(self):
        from pyGle.values import Countries, AvailableCountries

        c = Countries()
        c.setCountry(AvailableCountries.UnitedKingdom)
        self.search.withQuery("spain").withResultsAtCountry(c)
        self.__search()
