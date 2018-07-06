#
#                py-google-search  Copyright (C) 2018  Javinator9889
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
import lxml
import requests
import ujson as json

from bs4 import BeautifulSoup

from url import URLBuilder


class BaseExtractor:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/43.0.2357.134 Safari/537.36"
        }

    def extract_url(self, url: URLBuilder) -> list:
        pass


class ImageExtractor(BaseExtractor):
    def extract_url(self, url: URLBuilder) -> list:
        global image_format, image_id, image_posted_on, source, width, height, webpage_title, webpage_name, website_name
        built_url = url.build()
        requested_data = requests.get(built_url, headers=self.headers).content
        html = BeautifulSoup(requested_data, "lxml")
        images = []
        for a in html.find_all("div", {"class": "rg_meta"}):
            try:
                link = json.loads(a.text)["ou"]
            except ValueError:
                link = None
            finally:
                if link:
                    try:
                        image_format = json.loads(a.text)["ity"]
                    except ValueError:
                        image_format = "unknown"
                    finally:
                        try:
                            image_id = json.loads(a.text)["id"]
                        except ValueError:
                            image_id = "unknown"
                        finally:
                            try:
                                source = json.loads(a.text)["isu"]
                            except ValueError:
                                source = "unknown"
                            finally:
                                try:
                                    width = json.loads(a.text)["oh"]
                                except ValueError:
                                    width = "unknown"
                                finally:
                                    try:
                                        height = json.loads(a.text)["ow"]
                                    except ValueError:
                                        height = "unknown"
                                    finally:
                                        try:
                                            webpage_name = json.loads(a.text)["pt"]
                                        except ValueError:
                                            webpage_name = "unknown"
                                        finally:
                                            try:
                                                image_posted_on = json.loads(a.text)["ru"]
                                            except ValueError:
                                                image_posted_on = "unknown"
                                            finally:
                                                try:
                                                    webpage_title = json.loads(a.text)["s"]
                                                except ValueError:
                                                    webpage_title = "unknown"
                                                finally:
                                                    try:
                                                        website_name = json.loads(a.text)["st"]
                                                    except (ValueError, KeyError):
                                                        website_name = "unknown"
                                                    finally:
                                                        images.append({
                                                            "img_url": link,
                                                            "img_format": image_format,
                                                            "img_id": image_id,
                                                            "source": source,
                                                            "width": width,
                                                            "height": height,
                                                            "webpage_name": webpage_name,
                                                            "posted_on": image_posted_on,
                                                            "webpage_title": webpage_title,
                                                            "website_name": website_name
                                                        })
            # if link:
            #     if not image_format or image_format == '':
            #         image_format = "unknown"
            #     images.append({"img_url": link, "img_format": image_format})
        return images
