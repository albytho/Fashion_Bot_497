import scrapy


class Macyspider(scrapy.Spider):
    name = "macy_spider"
    start_urls = [
        #Men
        'https://www.macys.com/shop/mens-clothing/sale-clearance?id=9559&edge=hybrid',
        'https://www.macys.com/shop/mens-clothing/mens-dress-shirts?id=20635&edge=hybrid',
        'https://www.macys.com/shop/mens-clothing/basics?id=134585&cm_sp=us_hdr-_-men-_-134585_basics_COL1',
        'https://www.macys.com/shop/mens-clothing/mens-blazers-sports-coats?id=16499&cm_sp=us_hdr-_-men-_-16499_blazers-%26-sport-coats_COL1',
        'https://www.macys.com/shop/mens-clothing/mens-jackets-coats?id=3763&cm_sp=us_hdr-_-men-_-3763_coats-%26-jackets_COL1',
        'https://www.macys.com/shop/mens-clothing/hoodies-for-men?id=25995&cm_sp=us_hdr-_-men-_-25995_hoodies-%26-sweatshirts_COL1',
        'https://www.macys.com/shop/mens-clothing/mens-pants?id=89&cm_sp=us_hdr-_-men-_-89_pants_COL1',
        'https://www.macys.com/shop/mens-clothing/mens-polo-shirts?id=20640&cm_sp=us_hdr-_-men-_-20640_polos_COL1',
        'https://www.macys.com/shop/mens-clothing/mens-suits?id=17788&cm_sp=us_hdr-_-men-_-17788_suits-%26-tuxedos_COL1',
        'https://www.macys.com/shop/mens-clothing/mens-sweaters?id=4286&cm_sp=us_hdr-_-men-_-4286_sweaters_COL1',

        #Women
        # 'https://www.macys.com/shop/womens-clothing/womens-sale-clearance?id=10066&cm_sp=us_hdr-_-women-_-10066_sale-%26-clearance_COL4',
        # 'https://www.macys.com/shop/womens-clothing/womens-activewear?id=29891&cm_sp=us_hdr-_-women-_-29891_activewear_COL1',
        # 'https://www.macys.com/shop/womens-clothing/basic-clothing?id=135942&cm_sp=us_hdr-_-women-_-135942_basics_COL1',
        # 'https://www.macys.com/shop/womens-clothing/womens-blazers?id=55429&cm_sp=us_hdr-_-women-_-55429_blazers_COL1',
        # 'https://www.macys.com/shop/womens-clothing/womens-coats?id=269&cm_sp=us_hdr-_-women-_-269_coats_COL1',
        # 'https://www.macys.com/shop/womens-clothing/dresses?id=5449&cm_sp=us_hdr-_-women-_-5449_dresses_COL1',
        # 'https://www.macys.com/shop/womens-clothing/womens-jackets?id=120&cm_sp=us_hdr-_-women-_-120_jackets_COL1',
        # 'https://www.macys.com/shop/womens-clothing/womens-jeans?id=3111&cm_sp=us_hdr-_-women-_-3111_jeans_COL1',
        # 'https://www.macys.com/shop/womens-clothing/womens-jumpsuits-rompers?id=50684&cm_sp=us_hdr-_-women-_-50684_jumpsuits-%26-rompers_COL1',
        # 'https://www.macys.com/shop/womens-clothing/leggings?id=46905&cm_sp=us_hdr-_-women-_-46905_leggings_COL1',
        # 'https://www.macys.com/shop/womens-clothing/womens-shorts?id=5344&cm_sp=us_hdr-_-women-_-5344_shorts_COL1',
        # 'https://www.macys.com/shop/womens-clothing/womens-skirts?id=131&cm_sp=us_hdr-_-women-_-131_skirts_COL1',
        # 'https://www.macys.com/shop/womens-clothing/womens-sweaters?id=260&cm_sp=us_hdr-_-women-_-260_sweaters_COL1',


    ]

    def parse(self, response):
        for product in response.css('div.productThumbnail'):
            def extract_with_css(query):
                return product.css(query).extract()

            price = product.css('div.prices span::text').extract_first().strip()
            images = product.css('img::attr(src)').extract_first()
            url = "https://www.macys.com" + product.css('div.productDescription a::attr(href)').extract_first()
            yield{
                'product_brand': "Macys",
                'product_name': product.css('div.productDescription a::attr(title)').extract_first(),
                'price': price[1:],
                'images': images,
                'url': url
            }
    