#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'code'
SITENAME = u'Douban CODE'
SITEURL = ''

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('CODE', '/pages/code.html'),
         ('SQLStore', '/pages/sqlstore.html'),
         ('MC', '/pages/mc.html'),
         ('Quixote', '/pages/quixote.html'),
         ('Ellen', '/pages/ellen.html'),
         ('Pygit2', '/pages/pygit2.html'),
         ('GPack', '/pages/gpack.html'),
         ('Linguist', '/pages/linguist.html'),
         ('Scanner', '/pages/scanner.html'),
         ('Mikoto', '/pages/mikoto.html'),
         ('Misaka', '/pages/misaka.html'),
         ('About', '/pages/about.html'),)

# Social widget
SOCIAL = (('Douban@GitHub', 'https://github.com/douban'),
          ('CODE@GitHub', 'https://github.com/douban-code'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
THEME = 'themes/foundation'
FOUNDATION_PYGMENT_THEME = 'code'
FOUNDATION_FOOTER_TEXT = 'CODE © Douban Inc. 2012-2014'
TEMPLATE_PAGES = {'blog.html': 'blog.html', }
