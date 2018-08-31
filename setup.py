from setuptools import setup
from sys import version

from pyGle.version import __version__

# if version < '3':
#     raise RuntimeError("Python v3 at least needed")

try:
    import codecs

    readme = codecs.open(filename="README.rst", encoding="utf-8")
    long_description = readme.read()
    readme.close()
except:
    long_description = ''


requirements = ['lxml', 'beautifulsoup4', 'ujson', 'typing']
if version < '3':
    requirements.append('futures')


setup(
    name='g-pyGle',
    version=__version__,
    packages=['pyGle', 'pyGle.url', 'pyGle.values', 'pyGle.extractor'],
    url='https://github.com/Javinator9889/pyGle',
    license='GPL-3.0',
    author='Javinator9889',
    author_email='javialonso007@hotmail.es',
    description='A tool for searching the entire web with the Google technology',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    download_url="https://github.com/Javinator9889/pyGle/archive/master.zip",
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Programming Language :: Python',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Natural Language :: English',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
    ]
)
