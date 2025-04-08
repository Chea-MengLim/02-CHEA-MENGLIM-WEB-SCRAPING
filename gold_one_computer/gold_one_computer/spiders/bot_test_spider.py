import scrapy

class AmazonStealthSpider(scrapy.Spider):
    name = 'amazon_stealth'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?k=laptop']

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'DNT': '1',  # Do Not Track header
            'Connection': 'keep-alive',
            # User-Agent is set by middleware
        }

        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        if response.status != 200 or "captcha" in response.text.lower():
            self.logger.warning("🚫 BLOCKED by Amazon!")
            return

        for product in response.css('div.s-result-item'):
            title = product.css('h2 span::text').get()
            price = product.css('span.a-price > span.a-offscreen::text').get()
            if title:
                yield {
                    'title': title.strip(),
                    'price': price.strip() if price else None,
                    'url': response.url
                }

        # Pagination
        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
