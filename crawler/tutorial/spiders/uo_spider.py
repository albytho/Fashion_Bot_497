import scrapy


class uospider(scrapy.Spider):
    name = "uo_spider"
    start_urls = [
        #Men
        # 'https://www.urbanoutfitters.com/mens-tops',
        # 'https://www.urbanoutfitters.com/mens-jackets',
        # 'https://www.urbanoutfitters.com/mens-bottoms',
        # 'https://www.urbanoutfitters.com/graphic-tees-for-men',

        #Women
        'https://www.urbanoutfitters.com/dresses',
        'https://www.urbanoutfitters.com/womens-tops',
        'https://www.urbanoutfitters.com/jackets-coats-for-women',
        'https://www.urbanoutfitters.com/womens-bottoms',
        'https://www.urbanoutfitters.com/vintage-womens-clothing',

        
    ]

    def parse(self, response):
        for href in response.css('div.c-product-tile-controls__link-wrap a::attr(href)').extract():
            yield response.follow(href, self.parse_cloth)

    def parse_cloth(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        url = response.request.url
        name = extract_with_css('h1.c-product-meta__h1 span::text')[0].strip()
        price = extract_with_css('span.c-product-meta__current-price::text')[1].strip()
        images = extract_with_css('img.c-product-image::attr(src)')
        images = 'http://{}'.format(images[0][2:])
        
        yield{
            'product_brand': 'Urban Outfitters',
            'product_name': name,
            'price': price,
            'images': images,
            'url': url,
        }
    

    