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

from pyGle.url import URLBuilder
from pyGle.url.url_constants import __user_agents__
from pyGle.errors import GoogleOverloadedException, GoogleBlockingConnectionsError


class BaseExtractor:
    def __init__(self, must_use_session: bool = False, with_history_enabled: bool = False):
        key = random.choice(list(__user_agents__.keys()))
        self.headers = {"User-Agent": __user_agents__[key]}
        self.cpu_count = cpu_count() * 2
        self.session_cookies = {"cookie": None} if must_use_session else {"cookie": "disabled"}
        self.history = [] if with_history_enabled else None
        self.url = None

    def extract_url(self, url: URLBuilder) -> Future:
        pass

    def obtain_html_object(self, url: URLBuilder) -> tuple:
        try:
            start_time = time.time()
            built_url = url.build()
            self.url = built_url
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

    def getOverallTime(self) -> tuple:
        if self.history:
            time_amount = 0
            google_search_amount = 0
            parsing_elements_amount = 0
            length = len(self.history)
            for element in self.history:
                element_length = len(element) - 1
                time_amount += float(element[element_length]["stats"]["overall_time"].replace(" s", ''))
                google_search_amount += float(element[element_length]["stats"]["google_search_time"].replace(" s", ''))
                parsing_elements_amount += float(
                    element[element_length]["stats"]["parsing_page_time"].replace(" s", ''))
            return (time_amount / length), (google_search_amount / length), (parsing_elements_amount / length)
        else:
            return -1, -1, -1

    def printOverallTime(self):
        overall_time, google_search, parsing_elements = self.getOverallTime()
        if overall_time != -1:
            print("Total requests: " + str(len(self.history)))
            print("Overall time: " + str(overall_time) + " s")
            print("Google search overall time: " + str(google_search) + " s")
            print("Parsing elements overall time: " + str(parsing_elements) + " s")
        else:
            print("History is disabled or not petition has been done yet")

    @staticmethod
    def is_valid_url(url) -> bool:
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
    def cleanupString(text: str) -> str:
        import re

        return re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇñÑÄËÏÖÜäëïöü: \-.()/]', '', text)


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
            },
            "url": self.url
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
            return None
            # raise GoogleOverloadedException("It looks like Google is blocking your requests. Try enabling the "
            #                                 "proxy mode or wait for a few minutes")

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

    @staticmethod
    def __find_pages_in_selection(web_section) -> list:
        try:
            in_search_page = web_section.find_all("table", {"class": "nrgt"})[0]
            pages = in_search_page.find_all("div", {"class": "sld vsc"})
            results = []
            for page in pages:
                title_section = page.find("h3", {"class": "r"}).find("a", {"class": "l"})
                try:
                    title = title_section.get_text(strip=True).strip()
                    link = title_section.get("href").strip()
                    description = page.find("div", {"class": "s"}).find("div",
                                                                        {"class": "st"}).get_text(strip=True).strip()
                    results.append({
                        "title": title,
                        "link": link,
                        "description": description
                    })
                except AttributeError:
                    pass
            return results
        except IndexError:
            return []

    def __extractor(self, url: URLBuilder, start_time: float) -> list:
        html, search_time = super().obtain_html_object(url)
        search_results = []
        elements_start_time = time.time()
        results_areas = html.find_all("div", {"class": "bkWMgd"})
        for section in results_areas:
            found_results = section.find_all("div", {"class": "g"})
            for result in found_results:
                link, web_page_title = self.__get_web_page_title_link(result)
                more_info = self.__obtain_detailed_section(result)
                if more_info is None:
                    break
                web_cache_link = self.__obtain_web_cache(more_info)
                inside_pages = self.__find_pages_in_selection(result)
                try:
                    search_more_data = more_info.find_all("span", {"class": "st"})[0]
                    date = self.__obtain_date(search_more_data)
                    related_pages = self.__obtain_related_pages(more_info)
                    description = search_more_data.get_text(strip=True).replace(date, '', 1)
                except IndexError:
                    date = "unavailable"
                    related_pages = "unavailable"
                    description = "unavailable"
                current_results = {
                    "link": link,
                    "title": web_page_title,
                    "cached_version": web_cache_link,
                    "date": date.replace(" - ", ''),
                    "description": self.cleanupString(description)
                }
                if related_pages:
                    current_results["related_pages"] = related_pages
                if len(inside_pages) != 0:
                    current_results["inside_pages"] = inside_pages
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
                               },
                               "url": self.url})
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
            return image_found if NewsExtractor.is_valid_url(image_found) else "base64 image - URL not available"
        except AttributeError:
            return "unavailable"

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

    def __obtain_description(self, main_content) -> str:
        description = main_content.get_text(strip=True)
        return self.cleanupString(description) if description else "unavailable"

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
                             },
                             "url": self.url})
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


class VideoExtractor(BaseExtractor):
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
    def __obtain_thumbnail(web_section) -> str:
        try:
            thumbnail_section = web_section.find("div", class_="N3nEGc").find("a").find("g-img").find("img")
            return thumbnail_section.get("src")
        except AttributeError:
            return "unavailable"

    @staticmethod
    def __obtain_duration(web_section) -> str:
        try:
            thumbnail_section = web_section.find("div", class_="N3nEGc").find("a").find("span", {"class": "vdur"})
            return thumbnail_section.get_text(strip=True).replace("▶", '').strip()
        except AttributeError:
            return "unavailable"

    @staticmethod
    def __obtain_location(web_section) -> str:
        try:
            data_section = web_section.find("div", class_="hJND5c").find("cite")
            return data_section.get_text(strip=True)
        except AttributeError:
            return "unavailable"

    @staticmethod
    def __obtain_date(web_section) -> str:
        try:
            date_section = web_section.find("div", class_="slp f")
            return date_section.get_text(strip=True)
        except AttributeError:
            return "unavailable"

    def __obtain_description(self, web_section) -> str:
        try:
            desc_section = web_section.find("span", {"class": "st"})
            return self.cleanupString(desc_section.get_text(strip=True))
        except AttributeError:
            return "unavailable"

    @staticmethod
    def __obtain_stats(origin_html):
        try:
            stats = origin_html.find_all("div", {"id": "resultStats"})[0].get_text(strip=True)
        except IndexError:
            stats = "unavailable"
        return stats

    def __extractor(self, url: URLBuilder, start_time: float) -> list:
        html, search_time = super().obtain_html_object(url)
        vid_results = []
        elements_start_time = time.time()
        results_areas = html.find_all("div", {"class": "srg"})
        for section in results_areas:
            found_results = section.find_all("div", {"class": "g"})
            for result in found_results:
                link, title = self.__get_web_page_title_link(result)
                more_info = self.__obtain_detailed_section(result)
                thumbnail = self.__obtain_thumbnail(more_info)
                duration = self.__obtain_duration(more_info)
                date = self.__obtain_date(more_info)
                description = self.__obtain_description(more_info)
                vid_results.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "date": date,
                    "duration": duration,
                    "thumbnail": thumbnail
                })
        stats = self.__obtain_stats(html)
        elements_end_time = time.time()
        vid_results.append({"how_many_results": len(vid_results),
                            "google_stats": stats,
                            "stats": {
                                "overall_time": str((time.time() - start_time)) + " s",
                                "google_search_time": str(search_time) + " s",
                                "parsing_page_time": str((elements_end_time - elements_start_time)) + " s"
                            },
                            "url": self.url})
        if self.history is not None:
            self.history.append(vid_results)
        super().change_header()
        return vid_results

    def extract_url(self, url: URLBuilder) -> Future:
        start_time = time.time()
        executor = ThreadPoolExecutor(max_workers=self.cpu_count)
        future = executor.submit(self.__extractor, url, start_time)
        executor.shutdown(wait=False)
        return future


class PatentExtractor(BaseExtractor):
    @staticmethod
    def __get_title_link(current_value) -> tuple:
        try:
            section = current_value.find("h3", {"class": "r"}).find("a")
            link = section.get("href")
            title = section.get_text(strip=True).strip()
        except AttributeError:
            link = "unavailable"
            title = "unavailable"
        return title, link

    @staticmethod
    def __obtain_website(details_section) -> str:
        try:
            section = details_section.find_all("cite")[0]
            cite = section.get_text(strip=True).strip()
        except IndexError:
            cite = "unavailable"
        return cite

    def __obtain_description(self, details_section) -> str:
        try:
            section = details_section.find("span", {"class": "st"})
            description = section.get_text(strip=True).strip()
        except AttributeError:
            description = "unavailable"
        return self.cleanupString(description)

    def __obtain_patent_image(self, details_section) -> str:
        try:
            section = details_section.find("img", {"class": "rISBZc M4dUYb"})
            image_link = section.get("src")
            return image_link if self.is_valid_url(image_link) else "base64 image - URL not available"
        except AttributeError:
            return "unavailable"

    def __get_patent_extras(self, details_section) -> tuple:
        import re
        try:
            section = details_section.find("div", {"class": "slp f"})
            first_parts = section.get_text(strip=True).strip()
            parts = re.split("\s-\s", first_parts)
            for i in range(len(parts)):
                parts[i] = self.cleanupString(parts[i])
            return parts[0][:-1], parts[1][1:][:-1], parts[2][1:][:-1], parts[3][1:], parts[4][1:]
        except (AttributeError, IndexError):
            return "unavailable", "unavailable", "unavailable", "unavailable", "unavailable"

    @staticmethod
    def __get_patent_description_related_forum(details_section) -> tuple:
        try:
            section = details_section.find("div", {"class": "osl"})
            parts = section.find_all("a")
            return parts[0].get("href"), parts[1].get("href"), parts[2].get("href")
        except (AttributeError, IndexError):
            return "unavailable", "unavailable", "unavailable"

    @staticmethod
    def __obtain_stats(origin_html):
        try:
            stats = origin_html.find_all("div", {"id": "resultStats"})[0].get_text(strip=True)
        except IndexError:
            stats = "unavailable"
        return stats

    def __extractor(self, url: URLBuilder, start_time: float) -> list:
        html, search_time = super().obtain_html_object(url)
        patents_results = []
        elements_start_time = time.time()
        results_areas = html.find_all("div", {"id": "ires"})
        for section in results_areas:
            found_results = section.find_all("div", {"class": "g"})
            for result in found_results:
                current_value = result.find("div", {"class": "rc"})
                title, link = self.__get_title_link(current_value)
                details_section = current_value.find("div", {"class": "s"})
                cite = self.__obtain_website(details_section)
                description = self.__obtain_description(details_section)
                patent_image = self.__obtain_patent_image(details_section)
                status, presentation_date, publication_date, inventor, assignee = \
                    self.__get_patent_extras(details_section)
                general_description, related_patents, forum = \
                    self.__get_patent_description_related_forum(details_section)
                patents_results.append({
                    "title": title,
                    "link": link,
                    "cite": cite,
                    "description": description,
                    "image": patent_image,
                    "status": status,
                    "presentation_date": presentation_date,
                    "publication_date": publication_date,
                    "inventor": inventor,
                    "assignee": assignee,
                    "general_description": general_description,
                    "related_patents": related_patents,
                    "forum": forum
                })
        stats = self.__obtain_stats(html)
        elements_end_time = time.time()
        patents_results.append({"how_many_results": len(patents_results),
                                "google_stats": stats,
                                "stats": {
                                    "overall_time": str((time.time() - start_time)) + " s",
                                    "google_search_time": str(search_time) + " s",
                                    "parsing_page_time": str((elements_end_time - elements_start_time)) + " s"
                                },
                                "url": self.url})
        if self.history is not None:
            self.history.append(patents_results)
        super().change_header()
        return patents_results

    def extract_url(self, url: URLBuilder) -> Future:
        start_time = time.time()
        executor = ThreadPoolExecutor(max_workers=self.cpu_count)
        future = executor.submit(self.__extractor, url, start_time)
        executor.shutdown(wait=False)
        return future


class ShopExtractor(BaseExtractor):
    @staticmethod
    def __find_thumbnail(result) -> str:
        img = result.find("div", {"class": "JRlvE XNeeld"}).find("img")
        return img.get("src")

    @staticmethod
    def __find_link_title(extra_data) -> tuple:
        try:
            section = extra_data.find("div", {"class": "eIuuYe"}).find("a")
            link = "https://google.com" + section.get("href")
            title = section.get_text(strip=True).strip()
        except AttributeError:
            link = "unavailable"
            title = "unavailable"
        return link, title

    @staticmethod
    def __find_price(extra_data) -> str:
        try:
            section = extra_data.find("div", {"class": "mQ35Be"}).find("span", {"class": "O8U6h"})
            return section.get_text(strip=True).strip().replace(u"\xa0", " ")
        except AttributeError:
            return "unavailable"

    @staticmethod
    def __find_description(extra_data) -> str:
        try:
            section = extra_data.find_all("div", {"class": "na4ICd"})
            description = None
            for result in section:
                if description:
                    description = description + "\n" + result.get_text(strip=True).strip()
                else:
                    description = result.get_text(strip=True).strip()
            return description.replace(u"\xa0", " ")
        except AttributeError:
            return "unavailable"

    @staticmethod
    def __find_reviews_score(extra_data) -> str:
        try:
            section = extra_data.find("div", {"class": "vq3ore"})
            return section.get("aria-label").replace(u"\xa0", " ")
        except AttributeError:
            return "unavailable"

    def __extractor(self, url: URLBuilder, start_time: float) -> list:
        html, search_time = super().obtain_html_object(url)
        shop_results = []
        elements_start_time = time.time()
        results_areas = html.find_all("div", {"id": "ires"})
        for section in results_areas:
            found_results = section.find_all("div", {"class": "sh-dlr__list-result"})
            for result in found_results:
                thumbnail = self.__find_thumbnail(result)
                extra_data = result.find("div", {"class": "ZGFjDb"})
                link, title = self.__find_link_title(extra_data)
                price = self.__find_price(extra_data)
                score = self.__find_reviews_score(extra_data)
                description = self.__find_description(extra_data)
                shop_results.append({
                    "title": title,
                    "link": link,
                    "thumbnail": thumbnail,
                    "price": price,
                    "score": score,
                    "description": description
                })
        elements_end_time = time.time()
        shop_results.append({"how_many_results": len(shop_results),
                             "stats": {
                                 "overall_time": str((time.time() - start_time)) + " s",
                                 "google_search_time": str(search_time) + " s",
                                 "parsing_page_time": str((elements_end_time - elements_start_time)) + " s"
                             },
                             "url": self.url})
        if self.history is not None:
            self.history.append(shop_results)
        super().change_header()
        return shop_results

    def extract_url(self, url: URLBuilder) -> Future:
        start_time = time.time()
        executor = ThreadPoolExecutor(max_workers=self.cpu_count)
        future = executor.submit(self.__extractor, url, start_time)
        executor.shutdown(wait=False)
        return future


class BookExtractor(BaseExtractor):
    @staticmethod
    def __get_book_title_link(web_section) -> tuple:
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
    def __obtain_thumbnail(web_section) -> str:
        try:
            thumbnail_section = web_section.find("div", class_="N3nEGc").find("a").find("g-img").find("img")
            return thumbnail_section.get("src")
        except AttributeError:
            return "unavailable"

    @staticmethod
    def __obtain_google_books_url(detailed_section) -> str:
        try:
            url_section = detailed_section.find("div", {"class": "f hJND5c TbwUpd"}).find("cite", {"class": "iUh30"})
            return url_section.get_text(strip=True).strip()
        except AttributeError:
            return "unavailable"

    def __get_books_extras(self, details_section) -> tuple:
        try:
            section = details_section.find("div", {"class": "slp f"})
            parts = section.get_text(strip=True).strip().split("-")
            for i in range(len(parts)):
                parts[i] = self.cleanupString(parts[i])
            first_part = parts[0]
            second_part = parts[1][1:][:-1]
            try:
                int(second_part)
                return first_part, second_part
            except ValueError:
                try:
                    second_part = "unavailable"
                    int(first_part)
                    return second_part, first_part
                except ValueError:
                    return "unavailable", "unavailable"
            # return parts[0][:-1], parts[1][1:][:-1] if parts[1][1:][:-1] is int else ("unavailable", "unavailable")
        except (AttributeError, IndexError):
            return "unavailable", "unavailable"

    @staticmethod
    def __get_book_description(details_section) -> str:
        try:
            section = details_section.find("span", {"class": "st"})
            return section.get_text(strip=True).strip().replace(u"\xa0", " ")
        except AttributeError:
            return "unavailable"

    @staticmethod
    def __obtain_stats(origin_html):
        try:
            stats = origin_html.find_all("div", {"id": "resultStats"})[0].get_text(strip=True)
        except IndexError:
            stats = "unavailable"
        return stats

    def __extractor(self, url: URLBuilder, start_time: float) -> list:
        html, search_time = super().obtain_html_object(url)
        book_results = []
        elements_start_time = time.time()
        results_areas = html.find_all("div", {"class": "srg"})
        for section in results_areas:
            found_results = section.find_all("div", {"class": "g"})
            for result in found_results:
                link, title = self.__get_book_title_link(result)
                more_info = self.__obtain_detailed_section(result)
                thumbnail = self.__obtain_thumbnail(more_info)
                description = self.__get_book_description(more_info)
                author, age = self.__get_books_extras(more_info)
                book_url = self.__obtain_google_books_url(more_info)
                book_results.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "book_url": book_url,
                    "thumbnail": thumbnail,
                    "publisher": {
                        "age": age,
                        "author": author
                    }
                })
        stats = self.__obtain_stats(html)
        elements_end_time = time.time()
        book_results.append({"how_many_results": len(book_results),
                             "google_stats": stats,
                             "stats": {
                                 "overall_time": str((time.time() - start_time)) + " s",
                                 "google_search_time": str(search_time) + " s",
                                 "parsing_page_time": str((elements_end_time - elements_start_time)) + " s"
                             },
                             "url": self.url})
        if self.history is not None:
            self.history.append(book_results)
        super().change_header()
        return book_results

    def extract_url(self, url: URLBuilder) -> Future:
        start_time = time.time()
        executor = ThreadPoolExecutor(max_workers=self.cpu_count)
        future = executor.submit(self.__extractor, url, start_time)
        executor.shutdown(wait=False)
        return future
