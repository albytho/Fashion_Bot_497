import scrapy


class uniqlospider(scrapy.Spider):
    name = "uniqlo"
    start_urls = [
        'https://www.uniqlo.com/us/en/men/outerwear-and-blazers',
        'https://www.uniqlo.com/us/en/men/sweatshirts-and-sweatpants',
        'https://www.uniqlo.com/us/en/men/sweaters',
        'https://www.uniqlo.com/us/en/men/casual-shirts',
        'https://www.uniqlo.com/us/en/men/dress-shirts',
        'https://www.uniqlo.com/us/en/men/t-shirts-and-polos',
        'https://www.uniqlo.com/us/en/men/jeans',
        'https://www.uniqlo.com/us/en/men/pants-and-shorts',
        'https://www.uniqlo.com/us/en/men/chino-pants',
        'https://www.uniqlo.com/us/en/men/socks-and-tights',
    ]
    # start_urls = [
    #     'https://www.uniqlo.com/us/en/women/outerwear-and-blazers',
    #     'https://www.uniqlo.com/us/en/women/sweatshirts-and-sweatpants',
    #     'https://www.uniqlo.com/us/en/women/sweaters-and-cardigans',
    #     'https://www.uniqlo.com/us/en/women/shirts-and-blouses',
    #     'https://www.uniqlo.com/us/en/women/t-shirts-and-tops',
    #     'https://www.uniqlo.com/us/en/women/jeans',
    #     'https://www.uniqlo.com/us/en/women/pants-and-shorts',
    #     'https://www.uniqlo.com/us/en/women/leggings-pants',
    #     'https://www.uniqlo.com/us/en/women/skirts',
    #     'https://www.uniqlo.com/us/en/women/dresses-and-jumpsuits',
    #     'https://www.uniqlo.com/us/en/women/socks-and-hosiery',
    # ]

    def parse(self, response):
        for href in response.css('div.product-image a::attr(href)').extract():
            yield response.follow(href, self.parse_cloth)

    def parse_cloth(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        url = response.request.url
        name = extract_with_css('span.product-name::text')[0]
        price = extract_with_css('span.pdp-space-price::text')[0]
        images = extract_with_css('a.main-image img::attr(src)')[0]
        
        yield{
            'product_brand': 'uniqlo',
            'product_name': name,
            'price': price,
            'images': images,
            'url': url,
        }
    
            