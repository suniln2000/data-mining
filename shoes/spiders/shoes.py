import scrapy

class ShoesSpider(scrapy.Spider):
    name = 'shoes'

    def start_requests(self):
        base_url = 'https://www.mytheresa.com/int/en/men/shoes?page={}'
        start_page = 1
        end_page = 3