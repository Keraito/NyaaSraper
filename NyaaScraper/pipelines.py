# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json
import pyrebase
import re
import os

class NyaascraperPipeline(object):

    def __init__(self, api_key, email, password):
        self.firebase_config_json = {
            "apiKey": api_key,
            "authDomain": "nyaalert.firebaseapp.com",
            "databaseURL": "https://nyaalert.firebaseio.com",
            "storageBucket": "nyaalert.appspot.com"
        }
        self.auth_config_json = {
            "email" : email,
            "password" : password
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            api_key=crawler.settings.get('API_KEY'),
            email=crawler.settings.get('EMAIL'),
            password=crawler.settings.get('PASSWORD')
        )

    def open_spider(self, spider):
        self.tracking = ['Saenai Heroine no Sodatekata', 'Rokudenashi Majutsu Koushi to Akashic Records']
        self.qualities = ['720p']
        self.subbers = ['HorribleSubs']
        self.data = {}
        # with open('NyaaScraper/firebase.json') as firebase_config:
        # firebase_config_json = json.load(firebase_config)
        firebase = pyrebase.initialize_app(self.firebase_config_json)
        auth = firebase.auth()
        self.db = firebase.database()
        # with open('NyaaScraper/auth.json') as auth_config:
            # auth_config_json = json.load(auth_config)
        self.user = auth.sign_in_with_email_and_password(self.auth_config_json["email"], self.auth_config_json["password"])
        # Get all the animes that are currently in the databse. This is an array of PyreResponse objects.
        self.existing_anime = self.db.child('anime').get().each()

    def close_spider(self, spider):
        self.db.child('anime').update(self.data, self.user['idToken'])
        # db.child("users").child("Morty").remove(user['idToken'])

    def process_item(self, item, spider):
        incoming_name = item['name']
        for quality in self.qualities:
            # Check quality of the incoming anime torrent.
            if quality not in incoming_name:
                raise DropItem('Quality %s was not found in %s.' % (quality, item))
            for tracking_subs in self.subbers:
                # Check whether the title of a tracking anime is in the incoming torrent title.
                if tracking_subs in incoming_name:
                    # Strip the extension from the title.
                    title, ext = os.path.splitext(incoming_name)
                    # Get rid of all the brackets with text into them and the whitespaces around them ('[1080p]' and '[Subs]' f.e.).
                    name_episode = re.sub('\s*\[\w+\]\s*', '', title)
                    try:
                        # Split on dash with all the necessary whitespaces between and after.
                        name_and_epi = name_episode.rsplit(' - ', 1)
                        name = name_and_epi[0]
                        # Parse the second episode number to a Integer.
                        epi = int(name_and_epi[1])
                        # Check whether the anime already exists in the firebase database and whether this is a new episode.
                        for anime in self.existing_anime:
                            if name == anime.key() and epi <= anime.val():
                                raise DropItem('Firebase already has episode %s of %s.' % (anime.val(), item))
                        # Check the currently scraped animes as well.
                        scraped_anime = self.data
                        if name in scraped_anime and epi <= scraped_anime[name]:
                            raise DropItem('Current scraping already scraped later episode of %s.' % item)
                        self.data.update({ name : epi })
                        return item
                    # Catch the error thrown when parsing the episode number fails.
                    except ValueError:
                        raise DropItem('Wrong parsing of episode number in %s.' % item)
            raise DropItem('Not a HorribleSubs episode: %s.' % item)
