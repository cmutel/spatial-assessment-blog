#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u"Chris Mutel"
SITENAME = u"Spatial Assessment"
SITEURL = 'http://chris.mutel.org'
SITESUBTITLE = "weblog of Chris Mutel"
TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Blogroll
LINKS =  (('Me@ESD group', 'http://www.ifu.ethz.ch/ESD/people/cmutel'),
          ('My publications', 'http://scholar.google.ch/citations?user=SJiuf-MAAAAJ'),
          ('My code', 'https://bitbucket.org/cmutel/'),
          ('Brightway2', 'http://brightwaylca.org'),)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = 5
STATIC_PATHS = ['images']
TYPOGRIFY = True
THEME = "theme"
DISPLAY_PAGES_ON_MENU = False
PLUGINS = ["latex"]
FEED_ATOM = False
FEED_RSS = False
DISQUS_SITENAME = "spatialassessment"
GOOGLE_ANALYTICS = "UA-36804441-1"
