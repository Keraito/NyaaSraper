# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class NyaascraperPipeline(object):

    def process_item(self, item, spider):
        # TODO: Check whether the title, number and translator of the torrent.
        # TODO: Send to FireBase.
        return item
