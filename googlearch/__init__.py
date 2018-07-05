#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#


def main():
    import requests as rq

    from bs4 import BeautifulSoup
    from url import GoogleSearch, URLBuilder
    from values import Countries, TimeLimit, Languages, GooglePages

    country = Countries()
    country.setCountry("Spain")
    lang = Languages()
    lang.setLanguage("Spanish")
    limit = TimeLimit()
    limit.setDay()
    page = GooglePages()
    page.searchImage()

    prepared_query = GoogleSearch() \
        .withQuery("test") \
        .withContainingTwoTerms("psico", "analysis") \
        .withExcludedWords(["press"]) \
        .withNumberOfResults(20) \
        .withResultBetweenTwoNumbers(10, 20) \
        .withResultsAtCountry(country) \
        .withResultsLanguage(lang) \
        .withTimeLimit(limit)
    build_url = URLBuilder(prepared_query).build()
    print(build_url)
    data = rq.get(build_url).content
    soup = BeautifulSoup(data, 'html.parser')

    print(soup.prettify())

    n_p_q = GoogleSearch().withQuery("cursos hablar en público madrid").withNumberOfResults(
        20).withSortByUpdateTime().withSearchingAtDifferentGooglePages(page)
    nbu = URLBuilder(n_p_q).build()
    print(nbu)
    ndata = rq.get(nbu).content
    ns = BeautifulSoup(ndata, 'html.parser')

    print(ns.prettify())


if __name__ == '__main__':
    main()
