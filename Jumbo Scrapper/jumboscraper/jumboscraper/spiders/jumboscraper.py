import scrapy 
from .. items import JumboscraperItem

class JumboScraper(scrapy.Spider):
    name = 'jumbo'
    start_urls =[
        'https://www.jumbo.ae/'
    ]

    def parse(self, response):
        items = JumboscraperItem()

        all_div = response.css('div.variant-desc')

        for product in all_div:
            products = product.css('span.variant-title a::text').extract()
            price = product.css('span.m-w::text').extract()

            items['price'] = price
            items['products'] = products
            
            yield items