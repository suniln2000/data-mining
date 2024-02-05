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
        # represent individual shoes on the webpage
        shoes = response.css('.item--sale')

        #extracts the URL of each shoe's product page
        for shoe in shoes:
            product_url = shoe.css('a.item__link::attr(href)').get()
            #after following the link, it handle the new response.
            yield response.follow(product_url, callback=self.parse_shoe_page)