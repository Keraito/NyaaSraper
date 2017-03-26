# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
from scrapy.exceptions import DropItem

class NyaascraperPipeline(object):

    def __init__(self):
        self.current_time = datetime.datetime.utcnow()

    def process_item(self, item, spider):
        # Convert the date scraped from the torrent (f.e. '2017-03-25, 18:37 UTC') to a datetime object.
        torrent_time = datetime.datetime.strptime(item['date'], '%Y-%m-%d, %H:%M %Z')
        # Calculate the difference between now and the torrent_time date object.
        difference = self.current_time - torrent_time
        # Convert them into (hours, minutes).
        hm_difference = divmod(difference.days * 1440 + difference.seconds/60, 60)
        # Check if the torrent was uploaded longer than 24 hours ago.
        if hm_difference > (24, 0):
            raise DropItem("Torrent not uploaded within 24 hours: %s." % item)
        return item
