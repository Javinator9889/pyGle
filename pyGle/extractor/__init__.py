#
#                py-google-search  Copyright (C) 2018  Javinator9889
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
import lxml
import urllib.request
import urllib.parse
import urllib.error
import ujson as json
import random
import time

from bs4 import BeautifulSoup
from concurrent.futures import Future, ThreadPoolExecutor
from multiprocessing import cpu_count

from url import URLBuilder
from url.url_constants import __user_agents__
from errors import GoogleOverloadedException, GoogleBlockingConnectionsError


class BaseExtractor:
    def __init__(self, must_use_session: bool = False, with_history_enabled: bool = False):
        key = random.choice(list(__user_agents__.keys()))
        self.headers = {"User-Agent": __user_agents__[key]}
        self.cpu_count = cpu_count() * 2
        self.session_cookies = {"cookie": None} if must_use_session else {"cookie": "disabled"}
        self.history = [] if with_history_enabled else None

    def extract_url(self, url: URLBuilder) -> Future:
        pass

    def obtain_html_object(self, url: URLBuilder) -> tuple:
        try:
            start_time = time.time()
            built_url = urllib.parse.quote_plus(url.build(), safe="/?+&:=_.(|)*-%")
            request = urllib.request.Request(url=built_url, headers=self.headers)
            if self.session_cookies["cookie"] != "disabled" and self.session_cookies["cookie"] is not None:
                request.add_header("cookie", self.session_cookies["cookie"])
            web_content = urllib.request.urlopen(request)
            if self.session_cookies["cookie"] != "disabled":
                self.session_cookies["cookie"] = web_content.headers.get("Set-Cookie")
            requested_data = web_content.read().decode("utf-8")
            end_time = time.time()
            local_executor = ThreadPoolExecutor(max_workers=self.cpu_count)
            local_executor.submit(web_content.close)
            local_executor.shutdown(wait=False)
            return BeautifulSoup(requested_data, "lxml"), (end_time - start_time)
        except urllib.error.HTTPError as request_error:
            raise GoogleBlockingConnectionsError("It looks like Google is blocking errors.\n\t- Headers: "
                                                 + str(request_error.headers) + "\n\t- Error: "
                                                 + request_error.read().decode("utf-8"))

    def change_header(self):
        new_key = random.choice(list(__user_agents__.keys()))
        self.headers["User-Agent"] = __user_agents__[new_key]

    def getHistory(self) -> list:
        return self.history

    def getOverallTime(self) -> float:
        if self.history:
            amount = 0
            for element in self.history:
                amount += float(element[len(element) - 1]["stats"]["time"].replace(" s", ''))
            return amount / len(self.history)
        else:
            return -1

    def printOverallTime(self):
        overall = self.getOverallTime()
        if overall != -1:
            print("Total requests: " + str(len(self.history)))
            print("Overall time: " + str(overall))
        else:
            print("History is disabled or not petition has been done yet")


class ImageExtractor(BaseExtractor):
    def __extractor(self, url: URLBuilder, start_time: float) -> list:
        html, search_time = super().obtain_html_object(url)
        images = []
        elements_start_time = time.time()
        for a in html.find_all("div", {"class": "rg_meta"}):
            image_properties = json.loads(a.get_text(strip=True))
            link = image_properties.get("ou", None)
            if link:
                image_format = image_properties.get("ity", "unknown")
                image_id = image_properties.get("id", "unknown")
                source = image_properties.get("isu", "unknown")
                width = image_properties.get("oh", "unknown")
                height = image_properties.get("ow", "unknown")
                web_page_name = image_properties.get("pt", "unknown")
                web_page_title = image_properties.get("s", "unknown")
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
                    "webpage_name": web_page_name,
                    "webpage_title": web_page_title
                }
                images.append(found_image_properties)
        elements_end_time = time.time()
        images.append({
            "stats": {
                "images_found": len(images),
                "overall_time": str((time.time() - start_time)) + " s",
                "google_search_time": str(search_time) + " s",
                "parsing_page_time": str((elements_end_time - elements_start_time)) + " s"
            }
        })
        if self.history is not None:
            self.history.append(images)
        super().change_header()
        return images

    def extract_url(self, url: URLBuilder) -> Future:
        start_time = time.time()
        executor = ThreadPoolExecutor(max_workers=self.cpu_count)
        future = executor.submit(self.__extractor, url, start_time)
        executor.shutdown(wait=False)
        return future


class SearchExtractor(BaseExtractor):
    @staticmethod
    def __get_web_page_title_link(web_section) -> tuple:
        try:
            search_title_object = web_section.find_all("h3", {"class": "r"})[0].find_all("a")
            link = search_title_object[0].get("href")
            web_page_title = search_title_object[0].string
        except IndexError:
            link = "unavailable"
            web_page_title = "unavailable"
        return link, web_page_title

    @staticmethod
    def __obtain_detailed_section(web_section) -> BeautifulSoup:
        try:
            return web_section.find_all("div", {"class": "s"})[0]
        except IndexError:
            raise GoogleOverloadedException("It looks like Google is blocking your requests. Try enabling the "
                                            "proxy mode or wait for a few minutes")

    @staticmethod
    def __obtain_web_cache(detailed_section) -> str:
        try:
            web_cache_version = detailed_section.find_all("li",
                                                          {"class": "action-menu-item ab_dropdownitem",
                                                           "role": "menuitem"})[0]
            web_cache_link = web_cache_version.find_all("a", {"class": "fl"})[0].get("href")
        except IndexError:
            web_cache_link = "unavailable"
        return web_cache_link

    @staticmethod
    def __obtain_date(detailed_section) -> str:
        try:
            date = detailed_section.find_all("span", {"class": "f"})[0].string
        except IndexError:
            date = "unavailable"
        return date

    @staticmethod
    def __obtain_related_pages(detailed_section) -> list:
        try:
            related_pages = []
            for related_page in detailed_section.find_all("div", {"class": "VNLkW"}):
                page_info = {}
                related_link = related_page.find_all("a", {"class": "fl"})[0].get("href")
                related_title = related_page.find_all("a", {"class": "fl"})[0].get_text(strip=True)
                related_date = related_page.find_all("div", {"class": "G1Rrjc"})[1].get_text(strip=True)
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
        return related_pages

    @staticmethod
    def __obtain_related_search(origin_html):
        try:
            related_search_result = origin_html.find_all("div", {"class": "card-section"})[0]
            related_search = []
            for other_search in related_search_result.find_all("a"):
                related_search.append(other_search.get_text(strip=True))
        except IndexError:
            related_search = "unavailable"
        return related_search

    @staticmethod
    def __obtain_stats(origin_html):
        try:
            stats = origin_html.find_all("div", {"id": "resultStats"})[0].get_text(strip=True)
        except IndexError:
            stats = "unavailable"
        return stats

    def __extractor(self, url: URLBuilder, start_time: float) -> list:
        html, search_time = super().obtain_html_object(url)
        search_results = []
        elements_start_time = time.time()
        results_areas = html.find_all("div", {"class": "srg"})
        for section in results_areas:
            found_results = section.find_all("div", {"class": "g"})
            for result in found_results:
                link, web_page_title = self.__get_web_page_title_link(result)
                more_info = self.__obtain_detailed_section(result)
                web_cache_link = self.__obtain_web_cache(more_info)
                search_more_data = more_info.find_all("span", {"class": "st"})[0]
                date = self.__obtain_date(search_more_data)
                related_pages = self.__obtain_related_pages(more_info)
                description = search_more_data.get_text(strip=True).replace(date, '', 1)
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
        related_search = self.__obtain_related_search(html)
        stats = self.__obtain_stats(html)
        elements_end_time = time.time()
        search_results.append({"how_many_results": len(search_results),
                               "related_search": related_search,
                               "google_stats": stats,
                               "stats": {
                                   "overall_time": str((time.time() - start_time)) + " s",
                                   "google_search_time": str(search_time) + " s",
                                   "parsing_page_time": str((elements_end_time - elements_start_time)) + " s"
                               }})
        if self.history is not None:
            self.history.append(search_results)
        super().change_header()
        return search_results

    def extract_url(self, url: URLBuilder) -> Future:
        start_time = time.time()
        executor = ThreadPoolExecutor(max_workers=self.cpu_count)
        future = executor.submit(self.__extractor, url, start_time)
        executor.shutdown(wait=False)
        return future


class NewsExtractor(BaseExtractor):
    @staticmethod
    def __obtain_thumbnail(picture_class) -> str:
        try:
            a_section = picture_class.find("a", {"class": "top NQHJEb dfhHve"})
            image_found = a_section.find("img", {"class": "th BbeB2d"}).get("src")
            return image_found if NewsExtractor.__is_valid_url(image_found) else "base64 image - URL not available"
        except AttributeError:
            return "unavailable"

    @staticmethod
    def __is_valid_url(url) -> bool:
        import re

        # From: https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    @staticmethod
    def __get_title_link(html) -> tuple:
        try:
            header = html.find_all("h3", {"class": "r dO0Ag"})[0].find_all("a")[0]
            link = header.get("href")
            title = header.get_text(strip=True)
        except IndexError:
            link = "unavailable"
            title = "unavailable"
        return link, title

    @staticmethod
    def __obtain_publisher_date_extra(main_content) -> tuple:
        publisher = main_content.find("span", {"class": "xQ82C e8fRJf"}).get_text(strip=True)
        if not publisher:
            publisher = "unavailable"
        date = main_content.find("span", {"class": "f nsa fwzPFf"}).get_text(strip=True)
        if not date:
            date = "unavailable"
        extra_data = main_content.find("span", {"class": "HgetDe DwKiF"})
        extra = extra_data.get_text(strip=True) if extra_data else None
        return publisher, date, extra

    @staticmethod
    def __obtain_description(main_content) -> str:
        description = main_content.get_text(strip=True)
        return description if description else "unavailable"

    @staticmethod
    def __obtain_related_articles(section) -> list:
        found_articles = []
        articles = section.find_all("div", class_="card-section")
        for article in articles:
            article_attributes = {}
            try:
                title_data = article.find("a", {"class": "RTNUJf"})
                title = title_data.get_text(strip=True)
                link = title_data.get("href")
                publisher = article.find("span", class_="xQ82C").get_text(strip=True)
                date = article.find("span", class_="fwzPFf").get_text(strip=True)
                extra_data = article.find("span", class_="HgetDe")
                extra = extra_data.get_text(strip=True) if extra_data else None
                article_attributes["title"] = title if title else "unavailable"
                article_attributes["link"] = link if link else "unavailable"
                article_attributes["publisher"] = publisher if publisher else "unavailable"
                article_attributes["date"] = date if date else "unavailable"
                if extra:
                    article_attributes["extra"] = extra
                found_articles.append(article_attributes)
            except AttributeError:
                pass
        return found_articles

    @staticmethod
    def __obtain_stats(origin_html):
        try:
            stats = origin_html.find_all("div", {"id": "resultStats"})[0].get_text(strip=True)
        except IndexError:
            stats = "unavailable"
        return stats

    def __extractor(self, url: URLBuilder, start_time: float) -> list:
        html, search_time = super().obtain_html_object(url)
        news_results = []
        elements_start_time = time.time()
        results_area = html.find_all("div", {"id": "ires"})[0]
        found_results = results_area.find_all("div", {"class": "g"})
        for result in found_results:
            main_content = result.find_all("div", {"class": "gG0TJc"})[0]
            thumbnail = self.__obtain_thumbnail(result.find("div", class_="ts"))
            link, title = self.__get_title_link(main_content)
            publisher, date, extra = self.__obtain_publisher_date_extra(main_content.find("div", {"class": "slp"}))
            description = self.__obtain_description(main_content.find("div", {"class": "st"}))
            related_articles = self.__obtain_related_articles(result)
            result_data = {
                "title": title,
                "link": link,
                "thumbnail": thumbnail,
                "publisher": publisher,
                "date": date,
                "extra": extra,
                "description": description,
                "related_articles": related_articles
            }
            if not extra:
                result_data.pop("extra", None)
            news_results.append(result_data)
        stats = self.__obtain_stats(html)
        elements_end_time = time.time()
        news_results.append({"how_many_results": len(news_results),
                             "google_stats": stats,
                             "stats": {
                                 "overall_time": str((time.time() - start_time)) + " s",
                                 "google_search_time": str(search_time) + " s",
                                 "parsing_page_time": str((elements_end_time - elements_start_time)) + " s"
                             }})
        if self.history is not None:
            self.history.append(news_results)
        super().change_header()
        return news_results

    def extract_url(self, url: URLBuilder) -> Future:
        start_time = time.time()
        executor = ThreadPoolExecutor(max_workers=self.cpu_count)
        future = executor.submit(self.__extractor, url, start_time)
        executor.shutdown(wait=False)
        return future
