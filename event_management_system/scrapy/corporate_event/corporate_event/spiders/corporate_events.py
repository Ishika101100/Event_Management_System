import scrapy
from scrapy.selector import Selector


class SocialEventVenue(scrapy.Spider):
    name = 'corporate_event_venue'
    start_urls = ['https://www.weddingwire.in/busc.php?id_grupo=1&id_provincia=10010307&id_region=9639&id_sector=44']

    def parse(self, response):
        # hsx = Selector(response)
        for products in response.css('div.vendorTile__content'):
            try:
                yield {
                    'name': products.css('div.vendorTile__content h2 a::text').get(),
                    'location': products.css('span.vendorTile__location::text').get()[3:],
                    'price': response.css('div.vendorTileFooter__info::text').getall()[1].replace("0","00").replace("From ₹","").strip()
                }
            except:
                yield
                {
                    'name': 'Not Mentioned',
                    'location': 'Not Mentioned',
                    'price': 'Not Mentioned'

                }
        next_page = response.css('button.button.button--block.button--tertiary').attrib['data-href']
        print("next_page---->", next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
