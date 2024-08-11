import json

import scrapy


class MySpider(scrapy.Spider):
    name = "mySpider"
    allowed_domains = ["goldonecomputer.com"]
    start_urls = ["https://www.goldonecomputer.com/index.php?route=common/home"]

    def __init__(self):
        self.data = []

    def parse(self, response):
        # Select the container with the specified class
        headers_li = response.css("ul.dropmenu > li.top_level.dropdown")
        headers = {}
        # Iterate through each headers_li
        for header in headers_li:
            # Select all 'a' tags inside the 'li.top_level' elements
            link = header.css("li.top_level.dropdown > a.activSub::attr(href)").extract_first()
            title = header.css("li.top_level.dropdown > a.activSub::text").extract_first()
            headers[title] = link

        # Follow each link
        for title, link in headers.items():
            yield scrapy.Request(url=link, callback=self.parse_category, meta={'category_title': title})

    def parse_category(self, response):
        category_title = response.meta['category_title']
        # Select all 'div' elements with class 'image'
        image_divs = response.css("div.product-layout > div.product-block > div.product-block-inner > div.image")
        # Iterate through each 'div.image' element
        for image_div in image_divs:
            # Extract the 'href' attribute from the 'a' tag within the 'div.image'
            link = image_div.css("a::attr(href)").get()
            pro_img = image_div.css("a > img::attr(src)").get()
            yield scrapy.Request(url=link, callback=self.parse_product, meta={'category_title': category_title,
                                                                              'product_image': pro_img})

    def parse_product(self, response):
        category_title = response.meta['category_title']
        product_image = response.meta['product_image']
        brand = response.css(
            "#content > div.row > div.col-sm-6.product-right > ul:nth-child(3) > li:nth-child(1) > a::text").get()
        product_name = response.xpath("//*[@id='content']/div[1]/div[2]/h3/text()").get()
        product_code = response.xpath("//li[span[@class='desc']]/text()").get()
        review_count = response.xpath("//*[@id='content']/div[1]/div[2]/div[1]/a[1]/text()").get().split(" ")[0]

        # handle dynamic ui. product with discount is different UI from product does not have discount.
        # We use if, else to avoid None price
        if response.xpath("//*[@id='content']/div[1]/div[2]/ul[2]/li[2]/h3/text()").get() is not None:
            final_price = response.xpath("//*[@id='content']/div[1]/div[2]/ul[2]/li[2]/h3/text()").get()
        else:
            final_price = response.xpath("//*[@id='content']/div[1]/div[2]/ul[2]/li/h3/text()").get()

        obj = {
            'category_title': category_title,
            'product': {
                'product_name': product_name,
                'final_price': final_price,
                'brand': brand,
                'product_code': product_code,
                'product_image': product_image,
                'review_count': review_count,
            }
        }

        self.data.append(obj)

    def closed(self, reason):
        # When the spider finishes, write all collected data to a JSON file
        file_name = 'data.json'
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(self.data, json_file, ensure_ascii=False, indent=4)
        print(f"Data has been saved successfully to {file_name}")