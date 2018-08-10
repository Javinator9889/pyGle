#
#                py-google-search  Copyright (C) 2018  Javinator9889
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
import urllib.parse

from .url_constants import __google_base_url__, __google_url_modifiers__
from pyGle.values import *
from pyGle.values.InterfaceLanguages import InterfaceLanguages


class GoogleSearch:
    def __init__(self, query: str = None):
        self.query = query
        self.words_in_order = None
        self.or_words = None
        self.words_excluded = None
        self.number_of_results = None
        self.filetype = None
        self.sitesearch = None
        self.time_limit = None
        self.rights = None
        self.words_in_title = None
        self.words_in_body = None
        self.words_in_url = None
        self.words_in_anchor = None
        self.between_two_numbers = None
        self.synonym = None
        # self.define = None
        self.containing_two_words = None
        # self.operation = None
        self.safe = None
        self.related = None
        self.linked = None
        self.personalized_search = None
        self.results_lang = None
        self.country = None
        self.document_country = None
        self.search_between_two_dates = None
        self.sort_by_update_time = None
        self.search_at_different_pages = False
        self.search_at = None
        self.start_position = None
        self.image_params = None
        self.patents_params = None
        self.shop_params = None
        self.interface_language = None
        self.book_params = None
        # self.search_extractor = None

    def withQuery(self, query: str):
        self.query = query.replace(' ', '+')
        return self

    def withWordsInSpecificOrderSearch(self, words: list):
        self.words_in_order = '+'.join(words)
        return self

    def withOneOrMoreWordsInResult(self, words: list):
        self.or_words = '+'.join(words)
        return self

    def withExcludedWords(self, words: list):
        self.words_excluded = '+'.join(words)
        return self

    def withNumberOfResults(self, results: int = 10):
        self.number_of_results = str(results)
        return self

    def withFileSearchByFileType(self, filetype: str):
        self.filetype = filetype.replace(' ', '+')
        return self

    def withSiteSearch(self, site: str):
        self.sitesearch = site.replace(' ', '+')
        return self

    def withTimeLimit(self, time_limit: TimeLimit):
        self.time_limit = time_limit.getTimeLimit()
        return self

    def withRights(self, rights: Rights):
        self.rights = rights.getRights()
        return self

    def withTextInTitle(self, text: str):
        self.words_in_title = text.replace(' ', '+')
        return self

    def withTextInBody(self, text: str):
        self.words_in_body = text.replace(' ', '+')
        return self

    def withTextInUrl(self, text: str):
        self.words_in_url = text.replace(' ', '+')
        return self

    def withTextInAnchor(self, text: str):
        self.words_in_anchor = text.replace(' ', '+')
        return self

    def withResultBetweenTwoNumbers(self, first_number: float, second_number: float):
        self.between_two_numbers = [str(first_number), str(second_number)]
        return self

    def withRelatedPagesToADocument(self, document_url: str):
        self.related = document_url.replace(' ', '+')
        return self

    def withSynonymousSearchingToAWord(self, word: str):
        self.synonym = word.replace(' ', '+')
        return self

    # def withDefiningTerm(self, term: str):
    #     self.define = term.replace(' ', '+')
    #     return self

    def withContainingTwoTerms(self, first_term: str, second_term: str):
        self.containing_two_words = [first_term.replace(' ', '+'), second_term.replace(' ', '+')]
        return self

    # def withArithmeticOperation(self, operation: str):
    #     self.operation = operation.replace(' ', '').replace('+', "%2B")
    #     return self

    def withSafeModeActivated(self):
        self.safe = __google_url_modifiers__["with_safe_active"]
        return self

    def withSafeModeDeactivated(self):
        self.safe = __google_url_modifiers__["with_safe_deactivated"]
        return self

    def withLinkingToUrl(self, url: str):
        self.linked = url.replace(' ', '+')
        return self

    def withPersonalizedSearch(self):
        self.personalized_search = __google_url_modifiers__["with_personalized_search"]
        return self

    def withNoPersonalizedSearch(self):
        self.personalized_search = __google_url_modifiers__["with_no_personalized_search"]
        return self

    def withResultsLanguage(self, lang: Languages):
        self.results_lang = lang.getLanguage()
        return self

    def withResultsAtCountry(self, country: Countries):
        self.country = country.getCountry()
        return self

    def withDocumentCountry(self, country: Countries):
        self.document_country = country.getCountry()
        return self

    def withSearchBetweenTwoDates(self, dates: Dates):
        self.search_between_two_dates = dates.getDates()
        return self

    def withSortByUpdateTime(self):
        self.sort_by_update_time = True
        return self

    def withSearchingAtDifferentGooglePages(self, google_pages: GooglePages):
        self.search_at_different_pages = True
        self.search_at = google_pages.getGooglePage()
        return self

    def withSearchStartPositionAt(self, index: int):
        self.start_position = str(index)
        return self

    def withImageParams(self, params: GoogleImages):
        params_dict = params.getImageParams()
        self.image_params = {}
        for key, value in params_dict.items():
            if value:
                self.image_params[key] = value
        return self

    def withPatentParams(self, params: GooglePatents):
        params_dict = params.getPatentModifiers()
        self.patents_params = {}
        for key, value in params_dict.items():
            if value:
                self.patents_params[key] = value
        return self

    def withShopOptions(self, params: GoogleShop):
        params_dict = params.getShopModifiers()
        self.shop_params = {}
        for key, value in params_dict.items():
            if value:
                self.shop_params[key] = value
        return self

    def withInterfaceLanguage(self, language: InterfaceLanguages):
        self.interface_language = language
        return self

    def withBookParams(self, params: GoogleBooks):
        params_dict = params.getBooksModifiers()
        self.book_params = {}
        for key, value in params_dict.items():
            if value:
                self.book_params[key] = value
        return self


class URLBuilder:
    def __init__(self, google_search_params: GoogleSearch):
        self.params = google_search_params

    def __params_validator(self):
        from errors import TimeCombinationNonValid, MixedSearchException

        if self.params.search_between_two_dates and self.params.time_limit:
            raise TimeCombinationNonValid("You cannot search between two dates and a define a time limit")
        if self.params.search_at_different_pages:
            if self.params.search_at == __google_url_modifiers__["with_searching"]["books"]:
                if self.params.image_params or self.params.patents_params or self.params.shop_params:
                    raise MixedSearchException("You cannot combine a Google Books Search with other params")
            elif self.params.search_at == __google_url_modifiers__["with_searching"]["images"]:
                if self.params.shop_params or self.params.patents_params or self.params.book_params:
                    raise MixedSearchException("You cannot combine a Google Images Search with other params")
            elif self.params.search_at == __google_url_modifiers__["with_searching"]["news"]:
                if self.params.shop_params or self.params.patents_params or self.params.book_params or \
                        self.params.image_params:
                    raise MixedSearchException("You cannot combine a Google News Search with other params")
            elif self.params.search_at == __google_url_modifiers__["with_searching"]["patents"]:
                if self.params.shop_params or self.params.image_params or self.params.book_params:
                    raise MixedSearchException("You cannot combine a Google Patents Search with other params")
            elif self.params.search_at == __google_url_modifiers__["with_searching"]["shops"]:
                if self.params.patents_params or self.params.book_params or self.params.image_params:
                    raise MixedSearchException("You cannot combine a Google Shops Search with other params")
            elif self.params.search_at == __google_url_modifiers__["with_searching"]["videos"]:
                if self.params.shop_params or self.params.patents_params or self.params.book_params or \
                        self.params.image_params:
                    raise MixedSearchException("You cannot combine a Google Videos Search with other params")

    def build(self):
        # type: () -> tuple
        from errors import NullQueryError

        self.__params_validator()
        # if not self.params.operation:
        main_query = []
        if self.params.query:
            main_query.append(__google_url_modifiers__["query"].format(self.params.query))
        # elif self.params.define:
        #     main_query.append(__google_url_modifiers__["with_defining"].format(self.params.define))
        else:
            raise NullQueryError("At least \"query\" must be provided")
        if self.params.words_in_title:
            main_query.append(__google_url_modifiers__["with_text_in_title"].format(self.params.words_in_title))
        if self.params.words_in_body:
            main_query.append(__google_url_modifiers__["with_text_in_body"].format(self.params.words_in_body))
        if self.params.words_in_url:
            main_query.append(__google_url_modifiers__["with_text_in_url"].format(self.params.words_in_url))
        if self.params.words_in_anchor:
            main_query.append(
                __google_url_modifiers__["with_text_in_anchor"].format(self.params.words_in_anchor))
        if self.params.between_two_numbers:
            main_query.append(
                __google_url_modifiers__["between_two_numbers"].format(self.params.between_two_numbers[0],
                                                                       self.params.between_two_numbers[1]))
        if self.params.synonym:
            main_query.append(__google_url_modifiers__["with_synonymous_searching"].format(self.params.synonym))
        if self.params.containing_two_words:
            main_query.append(__google_url_modifiers__["with_containing_two_terms"].format(
                self.params.containing_two_words[0], self.params.containing_two_words[1]))

        extra_attributes_query = []
        tbs_attributes = []
        if self.params.words_in_order:
            extra_attributes_query.append(
                __google_url_modifiers__["in_order_displayed"].format(self.params.words_in_order))
        if self.params.or_words:
            extra_attributes_query.append(__google_url_modifiers__["or"].format(self.params.or_words))
        if self.params.words_excluded:
            extra_attributes_query.append(
                __google_url_modifiers__["exclude"].format(self.params.words_excluded))
        if self.params.number_of_results:
            extra_attributes_query.append(
                __google_url_modifiers__["number_of_results"].format(self.params.number_of_results))
        if self.params.filetype:
            extra_attributes_query.append(
                __google_url_modifiers__["with_extension"].format(self.params.filetype))
        if self.params.sitesearch:
            extra_attributes_query.append(__google_url_modifiers__["at_site"].format(self.params.sitesearch))
        if self.params.time_limit:
            extra_attributes_query.append(
                __google_url_modifiers__["with_time_limit"].format(self.params.time_limit))
        if self.params.rights:
            extra_attributes_query.append(__google_url_modifiers__["with_rights"].format(self.params.rights))
        if self.params.safe:
            extra_attributes_query.append(self.params.safe)
        if self.params.related:
            extra_attributes_query.append(
                __google_url_modifiers__["with_related_pages_to_a_doc"].format(self.params.related))
        if self.params.linked:
            extra_attributes_query.append(
                __google_url_modifiers__["with_linking_to_url"].format(self.params.linked))
        if self.params.personalized_search:
            extra_attributes_query.append(self.params.personalized_search)
        if self.params.results_lang:
            extra_attributes_query.append(
                __google_url_modifiers__["with_results_language"].format(self.params.results_lang))
        if self.params.interface_language:
            extra_attributes_query.append(
                __google_url_modifiers__["with_language_interface"].format(self.params.interface_language))
        if self.params.country:
            extra_attributes_query.append(
                __google_url_modifiers__["with_country_results"].format(self.params.country))
        if self.params.document_country:
            extra_attributes_query.append(
                __google_url_modifiers__["with_document_county"].format(self.params.document_country))
        if self.params.search_between_two_dates:
            if self.params.sort_by_update_time:
                tbs_attributes.append(
                    __google_url_modifiers__["with_search_between_two_dates_by_update_time"].format(
                        self.params.search_between_two_dates[0], self.params.search_between_two_dates[1]))
            else:
                tbs_attributes.append(__google_url_modifiers__["with_search_between_two_dates"].format(
                    self.params.search_between_two_dates[0], self.params.search_between_two_dates[1]))
        if self.params.sort_by_update_time and not self.params.search_between_two_dates:
            tbs_attributes.append(__google_url_modifiers__["with_search_by_update_time"])
        if self.params.search_at_different_pages:
            extra_attributes_query.append(
                __google_url_modifiers__["with_searching_at_different_google_pages"].format(
                    self.params.search_at))
        if self.params.start_position:
            extra_attributes_query.append(
                __google_url_modifiers__["with_starting_at_position"].format(self.params.start_position))
        if self.params.image_params:
            for key, value in self.params.image_params.items():
                tbs_attributes.append(value)
        if self.params.patents_params:
            for key, value in self.params.patents_params.items():
                tbs_attributes.append(value)
        if self.params.book_params:
            for key, value in self.params.book_params.items():
                tbs_attributes.append(value)

        final_query = '+'.join(main_query)
        final_attributes = '&'.join(extra_attributes_query)
        if len(tbs_attributes) > 0:
            extra_attributes = __google_url_modifiers__["with_extra_attributes"].format(','.join(tbs_attributes))
        else:
            extra_attributes = None
        if final_attributes and extra_attributes:
            attributes_query = final_query + '&' + final_attributes + '&' + extra_attributes
        elif final_attributes:
            attributes_query = final_query + '&' + final_attributes
        elif extra_attributes:
            attributes_query = final_query + '&' + extra_attributes
        else:
            attributes_query = final_query
        return urllib.parse.quote_plus(__google_base_url__ + attributes_query, safe="/?+&:=_.(|)*-%,")
        # return __google_base_url__ + attributes_query

        # else:
        #     main_query = [__google_url_modifiers__["query"].format(self.params.operation)]
        #     return urllib.parse.quote_plus(__google_base_url__ + main_query[0], safe="/?+&:=_.(|)*-%")
        #     # return __google_base_url__ + main_query[0]
