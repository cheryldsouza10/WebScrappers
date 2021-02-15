import scrapy 
from .. items import MallofemiratesItem

class ItemList(scrapy.Spider):
    name = 'new'
    start_urls =['https://www.malloftheemirates.com']

    def parse(self, response):

        cate = response.xpath('//ul[@class="content"]/li/a/@href')
        #yield {'category': cate}

        for j in cate:
            url = response.urljoin(j.extract())
            yield scrapy.Request(url, callback = self.parse_contents)
    
    def parse_contents(self, response):
        items = MallofemiratesItem()
        all = response.css('section.grid-7')
        # yield {'items': all}
        for i in all:
            title = i.css('div.storebox')

            for j in title:
                items['name'] = j.css('ul.storetitle li a::text').extract()
                items['phone'] = j.css('ul.storewidgets li a span.phoneno::text').extract()
                
                yield items
                


