#
#                py-google-search  Copyright (C) 2018  Javinator9889
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
import lxml
import requests
import ujson as json

from bs4 import BeautifulSoup, ResultSet
from pprint import pprint

from url import URLBuilder
from errors import GoogleOverloadedException


class BaseExtractor:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/43.0.2357.134 Safari/537.36"
        }

    def extract_url(self, url: URLBuilder) -> list:
        pass

    def obtain_html_object(self, url: URLBuilder) -> BeautifulSoup:
        built_url = url.build()
        requested_data = requests.get(built_url, headers=self.headers).content
        return BeautifulSoup(requested_data, "lxml")


class ImageExtractor(BaseExtractor):
    def extract_url(self, url: URLBuilder) -> list:
        html = super().obtain_html_object(url)
        images = []
        for a in html.find_all("div", {"class": "rg_meta"}):
            image_properties: dict = json.loads(a.text)
            link = image_properties.get("ou", None)
            if link:
                image_format = image_properties.get("ity", "unknown")
                image_id = image_properties.get("id", "unknown")
                source = image_properties.get("isu", "unknown")
                width = image_properties.get("oh", "unknown")
                height = image_properties.get("ow", "unknown")
                webpage_name = image_properties.get("pt", "unknown")
                webpage_title = image_properties.get("s", "unknown")
                image_posted_on = image_properties.get("ru", "unknown")
                website_name = image_properties.get("st", "unknown")

                found_image_properties = {
                    "url": link,
                    "format": image_format,
                    "id": image_id,
                    "source": source,
                    "width": width,
                    "height": height,
                    "posted_on": image_posted_on,
                    "website_name": website_name,
                    "webpage_name": webpage_name,
                    "webpage_title": webpage_title
                }
                images.append(found_image_properties)
        return images


class SearchExtractor(BaseExtractor):
    def extract_url(self, url: URLBuilder) -> list:
        global web_cache_link
        html = super().obtain_html_object(url)
        search_results = []
        found_results: ResultSet = html.find_all("div", {"class": "g"})
        for result in found_results:
            try:
                search_title_object = result.find_all("h3", {"class": "r"})[0].find_all("a")
                link = search_title_object[0].get("href")
                web_page_title = search_title_object[0].string
            except IndexError:
                link = "unavailable"
                web_page_title = "unavailable"
            try:
                more_info = result.find_all("div", {"class": "s"})[0]
            except IndexError:
                raise GoogleOverloadedException("It looks like Google is blocking your requests. Try enabling the "
                                                "proxy mode or wait for a few minutes")
            try:
                web_cache_version = more_info.find_all("li",
                                                       {"class": "action-menu-item ab_dropdownitem",
                                                        "role": "menuitem"})[0]
                web_cache_link = web_cache_version.find_all("a", {"class": "fl"})[0].get("href")
            except IndexError:
                web_cache_link = "unavailable"
            search_more_data = more_info.find_all("span", {"class": "st"})[0]
            try:
                date = search_more_data.find_all("span", {"class": "f"})[0].string
            except IndexError:
                date = "unavailable"
            description = search_more_data.text.replace(date, '', 1)
            search_results.append({
                "link": link,
                "title": web_page_title,
                "cached_version": web_cache_link,
                "date": date.replace(" - ", ''),
                "description": description
            })
        try:
            related_search_result = html.find_all("div", {"class": "card-section"})[0]
            related_search = []
            for other_search in related_search_result.find_all("a"):
                related_search.append(other_search.text)
        except IndexError:
            related_search = "unavailable"
        search_results.append({"how_many_results": len(search_results),
                               "related_search": related_search})
        return search_results
        # '''pprint(html.find_all("div", {"class": "g"}))
        # search_results = []
        # for results in html.find_all("div", {"class": "g"}):
        #     pprint(results)
        #     for result_title in results.find_all("h3", {"class": "r"}):
        #         link = result_title.a.get("href")
        #         title = result_title.a.string
        #     for result_data in results.find_all("div", {"class": "s"}):
        #         web_cache_obj = result_data.find_all("li",
        #                                              {"class": "action-menu-item ab_dropdownitem", "role": "menuitem"})
        #         web_cache_url = web_cache_obj.find_all("a").get("href")
        #         responses = result_data.find_all("div", {"class": "slp f"}).string
        #         description_obj = result_data.find_all("span", {"class": "st"})
        #         date = description_obj.find_all("span", {"class": "f"}).string
        #         description = description_obj.string
        #         other_results_found = result_data.find_all("div", {"class": "P1usbc"})
        #         other_results = []
        #         for related_search_pages in other_results_found.find_all("a", {"class": "fl"}):
        #             other_results.append({
        #                 "link": related_search_pages.get("href"),
        #                 "name": related_search_pages.string
        #             })
        #     search_results.append({
        #         "link": link,
        #         "title": title,
        #         "cached_web_page": web_cache_url,
        #         "responses": responses,
        #         "date": date,
        #         "description": description,
        #         "other_results": other_results
        #     })
        # return search_results

        # import re
        #
        # html = super().obtain_html_object(url)
        # # available_links = html.find_all("a")
        # search_results = []
        #
        # for link in html.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        #     search_results.append(re.split(":(?=http)", link["href"].replace("/url?q=", "")))
        #
        # return search_results
