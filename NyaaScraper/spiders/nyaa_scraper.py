import scrapy
from NyaaScraper.items import NyaascraperItem

class NyaaTorrentsScraper(scrapy.Spider):
    name = "nyaatorrents"
    start_urls = [
        'https://www.nyaa.se/?page=search&cats=1_37&minage=0&maxage=3&offset=1',
    ]

    def parse(self, response):
        for torrent in response.css('td.tlistname'):
            item = NyaascraperItem()
            # yield {
            #     'name'  :   torrent.css('a::text').extract_first(),
            #     'url'   :   torrent.css('a::attr(href)').extract_first(),
            # }
            request = scrapy.Request(response.urljoin(torrent.css('a::attr(href)').extract_first()), callback=self.parse_download_link)
            request.meta['item'] = item

            item['name'] = torrent.css('a::text').extract_first()
            item['url'] = torrent.css('a::attr(href)').extract_first()
            yield request

    def parse_download_link(self, response):
        # yield {
        #     'time'  :   response.css('td.vtop::text').extract_first()
        # }
        item = response.meta['item']
        item['date'] = response.css('td.vtop::text').extract_first()
        yield item
