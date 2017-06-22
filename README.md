# NyaaScraper
NyaaScraper is a spider/scraper written using [Scrapy](https://scrapy.org/) and Python for the purpose of scraping anime torrents content from Nyaatorrents (nyaa.se), an anime torrents tracker, to a [Firebase](https://firebase.google.com/) database.

The spider was hosted on [Scrapinghub](https://app.scrapinghub.com) to be run daily and can be executed by running `scrapy crawl nyaatorrents -s API_KEY="api_key_firebase_db" -s EMAIL="email_firebase_account" -s PASSWORD="pw_firebase_account"`.

Unfortunately, as of May 2017, Nyaatorrents was shut down due to EU regulations. Therefore, I've paused development on this project and [Nyaalert](https://github.com/Keraito/Nyaalert) (the front-end). I'm aware of current substitutes for Nyaatorrents, but will wait for a stabilised version before migrating.
