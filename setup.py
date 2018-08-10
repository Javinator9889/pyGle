from setuptools import setup
from pyGle.version import __version__


def requirements() -> list:
    with open("pyGle/requirements.txt", 'r') as f:
        req = f.read().splitlines()
    return req


setup(
    name='pyGle',
    version=__version__,
    packages=['pyGle', 'pyGle.url', 'pyGle.values', 'pyGle.extractor'],
    url='',
    license='GPL-3.0',
    author='Javinator9889',
    author_email='javialonso007@hotmail.es',
    description='A tool for searching the entire web with the Google technology',
    include_package_data=True,
    install_requires=requirements(),
    zip_safe=False,
    classifiers=[
            'Development Status :: 4 - Production/Beta',
            'Programming Language :: Python',
            'Environment :: Console',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: POSIX :: Linux',
            'Natural Language :: English',
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
