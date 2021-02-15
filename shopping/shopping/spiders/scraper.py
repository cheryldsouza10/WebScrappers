import scrapy
from ..items import ShoppingItem

class trial(scrapy.Spider):
    name = 'shopping'
    start_urls = ['https://www.shoppinginformer.com/stores/mall%20of%20emirates/']


    def parse(self, response):
        category = response.xpath('//div[@class="navmenuitem"]/a/@href')
        for i in category:
            url = response.urljoin(i.extract())
            yield scrapy.Request(url, callback = self.parse_pages)

    def parse_pages(self, response):
        items = ShoppingItem()

        all_items = response.css("div.store-ListBlock")
        for i in all_items:
            title = i.css('h3.ListH::text').extract()
            desc = i.css('p.Listsmalldesc::text').extract()

            for j in zip(title, desc):
                items['Title'] = j[0].strip()
                items['Description'] = j[1].strip()

                yield items