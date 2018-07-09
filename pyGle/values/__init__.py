#
#                py-google-search  Copyright (C) 2018  Javinator9889
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
from url.url_constants import __google_url_modifiers__


class TimeLimit:
    def __init__(self):
        self.__time_limit = None
        self.__times: dict = __google_url_modifiers__["with_time_limitation_for"]

    def setDay(self):
        self.__time_limit = self.__times["day"]

    def setWeek(self):
        self.__time_limit = self.__times["week"]

    def setMonth(self):
        self.__time_limit = self.__times["month"]

    def setYear(self):
        self.__time_limit = self.__times["year"]

    def setMonths(self, time: int):
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
        self.__available_rights: dict = __google_url_modifiers__["with_rights_types"]

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
        self.__available_lang: dict = __google_url_modifiers__["with_languages"]

    def show_languages(self):
        for key, value in self.__available_lang.items():
            print(key)

    def setLanguage(self, language: str):
        self.__lang = self.__available_lang[language]

    def getLanguage(self):
        # type: () -> str
        return self.__lang


class Countries:
    def __init__(self):
        self.__country = None
        self.__available_countries: dict = __google_url_modifiers__["with_countries"]

    def show_countries(self):
        for key, values in self.__available_countries.items():
            print(key)

    def setCountry(self, country: str):
        self.__country = self.__available_countries[country]

    def getCountry(self):
        # type: () -> str
        return self.__country


class Dates:
    def __init__(self):
        self.__date_one = None
        self.__date_two = None

    def setFirstDate(self, day, month, year):
        from datetime import datetime

        self.__date_one = datetime.strftime(day + '.' + month + '.' + year, "%d.%m.%Y")

    def setSecondDate(self, day, month, year):
        from datetime import datetime

        self.__date_two = datetime.strftime(day + '.' + month + '.' + year, "%d.%m.%Y")

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

    def searchApps(self):
        self.__google_page = self.__available_google_pages["apps"]

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

    def setColor(self, color: str = None):
        if not color:
            self.showColors()
        else:
            if color in self.__available_images_modifiers["color"]:
                self.__image_params["image_color"] = self.__available_images_modifiers["color"][color]
            else:
                print("Color not found. Colors:")
                self.showColors()

    def setColorType(self, color_type: str = None):
        if not color_type:
            self.showColorTypes()
        else:
            if color_type in self.__available_images_modifiers["color_type"]:
                self.__image_params["color_type"] = self.__available_images_modifiers["color_type"][color_type]
            else:
                print("Color-Type not found. Color-Types:")
                self.showColorTypes()

    def setImageRights(self, rights: str = None):
        if not rights:
            self.showImageRights()
        else:
            if rights in self.__available_images_modifiers["image_rights"]:
                self.__image_params["rights"] = self.__available_images_modifiers["image_rights"][rights]
            else:
                print("Rights not found. Rights:")
                self.showImageRights()

    def setImageSize(self, size: str = None):
        if not size:
            self.showImageSizes()
        else:
            if size in self.__available_images_modifiers["image_size"]:
                self.__image_params["size"] = self.__available_images_modifiers["image_size"][size]
            else:
                print("Size not found. Sizes:")
                self.showImageSizes()

    def setImageType(self, image_type: str = None):
        if not image_type:
            self.showImageTypes()
        else:
            if image_type in self.__available_images_modifiers["image_type"]:
                self.__image_params["type"] = self.__available_images_modifiers["image_type"][image_type]
            else:
                print("Image type not found. Types:")
                self.showImageTypes()

    def setAspectRatio(self, aspect_ratio: str = None):
        if not aspect_ratio:
            self.showAspectRatios()
        else:
            if aspect_ratio in self.__available_images_modifiers["aspect_ratio"]:
                self.__image_params["aspect_ratio"] = self.__available_images_modifiers["aspect_ratio"][aspect_ratio]
            else:
                print("Aspect ratio not found. Ratios:")
                self.showAspectRatios()

    def setImageFormat(self, image_format: str = None):
        if not image_format:
            self.showImageFormats()
        else:
            if image_format in self.__available_images_modifiers["format"]:
                self.__image_params["image_format"] = self.__available_images_modifiers["format"][image_format]
            else:
                print("Format not found. Formats:")
                self.showImageFormats()

    def getImageParams(self) -> dict:
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

    def __print_keys_in_dict(self, source_key: str):
        for key, value in self.__available_images_modifiers[source_key].items():
            print(key)

