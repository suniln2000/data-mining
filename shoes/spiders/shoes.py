import scrapy

class ShoesSpider(scrapy.Spider):
    name = 'shoes'

    def start_requests(self):
        base_url = 'https://www.mytheresa.com/int/en/men/shoes?page={}'
        start_page = 1
        end_page = 33

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

    #will handle the detailed product page.
    def parse_shoe_page(self, response):

        cleaned_listing_prices = response.css('.pricing__prices__original .pricing__prices__price::text').getall()
        cleaned_offer_prices = response.css('.pricing__prices__discount .pricing__prices__price::text').getall()


        yield {
            'breadcrumbs': response.css('a.breadcrumb__item__link::text').getall(),
            'image_url': response.css('.product__gallery__carousel__image::attr(src)').get(),
            'brand': response.css('.product__area__branding__designer__link::text').get(),
            'product_name': response.css('.product__area__branding__name::text').get(),
            'listing_prices': [price.strip() for price in cleaned_listing_prices if price.strip()],
            'offer_prices': [price.strip() for price in cleaned_offer_prices if price.strip()],
            'discount': response.css('.pricing__info__percentage::text').getall(),
            'product_id': response.css('.productinfo__pricedescription::text').getall(),
            'sizes': response.css('.sizeitem__label::text').getall(),
            'description': response.css('.accordion__body__content li::text').getall(),
            'other_images': response.css('.product__gallery__carousel__image::attr(src)').getall()
        }