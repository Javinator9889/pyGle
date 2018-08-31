# -*- coding: utf-8 -*-
#
#                py-google-search  Copyright (C) 2018  Javinator9889
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
from pyGle.url.url_constants import __google_url_modifiers__

from .AvailableCountries import AvailableCountries
from .AvailableLanguages import AvailableLanguages
from .OptionsForPatents import *
from .OptionsForPictures import *


class TimeLimit:
    def __init__(self):
        self.__time_limit = None
        self.__times = __google_url_modifiers__["with_time_limitation_for"]

    def setDay(self):
        self.__time_limit = self.__times["day"]

    def setWeek(self):
        self.__time_limit = self.__times["week"]

    def setMonth(self):
        self.__time_limit = self.__times["month"]

    def setYear(self):
        self.__time_limit = self.__times["year"]

    def setMonths(self, time):
        # type: (int) -> None
        if time <= 0:
            raise ValueError("Time must be greater than '0'")
        else:
            self.__time_limit = self.__times["month"] + str(time)

    def getTimeLimit(self):
        # type: () -> str
        return self.__time_limit


class Rights:
    def __init__(self):
        self.__rights = None
        self.__available_rights = __google_url_modifiers__["with_rights_types"]

    def setFreeToUse(self):
        self.__rights = self.__available_rights["free_to_use"]

    def setFreeToUseCommerciallyAlso(self):
        self.__rights = self.__available_rights["free_to_use_com"]

    def setFreeToUseAndModify(self):
        self.__rights = self.__available_rights["free_to_use_and_modify"]

    def setFreeToUseAndModifyCommerciallyAlso(self):
        self.__rights = self.__available_rights["free_to_use_and_modify_com"]

    def getRights(self):
        # type: () -> str
        return self.__rights


class Languages:
    def __init__(self):
        self.__lang = None
        self.__available_lang = __google_url_modifiers__["with_languages"]

    def show_languages(self):
        for key, value in self.__available_lang.items():
            print(key)

    def setLanguage(self, language):
        # type: (AvailableLanguages) -> None
        self.__lang = language

    def getLanguage(self):
        # type: () -> str
        return self.__lang


class Countries:
    def __init__(self):
        self.__country = None
        self.__available_countries = __google_url_modifiers__["with_countries"]

    def show_countries(self):
        for key, values in self.__available_countries.items():
            print(key)

    def setCountry(self, country):
        # type: (AvailableCountries) -> None
        self.__country = country

    def getCountry(self):
        # type: () -> str
        return self.__country


class Dates:
    def __init__(self):
        self.__date_one = None
        self.__date_two = None

    def setFirstDate(self, day, month, year):
        # type: (int, int, int) -> None
        from datetime import datetime

        self.__date_one = datetime(year, month, day).strftime("%d.%m.%Y")

    def setSecondDate(self, day, month, year):
        # type: (int, int, int) -> None
        from datetime import datetime

        self.__date_two = datetime(year, month, day).strftime("%d.%m.%Y")

    def getDates(self):
        # type: () -> list
        return [self.__date_one, self.__date_two]


class GooglePages:
    def __init__(self):
        self.__google_page = None
        self.__available_google_pages = __google_url_modifiers__["with_searching"]

    def searchImage(self):
        self.__google_page = self.__available_google_pages["images"]

    def searchNews(self):
        self.__google_page = self.__available_google_pages["news"]

    def searchBooks(self):
        self.__google_page = self.__available_google_pages["books"]

    def searchShops(self):
        self.__google_page = self.__available_google_pages["shops"]

    def searchVideos(self):
        self.__google_page = self.__available_google_pages["videos"]

    def searchPatents(self):
        self.__google_page = self.__available_google_pages["patents"]

    def getGooglePage(self):
        # type: () -> str
        return self.__google_page


class GoogleImages:
    def __init__(self):
        self.__available_images_modifiers = __google_url_modifiers__["with_image_params"]
        self.__image_params = {
            "image_color": None,
            "color_type": None,
            "rights": None,
            "size": None,
            "type": None,
            "aspect_ratio": None,
            "image_format": None
        }

    def setColor(self, color):
        # type: (AvailableColors) -> None
        self.__image_params["image_color"] = color

    def setColorType(self, color_type):
        # type: (AvailableColorsType) -> None
        self.__image_params["color_type"] = color_type

    def setImageRights(self, rights):
        # type: (AvailableRights) -> None
        self.__image_params["rights"] = rights

    def setImageSize(self, size):
        # type: (AvailableSizes) -> None
        self.__image_params["size"] = size

    def setImageType(self, image_type):
        # type: (AvailableImagesTypes) -> None
        self.__image_params["type"] = image_type

    def setAspectRatio(self, aspect_ratio):
        # type: (AvailableAspectRatios) -> None
        self.__image_params["aspect_ratio"] = aspect_ratio

    def setImageFormat(self, image_format):
        # type: (AvailableImageFormats) -> None
        self.__image_params["image_format"] = image_format

    def getImageParams(self):
        # type: () -> dict
        return self.__image_params

    def showColors(self):
        self.__print_keys_in_dict("color")

    def showColorTypes(self):
        self.__print_keys_in_dict("color_type")

    def showImageRights(self):
        self.__print_keys_in_dict("image_rights")

    def showImageSizes(self):
        self.__print_keys_in_dict("image_size")

    def showImageTypes(self):
        self.__print_keys_in_dict("image_type")

    def showAspectRatios(self):
        self.__print_keys_in_dict("aspect_ratio")

    def showImageFormats(self):
        self.__print_keys_in_dict("format")

    def __print_keys_in_dict(self, source_key):
        # type: (str) -> None
        for key, value in self.__available_images_modifiers[source_key].items():
            print(key)


class GooglePatents:
    def __init__(self):
        self.__available_patents_modifiers = __google_url_modifiers__["with_patents_params"]
        self.__patents_params = {
            "office_patents": None,
            "patent_status": None,
            "patent_type": None
        }

    def setOfficePatent(self, office_patent):
        # type: (OfficePatents) -> None
        self.__patents_params["office_patents"] = office_patent

    def setPatentStatus(self, status):
        # type: (PatentStatus) -> None
        self.__patents_params["patent_status"] = status

    def setPatentType(self, patent_type):
        # type: (AvailablePatentTypes) -> None
        self.__patents_params["patent_type"] = patent_type

    def getPatentModifiers(self):
        # type: () -> dict
        return self.__patents_params


class GoogleShop:
    def __init__(self):
        self.__available_shop_modifiers = __google_url_modifiers__["with_shop_params"]
        self.__shop_params = {
            "sort_order": None,
            "new_products": None,
            "max_price": None,
            "min_price": None
        }

    def onlyNewProducts(self):
        self.__shop_params["new_products"] = self.__available_shop_modifiers["only_new_products"]

    def orderByLowerToHigherPrice(self):
        self.__shop_params["sort_order"] = self.__available_shop_modifiers["sort_order_less_to_high"]

    def orderByHigherToLowerPrice(self):
        self.__shop_params["sort_order"] = self.__available_shop_modifiers["sort_order_high_to_less"]

    def orderByReviewScore(self):
        self.__shop_params["sort_order"] = self.__available_shop_modifiers["sort_order_reviews"]

    def withMinPrice(self, price):
        # type: (int) -> None
        self.__shop_params["min_price"] = self.__available_shop_modifiers["with_min_price"].format(str(price))

    def withMaxPrice(self, price):
        # type: (int) -> None
        self.__shop_params["max_price"] = self.__available_shop_modifiers["with_max_price"].format(str(price))

    def betweenTwoPrices(self, min_price, max_price):
        # type: (int, int) -> None
        self.__shop_params["min_price"] = self.__available_shop_modifiers["with_min_price"].format(str(min_price))
        self.__shop_params["max_price"] = self.__available_shop_modifiers["with_max_price"].format(str(max_price))

    def getShopModifiers(self):
        # type: () -> dict
        return self.__shop_params


class GoogleBooks:
    def __init__(self):
        self.__available_books_modifiers = __google_url_modifiers__["with_books_params"]
        self.__books_params = {
            "books_type": None,
            "with_searching": None
        }

    def searchOnlyBooksWithPreview(self):
        self.__books_params["books_type"] = self.__available_books_modifiers["books_with_preview"]

    def searchOnlyGoogleEBooks(self):
        self.__books_params["books_type"] = self.__available_books_modifiers["google_ebooks"]

    def searchOnlyFreeEBooks(self):
        self.__books_params["books_type"] = self.__available_books_modifiers["free_ebooks"]

    def searchOnlyBooks(self):
        self.__books_params["with_searching"] = self.__available_books_modifiers["with_searching_books"]

    def searchOnlyNewsPapers(self):
        self.__books_params["with_searching"] = self.__available_books_modifiers["with_searching_news"]

    def searchOnlyMagazines(self):
        self.__books_params["with_searching"] = self.__available_books_modifiers["with_searching_magazines"]

    def getBooksModifiers(self):
        # type: () -> dict
        return self.__books_params


class GoogleVideos:
    def __init__(self):
        self.__available_video_modifiers = __google_url_modifiers__["with_video_params"]
        self.__video_params = {
            "duration": None,
            "high_quality": None,
            "subtitles": None
        }

    def withShortDuration(self):
        self.__video_params["duration"] = self.__available_video_modifiers["duration"]["short"]

    def withMediumDuration(self):
        self.__video_params["duration"] = self.__available_video_modifiers["duration"]["medium"]

    def withLongDuration(self):
        self.__video_params["duration"] = self.__available_video_modifiers["duration"]["long"]

    def withHighQualityVideos(self):
        self.__video_params["high_quality"] = self.__available_video_modifiers["high_quality"]

    def withSubtitles(self):
        self.__video_params["subtitles"] = self.__available_video_modifiers["with_subtitles"]

    def getVideoModifiers(self):
        # type: () -> dict
        return self.__video_params
