#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u"Chris Mutel"
SITENAME = u"Spatial Assessment"
SITEURL = 'http://chris.mutel.org'
SITESUBTITLE = "weblog of Chris Mutel"
TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Blogroll
LINKS = (
    ('Notable posts', 'http://chris.mutel.org/tag/notable/index.html'),
    # ('ESD group', 'http://www.ifu.ethz.ch/ESD/index_EN'),
    ('Me@ESD group', 'http://www.ifu.ethz.ch/ESD/people/cmutel/index_EN'),
    ('Brightway2', 'http://brightwaylca.org'),
    ('Source for this blog', 'https://bitbucket.org/cmutel/spatial-assessment-blog'),
    ('My publications', 'http://scholar.google.ch/citations?user=SJiuf-MAAAAJ'),
    ('My code', 'https://bitbucket.org/cmutel/'),
    ('My talks', 'http://chris.mutel.org/tag/talks/index.html'),
    ('My videos', 'https://www.youtube.com/user/chrismutel/videos'),
)


# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = 10
STATIC_PATHS = ['images']
TYPOGRIFY = True
THEME = "theme"
DISPLAY_PAGES_ON_MENU = False
PLUGINS = ["latex"]
FEED_ATOM = False
FEED_RSS = False
DISQUS_SITENAME = "spatialassessment"
GOOGLE_ANALYTICS = "UA-36804441-1"

TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"
