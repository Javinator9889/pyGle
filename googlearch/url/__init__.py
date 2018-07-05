#
#                py-google-search  Copyright (C) 2018  Javinator9889
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
import requests

from .url_constants import __google_base_url__, __google_url_modifiers__
from values import TimeLimit, Rights, Languages, Countries, Dates, GooglePages


class GoogleSearch:
    def __init__(self, query: str = None):
        self.__query = query
        self.__words_in_order = None
        self.__or_words = None
        self.__words_excluded = None
        self.__number_of_results = None
        self.__filetype = None
        self.__sitesearch = None
        self.__time_limit = None
        self.__rights = None
        self.__words_in_title = None
        self.__words_in_body = None
        self.__words_in_url = None
        self.__words_in_anchor = None
        self.__between_two_numbers = None
        self.__synonym = None
        self.__define = None
        self.__containing_two_words = None
        self.__operation = None
        self.__safe = None
        self.__related = None
        self.__linked = None
        self.__personalized_search = None
        self.__results_lang = None
        self.__country = None
        self.__document_country = None
        self.__search_between_two_dates = None
        self.__sort_by_update_time = None
        self.__search_at_different_pages = None
        self.__search_at = None
        self.__start_position = None

    def withQuery(self, query: str):
        self.__query = query.replace(' ', '+')
        return self

    def withWordsInSpecificOrderSearch(self, words: list):
        self.__words_in_order = '+'.join(words)
        return self

    def withOneOrMoreWordsInResult(self, words: list):
        self.__or_words = '+'.join(words)
        return self

    def withExcludedWords(self, words: list):
        self.__words_excluded = '+'.join(words)
        return self

    def withNumberOfResults(self, results: int = 10):
        self.__number_of_results = str(results)
        return self

    def withFileSearchByFileType(self, filetype: str):
        self.__filetype = filetype.replace(' ', '+')
        return self

    def withSiteSearch(self, site: str):
        self.__sitesearch = site.replace(' ', '+')
        return self

    def withTimeLimit(self, time_limit: TimeLimit):
        self.__time_limit = time_limit.getTimeLimit()
        return self

    def withRights(self, rights: Rights):
        self.__rights = rights.getRights()
        return self

    def withTextInTitle(self, text: str):
        self.__words_in_title = text.replace(' ', '+')
        return self

    def withTextInBody(self, text: str):
        self.__words_in_body = text.replace(' ', '+')
        return self

    def withTextInUrl(self, text: str):
        self.__words_in_url = text.replace(' ', '+')
        return self

    def withTextInAnchor(self, text: str):
        self.__words_in_anchor = text.replace(' ', '+')
        return self

    def withResultBetweenTwoNumbers(self, first_number: float, second_number: float):
        self.__between_two_numbers = [str(first_number), str(second_number)]
        return self

    def withRelatedPagesToADocument(self, document_url: str):
        self.__related = document_url.replace(' ', '+')
        return self

    def withSynonymousSearchingToAWord(self, word: str):
        self.__synonym = word.replace(' ', '+')
        return self

    def withDefiningTerm(self, term: str):
        self.__define = term.replace(' ', '+')
        return self

    def withContainingTwoTerms(self, first_term: str, second_term: str):
        self.__containing_two_words = [first_term.replace(' ', '+'), second_term.replace(' ', '+')]
        return self

    def withArithmeticOperation(self, operation: str):
        self.__operation = operation.replace(' ', '').replace('+', "%2B")
        return self

    def withSafeModeActivated(self):
        self.__safe = __google_url_modifiers__["with_safe_active"]
        return self

    def withSafeModeDeactivated(self):
        self.__safe = __google_url_modifiers__["with_safe_deactivated"]
        return self

    def withLinkingToUrl(self, url: str):
        self.__linked = url.replace(' ', '+')
        return self

    def withPersonalizedSearch(self):
        self.__personalized_search = __google_url_modifiers__["with_personalized_search"]
        return self

    def withNoPersonalizedSearch(self):
        self.__personalized_search = __google_url_modifiers__["with_no_personalized_search"]
        return self

    def withResultsLanguage(self, lang: Languages):
        self.__results_lang = lang.getLanguage()
        return self

    def withResultsAtCountry(self, country: Countries):
        self.__country = country.getCountry()
        return self

    def withDocumentCountry(self, country: Countries):
        self.__document_country = country.getCountry()
        return self

    def withSearchBetweenTwoDates(self, dates: Dates):
        self.__search_between_two_dates = dates.getDates()
        return self

    def withSortByUpdateTime(self):
        self.__sort_by_update_time = True
        return self

    def withSearchingAtDifferentGooglePages(self, google_pages: GooglePages):
        self.__search_at_different_pages = True
        self.__search_at = google_pages.getGooglePage()
        return self

    def withSearchStartPositionAt(self, index: int):
        self.__start_position = str(index)
        return self


class URLBuilder:
    def __init__(self, google_search_params: GoogleSearch):
        self.__params = google_search_params

    def build(self):
        # type: () -> str
        from errors import InvalidCombinationException, NullQueryError

        if self.__params.__define and self.__params.__query:
            raise InvalidCombinationException("You cannot search and define a word at the same time")
        if (self.__params.__define and self.__params.__operation) or \
                (self.__params.__query and self.__params.__operation):
            raise InvalidCombinationException("You cannot search or define a word and perform an operation")
        if self.__params.__search_between_two_dates and self.__params.__time_limit:
            raise InvalidCombinationException("You cannot search between two dates and with a time-limit at the "
                                              "same time")
        if not self.__params.__operation:
            main_query = []
            if self.__params.__query:
                main_query.append(__google_url_modifiers__["query"].format(self.__params.__query))
            elif self.__params.__define:
                main_query.append(__google_url_modifiers__["with_defining"].format(self.__params.__define))
            else:
                raise NullQueryError("At least \"query\" or \"define\" must be provided")
            if self.__params.__words_in_title:
                main_query.append(__google_url_modifiers__["with_text_in_title"].format(self.__params.__words_in_title))
            if self.__params.__words_in_body:
                main_query.append(__google_url_modifiers__["with_text_in_body"].format(self.__params.__words_in_body))
            if self.__params.__words_in_url:
                main_query.append(__google_url_modifiers__["with_text_in_url"].format(self.__params.__words_in_url))
            if self.__params.__words_in_anchor:
                main_query.append(
                    __google_url_modifiers__["with_text_in_anchor"].format(self.__params.__words_in_anchor))
            if self.__params.__between_two_numbers:
                main_query.append(
                    __google_url_modifiers__["between_two_numbers"].format(self.__params.__between_two_numbers[0],
                                                                           self.__params.__between_two_numbers[1]))
            if self.__params.__synonym:
                main_query.append(__google_url_modifiers__["with_synonymous_searching"].format(self.__params.__synonym))
            if self.__params.__containing_two_words:
                main_query.append(__google_url_modifiers__["with_containing_two_terms"].format(
                    self.__params.__containing_two_words[0], self.__params.__containing_two_words[1]))

            extra_attributes_query = []
            if self.__params.__words_in_order:
                extra_attributes_query.append(
                    __google_url_modifiers__["in_order_displayed"].format(self.__params.__words_in_order))
            if self.__params.__or_words:
                extra_attributes_query.append(__google_url_modifiers__["or"].format(self.__params.__or_words))
            if self.__params.__words_excluded:
                extra_attributes_query.append(
                    __google_url_modifiers__["exclude"].format(self.__params.__words_excluded))
            if self.__params.__number_of_results:
                extra_attributes_query.append(
                    __google_url_modifiers__["number_of_results"].format(self.__params.__number_of_results))
            if self.__params.__filetype:
                extra_attributes_query.append(
                    __google_url_modifiers__["with_extension"].format(self.__params.__filetype))
            if self.__params.__sitesearch:
                extra_attributes_query.append(__google_url_modifiers__["at_site"].format(self.__params.__sitesearch))
            if self.__params.__time_limit:
                extra_attributes_query.append(
                    __google_url_modifiers__["with_time_limit"].format(self.__params.__time_limit))
            if self.__params.__rights:
                extra_attributes_query.append(__google_url_modifiers__["with_rights"].format(self.__params.__rights))
            if self.__params.__safe:
                extra_attributes_query.append(self.__params.__safe)
            if self.__params.__related:
                extra_attributes_query.append(
                    __google_url_modifiers__["with_related_pages_to_a_doc"].format(self.__params.__related))
            if self.__params.__linked:
                extra_attributes_query.append(
                    __google_url_modifiers__["with_linking_to_url"].format(self.__params.__linked))
            if self.__params.__personalized_search:
                extra_attributes_query.append(self.__params.__personalized_search)
            if self.__params.__results_lang:
                extra_attributes_query.append(
                    __google_url_modifiers__["with_results_language"].format(self.__params.__results_lang))
            if self.__params.__country:
                extra_attributes_query.append(
                    __google_url_modifiers__["with_country_results"].format(self.__params.__country))
            if self.__params.__document_country:
                extra_attributes_query.append(
                    __google_url_modifiers__["with_document_county"].format(self.__params.__document_country))
            if self.__params.__search_between_two_dates:
                if self.__params.__sort_by_update_time:
                    extra_attributes_query.append(
                        __google_url_modifiers__["with_search_between_two_dates_by_update_time"].format(
                            self.__params.__search_between_two_dates))
                else:
                    extra_attributes_query.append(__google_url_modifiers__["with_search_between_two_dates"].format(
                        self.__params.__search_between_two_dates))
            if self.__params.__sort_by_update_time and not self.__params.__search_between_two_dates:
                extra_attributes_query.append(__google_url_modifiers__["with_search_by_update_time"])
            if self.__params.__search_at_different_pages:
                extra_attributes_query.append(
                    __google_url_modifiers__["with_searching_at_different_google_pages"].format(
                        self.__params.__search_at))
            if self.__params.__start_position:
                extra_attributes_query.append(
                    __google_url_modifiers__["with_starting_at_position"].format(self.__params.__start_position))

            final_query = '+'.join(main_query)
            final_attributes = '&'.join(extra_attributes_query)
            return (__google_base_url__ + final_query + '&' + final_attributes) if final_attributes else (
                        __google_base_url__ + final_query)
        else:
            main_query = [__google_url_modifiers__["query"].format(self.__params.__operation)]
            return __google_base_url__ + main_query[0]
