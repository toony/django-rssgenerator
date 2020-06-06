import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-rssgenerator',
    version = '1.5',
    packages = ['rssgenerator'],
    include_package_data = True,
    license = 'GNU GPLv3+',
    description = 'A simple Django app to create and manage RSS feed.',
    long_description = open('README.txt').read(),
    url = 'https://github.com/toony/django-rssgenerator',
    author = 'Anthony Prades',
    author_email = 'toony.github@chezouam.net',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        "wheel",
        "Django == 2.2.13",
        "PyRSS2Gen >= 1.1",
        "python-magic",
        "django-background-tasks == 1.2.5",
        "pillow >= 7.0.0",
    ],
)
