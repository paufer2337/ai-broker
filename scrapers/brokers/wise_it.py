from ..base import BaseScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime
import time

class WiseITScraper(BaseScraper):
    def __init__(self, broker):
        super().__init__(broker)
        self.base_url = "https://getwiser.se/lediga-uppdrag"
        self.rate_limit = 2  # seconds between requests
        self.max_retries = 3

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def scrape(self):
        driver = None
        retry_count = 0
        missions = []

        try:
            while retry_count < self.max_retries:
                try:
                    driver = self.setup_driver()
                    logging.info(f"Scraping {self.base_url}")
                    
                    # Load the page
                    driver.get(self.base_url)
                    time.sleep(self.rate_limit)  # Initial wait for page load
                    
                    # Wait for content to load
                    mission_wrapper = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "article_summary_widget_wrapper"))
                    )
                    
                    # Scroll to load all missions
                    last_height = driver.execute_script("return document.body.scrollHeight")
                    while True:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        new_height = driver.execute_script("return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height
                    
                    # Find all mission elements
                    mission_elements = driver.find_elements(By.CLASS_NAME, "article_summary_widget_wrapper")
                    logging.info(f"Found {len(mission_elements)} missions")
                    
                    for element in mission_elements:
                        try:
                            mission_data = {
                                'title': element.find_element(By.TAG_NAME, "h3").text.strip(),
                                'description': element.find_element(By.CLASS_NAME, "description").text.strip(),
                                'location': element.find_element(By.CLASS_NAME, "location").text.strip(),
                                'required_skills': element.find_element(By.CLASS_NAME, "skills").text.strip(),
                                'broker_id': self.broker.id,
                                'posted_date': datetime.utcnow(),
                                'status': 'active'
                            }
                            missions.append(mission_data)
                            
                        except NoSuchElementException as e:
                            logging.error(f"Missing element in mission card: {str(e)}")
                            continue
                    
                    break  # Success, exit retry loop
                    
                except TimeoutException:
                    retry_count += 1
                    logging.warning(f"Timeout, attempt {retry_count} of {self.max_retries}")
                    if driver:
                        driver.quit()
                    time.sleep(self.rate_limit * 2)  # Wait longer between retries
                    
                except Exception as e:
                    logging.error(f"Unexpected error: {str(e)}")
                    break
                    
        finally:
            if driver:
                driver.quit()
                
        return missions 