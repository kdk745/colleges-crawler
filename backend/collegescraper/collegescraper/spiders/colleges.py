import scrapy
import os
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class CollegesSpider(scrapy.Spider):
    name = 'colleges'
    start_urls = ['https://bigfuture.collegeboard.org/college-search/filters']

    def __init__(self, *args, **kwargs):
        super(CollegesSpider, self).__init__(*args, **kwargs)

        environment = os.getenv('ENVIRONMENT', 'development')
        
        # specify chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        if environment == 'production':
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.binary_location = '/app/.apt/opt/google/chrome/chrome'

            chromedriver_path = '/app/.chromedriver/bin/chromedriver'
            driver_service = Service(chromedriver_path)
            self.driver = webdriver.Chrome(service=driver_service, options=chrome_options)
        else:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)

        previous_length = 0
        # Click "Show More Colleges" button until no more appear
        for i in range(10):
            try:
                show_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Show More Colleges"]'))
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
                self.driver.execute_script("arguments[0].click();", show_more_button)

                # Check if new content has been added
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.page_source) > previous_length
                )

                previous_length = len(self.driver.page_source)
            except Exception as e:
                self.logger.error(f"Exception occurred: {e}")
                break

        # Extract data-card-link from all loaded college elements
        html = self.driver.page_source
        response_obj = scrapy.Selector(text=html)
        college_links = response_obj.css('a.cs-college-card-college-name-link::attr(href)').getall()

        for link in college_links:
            yield scrapy.Request(url=link, callback=self.parse_college)

    def parse_college(self, response):
        try:
            # Extract data from the college page
            school_name = response.css('h1::text').get(default='').strip()
            location = response.css('div[data-testid="csp-banner-section-school-location-label"]::text').get()
            college_board_code = response.css('div[data-testid="csp-more-about-college-board-code-valueId"]::text').get()

            # Parse location into city and state
            if location:
                location_parts = location.split(', ')
                school_city = location_parts[0] if len(location_parts) > 0 else None
                school_state = location_parts[1] if len(location_parts) > 1 else None
            else:
                school_city, school_state = None, None

            # Handle college board code if "Not Available"
            if college_board_code == "Not available":
                college_board_code = None

            # Build the school item and yield it as output
            item = {
                'school_name': school_name,
                'school_city': school_city,
                'school_state': school_state,
                'college_board_code': college_board_code,
            }

            self.logger.info(f"CollegesSpider: Yielding item: {item}")
            yield item

        except Exception as e:
            self.logger.error(f"Error parsing college page: {e}")

    def closed(self, reason):
        self.driver.quit()

if __name__ == "__main__":
    # this will output the items as a list to the output.json file (for debugging purposes)
    process = CrawlerProcess()
    process.crawl(CollegesSpider)
    process.start()
