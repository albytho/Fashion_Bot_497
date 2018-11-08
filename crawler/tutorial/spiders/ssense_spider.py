import scrapy


class Ssensespider(scrapy.Spider):
    name = "ssense"
    start_urls = [
        # 'https://www.ssense.com/en-us/men/clothing',
        'https://www.ssense.com/en-us/women/clothing',
    ]

    def parse(self, response):
        print(response.request.url)
        for href in response.css('div.browsing-product-list a::attr(href)').extract():
            yield response.follow(href, self.parse_cloth)

        next_check = response.xpath("//nav[@aria-label='Pagination']/ul/li/a[text()='→']").extract_first()
        next_link = response.xpath("//nav[@aria-label='Pagination']/ul/li/a/@href").extract()[-1]
        if next_check:
            yield response.follow(next_link, self.parse)

    def parse_cloth(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        url = response.request.url
        name = extract_with_css('h2.product-name::text')[0]
        price = response.css('h3.price span.price::text').extract_first()[1:].split(' ')[0]
        images = response.xpath('//img/@data-srcset').extract_first()
        brand = extract_with_css('h1.product-brand a::text')[0]

        yield{
            'product_brand': brand,
            'product_name': name,
            'price': price,
            'images': images,
            'url': url,
        }
    
            