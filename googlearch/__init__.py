#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#


def main():
    import requests as rq
    import ujson as json

    from bs4 import BeautifulSoup
    import pprint

    from url import GoogleSearch, URLBuilder
    from values import Countries, TimeLimit, Languages, GooglePages, GoogleImages
    from extractor import ImageExtractor, SearchExtractor

    pp = pprint.PrettyPrinter(indent=4)
    country = Countries()
    country.setCountry("Spain")

    lang = Languages()
    lang.setLanguage("Spanish")

    limit = TimeLimit()
    limit.setDay()

    page = GooglePages()
    page.searchImage()

    image = GoogleImages()
    image.setImageFormat("jpg")
    image.setImageSize(">400*300")

    prepared_query = GoogleSearch() \
        .withQuery("test") \
        .withContainingTwoTerms("psico", "analysis") \
        .withExcludedWords(["press"]) \
        .withNumberOfResults(20) \
        .withResultBetweenTwoNumbers(10, 20) \
        .withResultsAtCountry(country) \
        .withResultsLanguage(lang) \
        .withTimeLimit(limit)
    s_extractor = SearchExtractor()
    print(URLBuilder(prepared_query).build())
    sbu = URLBuilder(prepared_query)
    nr = s_extractor.extract_url(sbu)
    pp.pprint(nr)

    npq = GoogleSearch().withQuery("pprint").withNumberOfResults(50)
    print(URLBuilder(npq).build())
    nr1 = s_extractor.extract_url(URLBuilder(npq))
    pp.pprint(nr1)
    '''
    build_url = URLBuilder(prepared_query).build()
    print(build_url)
    data = rq.get(build_url).content
    soup = BeautifulSoup(data, 'html.parser')
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134"
                      " Safari/537.36"}

    print(soup.prettify())'''

    # n_p_q = GoogleSearch().withQuery("cursos hablar en público madrid").withNumberOfResults(
    #     20).withSortByUpdateTime().withSearchingAtDifferentGooglePages(page).withImageParams(image)
    # nbu = URLBuilder(n_p_q)
    # print(nbu.build())
    # extractor = ImageExtractor()
    # result = extractor.extract_url(nbu)
    # # pprint(result)
    # pp.pprint(result)
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


if __name__ == '__main__':
    main()
