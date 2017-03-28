# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json
import pyrebase

class NyaascraperPipeline(object):

    def open_spider(self, spider):
        with open('NyaaScraper/firebase.json') as firebase_config:
            firebase_config_json = json.load(firebase_config)
        self.firebase = pyrebase.initialize_app(firebase_config_json)

    def close_spider(self, spider):
        auth = self.firebase.auth()
        db = self.firebase.database()
        with open('NyaaScraper/auth.json') as auth_config:
            auth_config_json = json.load(auth_config)
            user = auth.sign_in_with_email_and_password(auth_config_json["email"], auth_config_json["password"])
            data = {"Seiren": "5"}
            db.child("anime").update(data, user['idToken'])
            # db.child("users").child("Morty").remove(user['idToken'])

    def process_item(self, item, spider):
        # TODO: Check whether the title, number and translator of the torrent.
        # TODO: Send to FireBase.
        return item
