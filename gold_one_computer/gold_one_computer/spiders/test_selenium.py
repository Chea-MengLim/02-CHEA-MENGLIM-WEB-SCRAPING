import time
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["web-scraping.dev"]

    def start_requests(self):
        url = "https://web-scraping.dev/testimonials"
        yield SeleniumRequest(
            url=url,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.request.meta["driver"]

        for i in range(1, 10):
            ActionChains(driver).scroll_by_amount(0, 10000).perform()
            time.sleep(1)
            
        wait = WebDriverWait(driver, timeout=60)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".testimonial:nth-child(60)")))

        # get the HTML from the actual driver
        selector = Selector(text=driver.page_source)
        for review in selector.css("div.testimonial"):
            yield {
                "rate": len(review.css("span.rating > svg").getall()),
                "text": review.css("p.text::text").get()
            }