import scrapy
# from scrapy.selector import Selector


class SocialEventVenue(scrapy.Spider):
    name = 'social_event_venue'
    start_urls = ['https://www.mandap.com/ahmedabad/wedding-venues']

    def parse(self, response):
        # hsx = Selector(response)
        for products in response.css('div.list_result'):
            try:
                yield {
                    'name': products.css('div.list_title a h2::text').get(),
                    'location': products.css('div.list_location a::text').get(),
                    "price": products.css('b::text').getall()[1].replace("\u00a0", '')

                }
            except:
                yield
                {
                    'name': products.css('div.list_title a h2::text').get(),
                    'location': 'Ahmedabad',
                    'price': 'Not mentioned',

                }
        next_page = response.css('a.nxt_txt.inactive.pntr').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
