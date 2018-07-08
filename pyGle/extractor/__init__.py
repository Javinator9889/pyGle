#
#                py-google-search  Copyright (C) 2018  Javinator9889
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
import lxml
import requests
import urllib.request
import urllib.parse
import urlencode as ude
import ujson as json
import random
import time

from bs4 import BeautifulSoup
from concurrent.futures import Future, ThreadPoolExecutor
from multiprocessing import cpu_count

from url import URLBuilder
from url.url_constants import __user_agents__
from errors import GoogleOverloadedException


class BaseExtractor:
    def __init__(self, must_use_session: bool = False):
        key = random.choice(list(__user_agents__.keys()))
        self.headers = {"User-Agent": __user_agents__[key]}
        self.cpu_count = cpu_count() * 2
        self.session = requests.Session() if must_use_session else None
        # self.http = urllib3.PoolManager()

    def extract_url(self, url: URLBuilder) -> Future:
        pass

    def obtain_html_object(self, url: URLBuilder) -> BeautifulSoup:
        built_url = ude.urlencoder(text=url.build())
        request = urllib.request.Request(url=built_url[0], headers=self.headers)
        # with urllib.request.urlopen(request) as web_content:
        #     requested_data = web_content.read().decode("utf-8")
        web_content = urllib.request.urlopen(request)
        requested_data = web_content.read().decode("utf-8")
        # executor = ThreadPoolExecutor(max_workers=self.cpu_count)
        # executor.submit(web_content.close)
        # executor.shutdown(wait=False)
        # requested_data = self.session.get(built_url, headers=self.headers).content if self.session \
        #     else requests.get(built_url, headers=self.headers).content
        # requested_data = requests.get(built_url, headers=self.headers).content
        return BeautifulSoup(requested_data, "lxml")

    def change_header(self):
        new_key = random.choice(list(__user_agents__.keys()))
        self.headers["User-Agent"] = __user_agents__[new_key]


class ImageExtractor(BaseExtractor):
    def __extractor(self, url: URLBuilder, start_time) -> list:
        html = super().obtain_html_object(url)
        images = []
        for a in html.find_all("div", {"class": "rg_meta"}):
            image_properties = json.loads(a.text)
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
        images.append({"stats": {"time": str((time.time() - start_time)) + " s", "images_found": len(images)}})
        super().change_header()
        return images

    def extract_url(self, url: URLBuilder) -> Future:
        start_time = time.time()
        executor = ThreadPoolExecutor(max_workers=self.cpu_count)
        future = executor.submit(self.__extractor, url, start_time)
        executor.shutdown(wait=False)
        return future


class SearchExtractor(BaseExtractor):
    def __extractor(self, url: URLBuilder, start_time) -> list:
        print("Performing Google request... | " + str(time.time() - start_time) + " s")
        html = super().obtain_html_object(url)
        print("Google request done! | " + str(time.time() - start_time) + " s")
        search_results = []
        print("Finding \"div\" classes... | " + str(time.time() - start_time) + " s")
        results_areas = html.find_all("div", {"class": "srg"})
        print("\"div\" classes found! | " + str(time.time() - start_time) + " s")
        for section in results_areas:
            found_results = section.find_all("div", {"class": "g"})
            for result in found_results:
                try:
                    print("Searching title... | " + str(time.time() - start_time) + " s")
                    search_title_object = result.find_all("h3", {"class": "r"})[0].find_all("a")
                    link = search_title_object[0].get("href")
                    web_page_title = search_title_object[0].string
                    print("Title found! | " + str(time.time() - start_time) + " s")
                except IndexError:
                    link = "unavailable"
                    web_page_title = "unavailable"
                try:
                    print("Finding more info... | " + str(time.time() - start_time) + " s")
                    more_info = result.find_all("div", {"class": "s"})[0]
                    print("More info found! | " + str(time.time() - start_time) + " s")
                except IndexError:
                    raise GoogleOverloadedException("It looks like Google is blocking your requests. Try enabling the "
                                                    "proxy mode or wait for a few minutes")
                try:
                    print("Finding cached version... | " + str(time.time() - start_time) + " s")
                    web_cache_version = more_info.find_all("li",
                                                           {"class": "action-menu-item ab_dropdownitem",
                                                            "role": "menuitem"})[0]
                    web_cache_link = web_cache_version.find_all("a", {"class": "fl"})[0].get("href")
                    print("Cached version found! | " + str(time.time() - start_time) + " s")
                except IndexError:
                    web_cache_link = "unavailable"
                search_more_data = more_info.find_all("span", {"class": "st"})[0]
                try:
                    date = search_more_data.find_all("span", {"class": "f"})[0].string
                except IndexError:
                    date = "unavailable"
                try:
                    related_pages = []
                    for related_page in more_info.find_all("div", {"class": "VNLkW"}):
                        page_info = {}
                        related_link = related_page.find_all("a", {"class": "fl"})[0].get("href")
                        related_title = related_page.find_all("a", {"class": "fl"})[0].text
                        related_date = related_page.find_all("div", {"class": "G1Rrjc"})[1].text
                        if related_link:
                            page_info["link"] = related_link
                        if related_title:
                            page_info["title"] = related_title
                        if related_date:
                            page_info["date"] = related_date
                        if len(page_info) != 0:
                            related_pages.append(page_info)
                    if len(related_pages) == 0:
                        related_pages = None
                except IndexError:
                    related_pages = None
                description = search_more_data.text.replace(date, '', 1)
                current_results = {
                    "link": link,
                    "title": web_page_title,
                    "cached_version": web_cache_link,
                    "date": date.replace(" - ", ''),
                    "description": description
                }
                if related_pages:
                    current_results["related_pages"] = related_pages
                search_results.append(current_results)
        try:
            related_search_result = html.find_all("div", {"class": "card-section"})[0]
            related_search = []
            for other_search in related_search_result.find_all("a"):
                related_search.append(other_search.text)
        except IndexError:
            related_search = "unavailable"
        try:
            stats = html.find_all("div", {"id": "resultStats"})[0].text
        except IndexError:
            stats = "unavailable"
        search_results.append({"how_many_results": len(search_results),
                               "related_search": related_search,
                               "google_stats": stats,
                               "stats": {
                                   "time": str((time.time() - start_time)) + " s"
                               }})
        super().change_header()
        return search_results

    def extract_url(self, url: URLBuilder) -> Future:
        start_time = time.time()
        executor = ThreadPoolExecutor(max_workers=self.cpu_count)
        future = executor.submit(self.__extractor, url, start_time)
        executor.shutdown(wait=False)
        return future
