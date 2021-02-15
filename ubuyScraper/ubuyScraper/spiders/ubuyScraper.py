import scrapy
from .. items import UbuyscraperItem

class UbuyScraper(scrapy.Spider):
    name = 'ubuy'
    start_urls = ['https://www.ubuy.ae/en/']

    def parse(self, response):
        category = response.xpath('//a[@class="cat-img"]/@href')
        #print(category)

        for i in category:
            yield scrapy.Request(i.extract(), callback = self.parse_pages)

    def parse_pages(self, response):
        items = UbuyscraperItem()
        pro_container = response.css('div.product-body')

        for i in pro_container:
            pro_name = i.css('h3.product-name a::text').extract()
            pro_price = i.css('h4.product-price::text').extract()
            #print(pro_name, pro_price)
            for j in zip(pro_name, pro_price):
                items['name'] = j[0].strip()
                items['price'] = j[1].strip()
                #print(name, price)
                yield items
        
            