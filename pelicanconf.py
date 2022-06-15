#!/usr/bin/env python
# -*- coding: utf-8 -*- #
AUTHOR = "Chris Mutel"
SITENAME = "Spatial Assessment"
SITEURL = 'https://chris.mutel.org'
SITESUBTITLE = "Weblog of Chris Mutel"
TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = 'en'
TIMEZONE = 'Europe/Paris'

PATH = 'content'


# Blogroll
LINKS = (
    ('Notable posts', 'https://chris.mutel.org/tag/notable/index.html'),
    ('PSI', 'https://www.psi.ch/ta/cmutel'),
    ('Brightway', 'https://brightwaylca.org'),
    ('Cauldron', 'https://cauldron.ch/'),
    ('Publications', 'http://scholar.google.ch/citations?user=SJiuf-MAAAAJ'),
)


# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = 10
STATIC_PATHS = ['images']
THEME = "alchemy"
# DISPLAY_PAGES_ON_MENU = False
PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ["render_math"]
# FEED_ATOM = 'feeds/all.atom.xml'
# FEED_RSS = False
DISQUS_SITENAME = "spatialassessment"
RELATIVE_URLS = False
# GOOGLE_ANALYTICS = "UA-36804441-1"

TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"

HIDE_AUTHORS = True

SITEIMAGE = '/theme/image/map.png'
