import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class CollegesSpider(scrapy.Spider):
    name = 'colleges'
    start_urls = ['https://bigfuture.collegeboard.org/college-search/filters'] 

    def __init__(self, *args, **kwargs):
        super(CollegesSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(1)

        previous_length = 0
        # Click "Show More Colleges" button until no more appear
        # For the sake of time, I have modified this to only click this buttom 10 times
        # If we actually wanted to pull every single college, then change the for loop line to while True:
        for i in range(10):
            try:
                show_more_button = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Show More Colleges"]')
                self.driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
                self.driver.execute_script("arguments[0].click();", show_more_button)
                time.sleep(0.5)  # Wait for new content to load

                # Check if new content has been added
                current_length = len(self.driver.page_source)
                if current_length == previous_length:
                    break
                previous_length = current_length
            except Exception as e:
                self.logger.error(f"Exception occured: {e}")
                break

        # Extract data-card-link from all loaded college elements
        html = self.driver.page_source
        response_obj = scrapy.Selector(text=html)
        college_links = response_obj.css('a.cs-college-card-college-name-link::attr(href)').getall()

        for link in college_links:
            yield scrapy.Request(url=link, callback=self.parse_college)

    def parse_college(self, response):
        # Extract data from the college page
        school_name = response.css('h1::text').get().strip()
        location = response.css('div[data-testid="csp-banner-section-school-location-label"]::text').get()
        college_board_code = response.css('div[data-testid="csp-more-about-college-board-code-valueId"]::text').get()

        if location:
            school_city, school_state = location.split(', ')
        else:
            school_city, school_state = None, None

        if college_board_code == "Not available":
            college_board_code = None

        # build the school item and yield it as output
        item = {
            'school_name': school_name,
            'school_city': school_city,
            'school_state': school_state,
            'college_board_code': college_board_code,
        }

        self.logger.info(f"CollegesSpider: Yielding item: {item}")

        yield item
        

    def closed(self, reason):
        self.driver.quit()

if __name__ == "__main__":
    # this will output the items as a list to the output.json file (for debugging purposes)
    process = CrawlerProcess(settings={
        "FEEDS": {
            "output.json": {"format": "json"},
        },
    })
    process.crawl(CollegesSpider)
    process.start()
