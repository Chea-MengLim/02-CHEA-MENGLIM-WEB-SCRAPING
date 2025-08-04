import time
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LoginAndScrollSpider(scrapy.Spider):
    name = "login_reviews"
    allowed_domains = ["web-scraping.dev"]

    def start_requests(self):
        url = "https://web-scraping.dev/login?cookies="
        yield SeleniumRequest(
            url=url,
            callback=self.after_login,
            wait_time=10,
            wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-content")),
            script="""
                // Accept cookies
                const cookieBtn = document.querySelector("button#cookie-ok");
                if (cookieBtn) cookieBtn.click();

                // Fill in username
                const userInput = document.querySelector("input[name='username']");
                if (userInput) {
                    userInput.value = 'user123';
                    userInput.dispatchEvent(new Event('input', { bubbles: true }));
                }

                // Fill in password
                const passInput = document.querySelector("input[name='password']");
                if (passInput) {
                    passInput.value = 'password';
                    passInput.dispatchEvent(new Event('input', { bubbles: true }));
                }

                // Submit the form properly
                const form = document.querySelector("form");
                if (form) {
                    form.submit();
                } else {
                    // Fallback: click the submit button
                    const loginBtn = document.querySelector("button[type='submit']");
                    if (loginBtn) loginBtn.click();
                }
            """
        )

    def after_login(self, response):
        driver = response.meta["driver"]

        # Wait longer for login to complete and page to redirect
        time.sleep(5)
        current_url = driver.current_url
        print(f"Current URL after login: {current_url}")

        if "login" in current_url:
            print("Login might have failed, still on login page")
            try:
                error_element = driver.find_element(By.CSS_SELECTOR, ".alert, .error, .text-danger")
                print(f"Login error: {error_element.text}")
            except:
                print("No error message found")
            
            # Try to manually navigate to testimonials even if login failed
            print("Attempting to navigate to testimonials page...")
            driver.get("https://web-scraping.dev/testimonials")
            time.sleep(3)
        else:
            print("Login successful, navigating to testimonials...")
            driver.get("https://web-scraping.dev/testimonials")
            time.sleep(3)

        # Scroll to load dynamic content
        for i in range(1, 10):
            ActionChains(driver).scroll_by_amount(0, 10000).perform()
            time.sleep(1)

        WebDriverWait(driver, timeout=60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".testimonial:nth-child(60)"))
        )

        selector = Selector(text=driver.page_source)
        for review in selector.css("div.testimonial"):
            yield {
                "rate": len(review.css("span.rating > svg").getall()),
                "text": review.css("p.text::text").get()
            }


