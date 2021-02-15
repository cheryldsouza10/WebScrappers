import scrapy
from .. items import JumboscrapyItem

class Jumbo(scrapy.Spider):
    name = 'jumbo'
    start_urls = [
        'https://www.jumbo.ae/'
    ]

    def parse(self, response):
        category = response.xpath('//li[@class = "dropdown"]/a/@href')
        #print(category)

        for cat in category:
            if cat.extract() == '/':
                continue
            url = response.urljoin(cat.extract())
            #print(url)
            yield scrapy.Request(url, callback = self.parse_pages)

    def parse_pages(self, response):
        items = JumboscrapyItem()
        data = response.css('ul.grid-view li div.variant-wrapper')
        #print(data)
        for i in data:
            title = i.css('div.variant-desc span.variant-title a::text').extract()
            #print(title)
            price = i.css('span.variant-final-price span.m-w::text').extract()
            #print(price)
            items['product_name'] = title
            items['product_price'] = price
            yield items

    
        page_url = response.xpath('//div[@class = "pagination"]/a[@class = "next_page"]/@href')
        proper_url = response.urljoin(page_url[0].extract())
        print(proper_url)
        yield response.follow(proper_url, self.parse_pages)

        