import scrapy
from NyaaScraper.items import NyaascraperItem

class NyaaTorrentsScraper(scrapy.Spider):
    name = "nyaatorrents"
    start_urls = [
        'https://www.nyaa.se/?page=search&cats=1_37&minage=0&maxage=1&offset=1',
    ]

    def parse(self, response):
        for torrent in response.css('td.tlistname'):
            item = NyaascraperItem()
            request = scrapy.Request(response.urljoin(torrent.css('a::attr(href)').extract_first()), callback=self.parse_download_link)
            request.meta['item'] = item

            item['name'] = torrent.css('a::text').extract_first()
            item['url'] = torrent.css('a::attr(href)').extract_first()
            yield request
        # Extract the url to the next page based on the '>' indicator on the page.
        # There are two of these indicators on the page.
        # This line assumes the first in the list is always the '>' instead of the '>>'.
        next_page = response.css('div.rightpages a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_download_link(self, response):
        item = response.meta['item']
        item['date'] = response.css('td.vtop::text').extract_first()
        yield item
