import scrapy

class ShoesSpider(scrapy.Spider):
    name = 'shoes'

    def start_requests(self):
        base_url = 'https://www.mytheresa.com/int/en/men/shoes?page={}'
        start_page = 1
        end_page = 3

        for page in range(start_page, end_page + 1):
            url = base_url.format(page)
            yield scrapy.Request(url, callback=self.parse)

    #to handle the HTTP response
    def parse(self, response):