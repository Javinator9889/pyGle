#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#


def torify():
    import socks
    import socket

    socks.set_default_proxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
    socket.socket = socks.socksocket


def main():
    # global OfficePatents
    import requests as rq
    import ujson as json

    from bs4 import BeautifulSoup
    import pprint
    import time

    from url import GoogleSearch, URLBuilder
    from values.OptionsForPatents import OfficePatents, PatentStatus, AvailablePatentTypes
    from extractor import ImageExtractor, SearchExtractor, NewsExtractor, VideoExtractor, PatentExtractor, ShopExtractor, BookExtractor
    from values import TimeLimit, GooglePatents, AvailableLanguages, GoogleImages, GooglePages, Countries, Languages, \
        AvailableCountries, GoogleShop, InterfaceLanguages, GoogleBooks

    pp = pprint.PrettyPrinter(indent=4)
    country = Countries()
    # country.setCountry("Spain")

    lang = Languages()
    lang.setLanguage(AvailableLanguages.Spanish)

    limit = TimeLimit()
    limit.setDay()

    page = GooglePages()
    page.searchImage()
    page.searchShops()

    image = GoogleImages()
    # image.setImageFormat("jpg")
    # image.setImageSize(">400*300")

    news = GooglePages()
    news.searchNews()

    vid = GooglePages()
    vid.searchVideos()

    patents = GooglePages()
    patents.searchPatents()

    patents_params = GooglePatents()
    patents_params.setOfficePatent(OfficePatents.USA)
    patents_params.setPatentStatus(PatentStatus.Applications)
    patents_params.setPatentType(AvailablePatentTypes.Design)

    prepared_query = GoogleSearch() \
        .withQuery("test") \
        .withContainingTwoTerms("psico", "analysis") \
        .withExcludedWords(["press"]) \
        .withNumberOfResults(20) \
        .withResultBetweenTwoNumbers(10, 20) \
        .withResultsAtCountry(country) \
        .withResultsLanguage(lang) \
        .withTimeLimit(limit)
    # torify()
    s_extractor = SearchExtractor(must_use_session=True, with_history_enabled=True)
    # print(URLBuilder(prepared_query).build())
    # sbu = URLBuilder(prepared_query)
    # nr = s_extractor.extract_url(sbu)
    # pp.pprint(nr)

    npq = GoogleSearch().withQuery("cursos hablar en público en madrid").withNumberOfResults(10)\
        .withResultsLanguage(lang)

    # npq2 = GoogleSearch().withQuery("cursos hablar en público en madrid").withNumberOfResults(10) \
    #     .withResultsLanguage(lang).withSearchingAtDifferentGooglePages(vid)
    # npq3 = GoogleSearch().withQuery("clock").withNumberOfResults(10) \
    #     .withResultsLanguage(lang).withSearchingAtDifferentGooglePages(patents).withPatentParams(patents_params)
    url = URLBuilder(npq).build()
    print(url)
    # p_extractor = PatentExtractor(with_history_enabled=True)
    # res = p_extractor.extract_url(URLBuilder(npq3))
    # pp.pprint(res.result())

    # v_extractor = VideoExtractor(with_history_enabled=True)
    # res = v_extractor.extract_url(URLBuilder(npq2))
    # pp.pprint(res.result())
    # v_extractor.printOverallTime()
    #
    # for i in range(1):
    #     # print(url)
    #     nr1 = s_extractor.extract_url(URLBuilder(npq))
    #     # print("Waiting for values...")
    #     result = nr1.result(10)
    #     ex = nr1.exception()
    #     if ex:
    #         print(ex)
    #     pp.pprint(result)
    # s_extractor.printOverallTime()

    # start_time = time.time()
    # data = rq.get(url)
    # end_time = time.time()
    # print("Data time: " + str((end_time - start_time)) + " s")
    # start_time = time.time()
    # content = data.content
    # end_time = time.time()
    # print("Content time: " + str((end_time - start_time)) + " s")
    '''
    build_url = URLBuilder(prepared_query).build()
    print(build_url)
    data = rq.get(build_url).content
    soup = BeautifulSoup(data, 'html.parser')
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134"
                      " Safari/537.36"}

    print(soup.prettify())'''
    # extractor = ImageExtractor(must_use_session=True, with_history_enabled=True)
    # for m in range(10):
    #     n_p_q = GoogleSearch().withQuery("cursos hablar en público madrid").withNumberOfResults(
    #         10).withSortByUpdateTime().withSearchingAtDifferentGooglePages(page).withImageParams(image)
    #     nbu = URLBuilder(n_p_q)
    #     # print(nbu.build())
    #     result = extractor.extract_url(nbu)
    #     # pprint(result)
    #     pp.pprint(result.result())
    # s_extractor.printOverallTime()
    # extractor.printOverallTime()
    #
    # npqa = GoogleSearch().withQuery("tailandia").withResultsLanguage(lang).withTimeLimit(limit)\
    #     .withSearchingAtDifferentGooglePages(news)
    # print(URLBuilder(npqa).build())
    # news_ex = NewsExtractor(with_history_enabled=True, must_use_session=False)
    # rs = news_ex.extract_url(URLBuilder(npqa))
    # # try:
    # pp.pprint(rs.result())
    # except Exception as e:
    #     print(str(e))
    '''print(nbu)
    ndata = rq.get(nbu, headers=header).content
    ns = BeautifulSoup(ndata, 'html.parser')
    actual_images = []
    for a in ns.find_all("div", {"class": "rg_meta"}):
        link, image_type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        if not image_type:
            image_type = "unknown format"
        actual_images.append((link, image_type))
    print(ns.prettify())
    print("There are total: " + str(len(actual_images)) + " images")
    for i, (img_link, img_type) in enumerate(actual_images):
        print("\t- Image link [" + str(i) + "]: " + img_link + "\n\t\t- Image type [" + str(i) + "]: " + img_type)'''
    country = Countries()
    country.setCountry(AvailableCountries.Spain)
    pages = GoogleSearch()
    page.searchBooks()
    # params = GoogleShop()
    # params.orderByReviewScore()
    # params.onlyNewProducts()
    params = GoogleBooks()
    params.searchOnlyBooks()
    pages.withDefiningTerm("palabra").withResultsLanguage(lang)
    print(URLBuilder(pages).build())
    # pages.withNumberOfResults(10).withQuery("papás").withSearchingAtDifferentGooglePages(page).withInterfaceLanguage(InterfaceLanguages.InterfaceLanguages.English).withBookParams(params)
    # print(URLBuilder(pages).build())
    # b_ex = BookExtractor(must_use_session=False, with_history_enabled=True)
    # pg = b_ex.extract_url(URLBuilder(pages))
    # pp.pprint(pg.result())
    # sh_extractor = ShopExtractor(must_use_session=False, with_history_enabled=True)
    # pg = sh_extractor.extract_url(URLBuilder(pages))
    # pp.pprint(pg.result())


if __name__ == '__main__':
    main()
