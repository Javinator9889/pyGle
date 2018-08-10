# [pyGle](https://github.com/Javinator9889/pyGle)
A tool for searching the entire web with the Google technology

[![PyPi](https://img.shields.io/badge/v1.0%20-PyPi-green.svg)](https://pypi.org/project/g-pyGle/)
[![ZIP](https://img.shields.io/badge/Package%20-Zip-blue.svg)](https://github.com/Javinator9889/pyGle/archive/master.zip)
[![GIT](https://img.shields.io/badge/Package%20-Git-red.svg)](https://github.com/Javinator9889/pyGle.git)

## Index
1. [Introduction](https://github.com/Javinator9889/pyGle#Introduction)
2. [Purpose](https://github.com/Javinator9889/pyGle#Purpose)
3. [Installation](https://github.com/Javinator9889/pyGle#Installation)
4. [Instructions](https://github.com/Javinator9889/pyGle#Instructions)
5. [Contribute](https://github.com/Javinator9889/pyGle#Contribute)
6. [License](https://github.com/Javinator9889/pyGle#License)

## 1. Introduction

[pyGle](https://github.com/Javinator9889/pyGle) aims to be a *very powerful* tool for just **searching the entire web** 
by using the *Google* technology, without **any limitations** (or almost no one).

Just with a *few lines* of code you will be able to:
* Perform a *normal search* on Google 🔎
* Look at *Google Images* for obtaining all the information you need about a pic 🌅
* Search *the latest news* and also **a lot of articles** on *Google News* 📰
* Filter and obtain *patents* by using *Google Patents* 📝
* Have a look at hundreds of *different products* at *Google Shops* 🛒
* Look for *books*, *magazines* and more at *Google Books* 📘
* Videos, videos and more videos at *Google Videos* 🎥

As the speed is a crucial factor, I developed this library in order to be the fastest one for each possible situation.

With every search, a little log is included at the end of the result with the **available stats** for the web scrapping.
After some test, I noticed that using *[requests](https://github.com/requests/requests)* **slow down** the overall 
speed. For that reason is why you can see the lib performs all *Internet access* by using 
*[urllib](https://docs.python.org/3/library/urllib.html)*, which has two advantages:

1. Is included with **all Python installations**, so it is a less library to install.
2. The requests overall time has been reduced at almost **70%**: with *requests*, it took about **3~4 seconds**. 
With *urllib*, that time now becomes about **~1 second** or less.

With the motivation of the said before, when performing a *research*, the lib **instantly** returns the object that you 
will use in the future for gathering the results. That object is also known as a **Future** (*you can read more 
information right here* 
[👉 Python Concurrent Futures](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future)), 
whose functionality is the following:

+ You want to *do a research* at Google.
+ As explained before, it needs about **~1 second** to complete, so it is a lot of time for you to do *other things* 
that do not depend on the result of your search.
+ So when you *ask [pyGle](https://github.com/Javinator9889/pyGle)* to scrap the web with Google, it returns a **Future** object. At the first moment, it does 
have **nothing**, but when [pyGle](https://github.com/Javinator9889/pyGle) ends its work, the Future object will contain all the data.
+ [pyGle](https://github.com/Javinator9889/pyGle) automatically detects the *number of processors* of your system so it can speed-up all the process.

## 2. Purpose

Searching the web with Google *is very easy* from a web browser such as Chrome or Firefox, but sometimes we need that 
**information** to be available for a program that we are developing or similar. Or just we need to *transform and work 
with that info*.

For that situation, [pyGle](https://github.com/Javinator9889/pyGle) is the real solution. By using the powerful 
*[Python lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)* and also 
*[Python dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)*, [pyGle](https://github.com/Javinator9889/pyGle) will give you all 
what you need. Let me exemplify you with a simple search of the term *"test"*:

1. Here is the simplicity of [pyGle](https://github.com/Javinator9889/pyGle) in code for achieving that:
    ```python
    from pprint import pprint  # Not necessary but for a beautiful print
    from pyGle import PyGle
 
    pSearch = PyGle(query="test")
    ft = pSearch.doSearch()  # A Future object
    pprint(ft.result())
    ```

2. And now, when the Future is done, here is the result:
    ```python
    [   {   'cached_version': 'http://webcache.googleusercontent.com/search?q=cache:jNPwduM3zRgJ:www.eljueves.es/news/test-que-meme-eres_2448+&cd=1&hl=es&ct=clnk&gl=es',
        'date': '30 may. 2018',
        'description': '30 may. 2018 -Olvídalas Lo mejor para definir tu '
                       'personalidad son los memes. Descubre cuál es el tuyo '
                       'con este rigurosotestavalado por la Universidad...',
        'link': 'http://www.eljueves.es/news/test-que-meme-eres_2448',
        'title': 'TEST: ¿Qué meme eres? - El Jueves'},
    {   'cached_version': 'https://webcache.googleusercontent.com/search?q=cache:nbx31tovq8UJ:https://www.enfemenino.com/psico/tests-ssc17.html+&cd=2&hl=es&ct=clnk&gl=es',
        'date': 'unavailable',
        'description': 'Tests-Testde personalidad de inteligencia de '
                       'belleza... todo tipo detestque te pueden ayudar a '
                       'tomar decisiones o simplemente aclararte las ideas.',
        'link': 'https://www.enfemenino.com/psico/tests-ssc17.html',
        'title': 'Tests - Tests de personalidad, inteligencia, moda, belleza, '
                 '| enfemenino'},
    {   'cached_version': 'https://webcache.googleusercontent.com/search?q=cache:PQFS2G6QNgAJ:https://www.muyinteresante.es/tests+&cd=3&hl=es&ct=clnk&gl=es',
        'date': 'unavailable',
        'description': 'TestsMuyInteresante.es. Mide tu ingenio y lo que sabes '
                       'de forma divertida y amena.',
        'link': 'https://www.muyinteresante.es/tests',
        'title': 'Tests inteligentes y curiosos en Muy Interesante España'},
    {   'cached_version': 'https://webcache.googleusercontent.com/search?q=cache:iQ_U_r5BkKkJ:https://www.testdevelocidad.es/+&cd=4&hl=es&ct=clnk&gl=es',
        'date': 'unavailable',
        'description': 'Testde velocidad para medir la calidad de tu acceso a '
                       'Internet con ADSL o fibra óptica . Comprueba la '
                       'velocidad real de tu conexión.',
        'link': 'https://www.testdevelocidad.es/',
        'title': 'Test de velocidad : Mide tu ADSL o fibra con el SpeedTest de '
                 'www ...'},
    {   'cached_version': 'https://webcache.googleusercontent.com/search?q=cache:m6vzOP8qmEsJ:https://www.arealme.com/mental/es/+&cd=5&hl=es&ct=clnk&gl=es',
        'date': 'unavailable',
        'description': 'Testde edad mental. cual es tu edad mental. Estetestes '
                       'de origen japonés y se llama . Por favor sé sincero al '
                       'responder a las preguntas.',
        'link': 'https://www.arealme.com/mental/es/',
        'title': 'Test de edad mental (cual es tu edad mental) - A Real Me'},
    {   'cached_version': 'https://webcache.googleusercontent.com/search?q=cache:gU4XOSuOIR0J:https://www.clara.es/temas/test+&cd=6&hl=es&ct=clnk&gl=es',
        'date': 'unavailable',
        'description': 'Haz nuestrostesty descubre cuál es la mejor dieta para '
                       'adelgazar los mejores tratamientos estéticos y de '
                       'belleza los alimentos que mejor te sientan.',
        'link': 'https://www.clara.es/temas/test',
        'title': 'Test dieta, belleza, salud, alimentación, nutrición, '
                 'psicología, moda…'},
    {   'cached_version': 'https://webcache.googleusercontent.com/search?q=cache:2C5cLoSzSKoJ:https://testdivertidos.es/+&cd=7&hl=es&ct=clnk&gl=es',
        'date': 'unavailable',
        'description': 'TestDivertidos.es - Lostestsgratis más divertidos de '
                       'internet:testde inteligencia personalidad psicológicos '
                       'de amor para niños...',
        'link': 'https://testdivertidos.es/',
        'title': 'Test Divertidos | Los tests más divertidos de la web'},
    {   'cached_version': 'https://webcache.googleusercontent.com/search?q=cache:hBp-w20VAWEJ:https://www.psicoactiva.com/tests/personalidad/test-personalidad-5factores.htm+&cd=8&hl=es&ct=clnk&gl=es',
        'date': 'unavailable',
        'description': 'Testgratis que evalúa la Personalidad a partir de sus '
                       'cinco Dimensiones llamadas Los Cinco Grandes.',
        'link': 'https://www.psicoactiva.com/tests/personalidad/test-personalidad-5factores.htm',
        'title': 'PsicoActiva.com: Test de personalidad de cinco factores.'},
    {   'cached_version': 'https://webcache.googleusercontent.com/search?q=cache:3_8PsvuNwh0J:https://www.nationalgeographic.com.es/temas/tests-ng+&cd=9&hl=es&ct=clnk&gl=es',
        'date': 'unavailable',
        'description': 'Pon a prueba tus conocimientos con losTESTde National '
                       'Geographic sobre historia naturaleza países ciencia '
                       'personajes históricos ciudades...',
        'link': 'https://www.nationalgeographic.com.es/temas/tests-ng',
        'title': 'Los mejores TEST de National Geographic'},
    {   'cached_version': 'http://webcache.googleusercontent.com/search?q=cache:-7iUEjuLNkMJ:www.movistar.es/particulares/test-de-velocidad/+&cd=10&hl=es&ct=clnk&gl=es',
        'date': 'unavailable',
        'description': 'Comprueba la velocidad de tu conexión a Internet con '
                       'eltestde velocidad que usan los instaladores de '
                       'Movistar OFERTA FIBRA -63 DESCUENTO 900 104...',
        'link': 'http://www.movistar.es/particulares/test-de-velocidad/',
        'title': 'Test Velocidad ADSL y Fibra - Mide la velocidad de tu '
                 'Internet - Movistar'},
    {   'google_stats': 'Aproximadamente 3.090.000.000 resultados(0,34 '
                        'segundos)',
        'how_many_results': 10,
        'related_search': [   'testcuriosos',
                              'testdivertidos',
                              'testpara adolescentes',
                              'tests de personalidad',
                              'tests divertidos para pasar el rato',
                              'testjuegos',
                              'testde belleza',
                              'tests de amor'],
        'stats': {   'google_search_time': '0.8270025253295898 s',
                     'overall_time': '0.8999979496002197 s',
                     'parsing_page_time': '0.040498971939086914 s'},
        'url': 'https://www.google.com/search?q=test'}]
    ```
    At this case, I am in Spain, so the results language are based on your **current location** (if you *do not 
    specify one*).
    
If another page must be searched, all the methods start with: ```with```. You can find more instructions at the 
[wiki](https://github.com/Javinator9889/pyGle/wiki).

## 3. Installation

As usual, you have the [pip](https://pypi.org/project/pip/) mode or the 
[easy install](https://setuptools.readthedocs.io/en/latest/easy_install.html) methods:

*The commands for *Windows* are the same but without `sudo`*

### *Installing via PyPi (pip)*

+ In some Linux systems, *pip* is not directly available in command line, so we have two options:
    
    *Installing pip for Python 3* (assuming that you **already have Python 3 installed**): 
    ```bash
    ## DEBIAN SYSTEMS ##
    sudo apt update && sudo apt upgrade
    sudo apt-get install python3-pip
    ```
    ```bash
    ## CENTOS ##
    sudo yum install python34-setuptools
    sudo easy_install pip
    ```

+ Installing [pyGle](https://github.com/Javinator9889/pyGle):
    
    Once you did what said before, now you are able to install [pyGle](https://github.com/Javinator9889/pyGle)
    ```bash
    #### USING PIP ####
    sudo pip3 install g-pyGle
  
    ## If pip3 is not available ##
    sudo pip install g-pyGle
  
    ## Via Python 3 ##
    sudo python3 -m pip install g-pyGle

    ## Without admin permissions ##
    pip3 install -U g-pyGle 
    OR
    python3 -m pip install -U g-pyGle
    ```

### *Installing via easy install*

+ Basically, we will install *Python 3* on our systems, and then we will be able to install [pyGle](https://github.com/Javinator9889/pyGle):
    
    + [Windows](https://realpython.com/installing-python/#windows)
    + [Linux (all systems)](https://realpython.com/installing-python/#linux)
    + [MacOS](https://realpython.com/installing-python/#macos-mac-os-x)
    + [iOS](https://realpython.com/installing-python/#ios-iphone-ipad)
    + [Android](https://realpython.com/installing-python/#android-phones-tablets)
    
+ Now, we can install [pyGle](https://github.com/Javinator9889/pyGle) as follows:
    ```bash
    #### USING EASY INSTALL ####
    git clone https://github.com/Javinator9889/pyGle.git
    cd pyGle
    sudo python3 setup.py install
    ```
    
## 4. Instructions

Every time we want to use [pyGle](https://github.com/Javinator9889/pyGle), we will do the following:

```python
from pyGle import PyGle
```

[pyGle](https://github.com/Javinator9889/pyGle) allows us to **enable a history** and **keep the session cookies** (for a faster browsing):
```python
pSearch = PyGle(enable_history=True, use_session_cookies=True)
```

As normal, [pyGle](https://github.com/Javinator9889/pyGle) will only do a normal Google search if we add a query:
```python
pSearch.withQuery("what we want to search")
```

Also, with every method, you can continue *defining your needs* without **creating thousands** of lines of code:
```python
pSearch.withQuery("what we want to search").withContainingTwoTerms("term 1", "term 2").withTextInTitle("text in title").withSafeModeDeactivated().withSearchStartPositionAt(25)
```

Once we are done, searching is as simple as:
```python
ft = pSearch.doSearch()

# Wait for the result to be available
search_results = ft.result()
```

Finally, we can recover (if enabled) all the history of the search we did just:
```python
history = pSearch.getHistory()

# Or printing history
pSearch.pprintHistory()
```

*If you want to read more, have a look at the [wiki](https://github.com/Javinator9889/pyGle/wiki)*.

### *Torify*

Another functionality included with this lib is the possibility to work under **Tor**.

If you do not know what is it, **Tor** is the *easiest way* to browse the web anonymously by using proxies that hide 
yourself. You can read more [right here](https://lifehacker.com/what-is-tor-and-should-i-use-it-1527891029).

If you want *to use this functionality*, you need to have Tor installed on your system. Here you have the instructions 
for your systems:

+ [Windows](https://www.quora.com/How-do-I-run-Tor-headless-on-Windows-10)
+ [Linux](https://www.torproject.org/docs/debian.html.en)
+ [MacOS](https://www.torproject.org/docs/tor-doc-osx.html.en)
+ [Android](https://www.torproject.org/docs/android.html.en)

Finally, once Tor is configured on your system, for using it is as simple as (*following the latest example*):
```python
ft = pSearch.doSearch(torify=True)
```

## 5. Contribute
If you really appreciate my work, you can *contribute to this project* perfectly, for example:

1. If you find **bugs** 🔎🐞, you can comment at [issues](https://github.com/Javinator9889/pyGle/issues) what happened to 
you and *I will try to find a solution*.
2. You can **fork** this repository and *include all what you think* [pyGle](https://github.com/Javinator9889/pyGle) should have. Create a pull request and, if I
 like your changes, I will include it on the official repo and you will automatically become a developer and 
 maintainer 😄
3. Also, if you are a great fan, you can donate me what you want by clicking here 🤑

[![Donate me](http://pluspng.com/img-png/paypal-donate-button-png-paypal-donate-button-png-file-png-image-200.png)](https://paypal.me/Javinator9889)

## 6. License

    Copyright (C) 2018 - Javinator9889 - pyGle
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.`