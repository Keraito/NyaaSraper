# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NyaascraperItem(scrapy.Item):
    # Name of the torrent.
    name = scrapy.Field()
    # Upload time of the torrent.
    date = scrapy.Field()
    # URL to the torrent.
    url = scrapy.Field()
