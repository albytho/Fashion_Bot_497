import scrapy


class Oldnavyspider(scrapy.Spider):
    name = "oldnavy_spider"
    start_urls = [
        'http://oldnavy.gap.com/browse/category.do?cid=26061&sop=true&mlink=5155,13518818,flyout_m_SALE&clink=13518818',
        # 'http://oldnavy.gap.com/browse/category.do?cid=5249&sop=true&mlink=26061,13518818,flyout_m_Tee_Shop&clink=13518818',
        # 'http://oldnavy.gap.com/browse/category.do?cid=5271&sop=true&mlink=5249,13518818,flyout_m_Graphic_Tees&clink=13518818',
        # 'http://oldnavy.gap.com/browse/category.do?cid=1010005&sop=true&mlink=5271,13518818,flyout_m_Shirts_&clink=13518818',
        # 'http://oldnavy.gap.com/browse/category.do?cid=5256&sop=true&mlink=1010005,13518818,flyout_m_Polos&clink=13518818',
        # 'http://oldnavy.gap.com/browse/category.do?cid=1016048&sop=true&mlink=5256,13518818,flyout_m_Fleece_Hoodies&clink=13518818',
        # 'http://oldnavy.gap.com/browse/category.do?cid=72305&sop=true&mlink=1016048,13518818,flyout_m_Jackets_Outerwear&clink=13518818',
        # 'http://oldnavy.gap.com/browse/category.do?cid=63315&sop=true&mlink=72305,13518818,flyout_m_Sweaters&clink=13518818',
        # 'http://oldnavy.gap.com/browse/category.do?cid=5226&sop=true&mlink=63315,13518818,flyout_m_Shorts&clink=13518818',
        # 'http://oldnavy.gap.com/browse/category.do?cid=5211&sop=true&mlink=5226,13518818,flyout_m_Pants&clink=13518818',

    ]

    def parse(self, response):
        for href in response.css('div.sp_sm a::attr(href)').extract():
            yield response.follow('http://oldnavy.gap.com/{}'.format(href), self.parse_cloth) 

    def parse_cloth(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        print("HELLO")
        price = response.css('h5.product-price::text').extract_first().strip()
        images = 'http://oldnavy.gap.com/{}'.format(extract_with_css('img::attr(src)')[1])
        yield{
            'product_brand': "Old Navy",
            'product_name': response.css('h1.product-title::text').extract_first().strip(),
            'price': price,
            'images': images
        }
    
            