#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
__all__ = ['PyGle']

from .url import GoogleSearch, URLBuilder
from .extractor import (BaseExtractor,
                        ImageExtractor,
                        SearchExtractor,
                        NewsExtractor,
                        VideoExtractor,
                        PatentExtractor,
                        ShopExtractor,
                        BookExtractor,
                        Future)
from .url.url_constants import __google_url_modifiers__
from .version import print_ver_info


class PyGle(GoogleSearch):
    def __init__(self, query: str = None, enable_history: bool = False, use_session_cookies: bool = False):
        super().__init__(query)
        self.__search_extractor = SearchExtractor(must_use_session=use_session_cookies,
                                                  with_history_enabled=enable_history)
        self.__books_extractor = BookExtractor(must_use_session=use_session_cookies,
                                               with_history_enabled=enable_history)
        self.__image_extractor = ImageExtractor(must_use_session=use_session_cookies,
                                                with_history_enabled=enable_history)
        self.__news_extractor = NewsExtractor(must_use_session=use_session_cookies,
                                              with_history_enabled=enable_history)
        self.__patents_extractor = PatentExtractor(must_use_session=use_session_cookies,
                                                   with_history_enabled=enable_history)
        self.__shops_extractor = ShopExtractor(must_use_session=use_session_cookies,
                                               with_history_enabled=enable_history)
        self.__videos_extractor = VideoExtractor(must_use_session=use_session_cookies,
                                                 with_history_enabled=enable_history)
        self.__session_cookies = use_session_cookies
        self.__history_enabled = enable_history

    @staticmethod
    def __torify():
        import socks
        import socket

        socks.set_default_proxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
        socket.socket = socks.socksocket

    def doSearch(self, torify: bool = False) -> Future:
        url_builder_object = URLBuilder(self)
        ext = BaseExtractor(must_use_session=self.__session_cookies, with_history_enabled=self.__history_enabled)
        if self.search_at_different_pages:
            if self.search_at == __google_url_modifiers__["with_searching"]["books"]:
                ext = self.__books_extractor
            elif self.search_at == __google_url_modifiers__["with_searching"]["images"]:
                ext = self.__image_extractor
            elif self.search_at == __google_url_modifiers__["with_searching"]["news"]:
                ext = self.__news_extractor
            elif self.search_at == __google_url_modifiers__["with_searching"]["patents"]:
                ext = self.__patents_extractor
            elif self.search_at == __google_url_modifiers__["with_searching"]["shops"]:
                ext = self.__shops_extractor
            elif self.search_at == __google_url_modifiers__["with_searching"]["videos"]:
                ext = self.__videos_extractor
        else:
            ext = self.__search_extractor
        if torify:
            self.__torify()

        return ext.extract_url(url_builder_object)

    def pprintHistory(self):
        import pprint

        printer = pprint.PrettyPrinter(indent=4)
        if self.__history_enabled:
            history = self.getHistory()
            for key, value in history.items():
                if len(value) != 0:
                    print("Google {0} history".format(key))
                    printer.pprint(value)
        else:
            print("History is not enabled or no petition has been done yet")

    def getHistory(self) -> dict:
        return {"Books": self.__books_extractor.getHistory(),
                "Images": self.__image_extractor.getHistory(),
                "News": self.__news_extractor.getHistory(),
                "Patents": self.__patents_extractor.getHistory(),
                "Search": self.__search_extractor.getHistory(),
                "Shops": self.__shops_extractor.getHistory(),
                "Videos": self.__videos_extractor.getHistory()} if self.__history_enabled else {}

    def printOverallTime(self):
        if self.__history_enabled:
            history = self.getHistory()
            for key, value in history.items():
                if len(value) != 0:
                    print("Google {0} overall time".format(key))
                    if key == "Books":
                        self.__books_extractor.printOverallTime()
                    elif key == "Images":
                        self.__image_extractor.printOverallTime()
                    elif key == "News":
                        self.__news_extractor.printOverallTime()
                    elif key == "Patents":
                        self.__patents_extractor.printOverallTime()
                    elif key == "Search":
                        self.__search_extractor.printOverallTime()
                    elif key == "Shops":
                        self.__shops_extractor.printOverallTime()
                    elif key == "Videos":
                        self.__videos_extractor.printOverallTime()

    @staticmethod
    def version():
        print_ver_info()
