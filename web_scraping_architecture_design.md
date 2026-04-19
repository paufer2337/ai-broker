# Web Scraping Architecture Design for AI-Broker

## Overview

Based on the examination of the existing codebase, I'll design a web scraping architecture that integrates seamlessly with the current system while adding support for additional broker websites. The design will follow the established patterns and extend the functionality to scrape mission data from multiple broker sites without requiring authentication.

## Current Architecture

The existing architecture consists of:

1. **BaseScraper (abstract class)**: Defines the interface for all broker scrapers
2. **ScraperManager**: Manages broker-specific scraper selection and mission updates
3. **Broker-specific scrapers**: Implementations for specific broker websites (WiseITScraper, ExperisScraper)
4. **SCRAPER_MAP**: Maps broker names to scraper classes

## Design Goals

1. Maintain compatibility with the existing architecture
2. Add support for additional broker websites that don't require authentication
3. Ensure robust error handling and rate limiting
4. Standardize mission data extraction
5. Provide a flexible framework for future additions

## Broker Website Analysis

I'll analyze several broker websites to determine:
- URL structure for mission listings
- HTML structure and CSS selectors for mission data
- Pagination mechanisms
- Any AJAX/JavaScript requirements
- Rate limiting considerations

## Implementation Strategy

### 1. Extend SCRAPER_MAP

Update the `__init__.py` file to include new broker scrapers:

```python
from .wise_it import WiseITScraper
from .experis import ExperisScraper
from .new_broker1 import NewBroker1Scraper
from .new_broker2 import NewBroker2Scraper
# Add more imports as needed

SCRAPER_MAP = {
    'wise it': WiseITScraper,
    'experis': ExperisScraper,
    'new_broker1': NewBroker1Scraper,
    'new_broker2': NewBroker2Scraper,
    # Add more mappings as needed
}
```

### 2. Implement New Broker Scrapers

Create new scraper classes for each broker website, following either the requests-based pattern (like ExperisScraper) or the Selenium-based pattern (like WiseITScraper) depending on the website's complexity:

#### Requests-based Pattern (for simpler websites)

```python
from ..base import BaseScraper
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

class SimpleWebsiteScraper(BaseScraper):
    def __init__(self, broker):
        super().__init__(broker)
        self.base_url = "https://example.com/jobs"
        self.rate_limit = 3  # seconds between requests
        
    def scrape(self):
        missions = []
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            mission_elements = soup.select('.job-listing')
            
            for element in mission_elements:
                try:
                    mission_data = {
                        'title': element.select_one('.job-title').text.strip(),
                        'description': element.select_one('.job-description').text.strip(),
                        'location': element.select_one('.job-location').text.strip(),
                        'required_skills': element.select_one('.job-skills').text.strip(),
                        'broker_id': self.broker.id,
                        'posted_date': datetime.utcnow(),
                        'status': 'active'
                    }
                    missions.append(mission_data)
                except Exception as e:
                    logging.error(f"Error parsing mission: {str(e)}")
                    continue
                    
            return missions
        except Exception as e:
            logging.error(f"Error scraping {self.base_url}: {str(e)}")
            return []
```

#### Selenium-based Pattern (for complex websites with JavaScript)

```python
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

class ComplexWebsiteScraper(BaseScraper):
    def __init__(self, broker):
        super().__init__(broker)
        self.base_url = "https://example.com/jobs"
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
                    time.sleep(self.rate_limit)
                    
                    # Wait for content to load
                    mission_wrapper = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "job-listings"))
                    )
                    
                    # Find all mission elements
                    mission_elements = driver.find_elements(By.CLASS_NAME, "job-card")
                    logging.info(f"Found {len(mission_elements)} missions")
                    
                    for element in mission_elements:
                        try:
                            mission_data = {
                                'title': element.find_element(By.CLASS_NAME, "job-title").text.strip(),
                                'description': element.find_element(By.CLASS_NAME, "job-description").text.strip(),
                                'location': element.find_element(By.CLASS_NAME, "job-location").text.strip(),
                                'required_skills': element.find_element(By.CLASS_NAME, "job-skills").text.strip(),
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
```

### 3. Standardize Mission Data Structure

Ensure all scrapers return mission data in a consistent format that matches the Mission model:

```python
mission_data = {
    'title': str,                # Mission title
    'description': str,          # Mission description
    'location': str,             # Mission location
    'required_skills': str,      # Required skills (comma-separated)
    'broker_id': int,            # Broker ID
    'posted_date': datetime,     # Posted date
    'status': str,               # Status (active, closed, etc.)
    'start_date': datetime,      # Optional: Start date
    'duration': str,             # Optional: Duration
    'rate': str                  # Optional: Rate
}
```

### 4. Implement Pagination Support

For websites with paginated results, add pagination support:

```python
def scrape_with_pagination(self, max_pages=5):
    all_missions = []
    
    for page in range(1, max_pages + 1):
        url = f"{self.base_url}?page={page}"
        # Scrape the page
        missions = self.scrape_page(url)
        
        if not missions:
            break  # No more results
            
        all_missions.extend(missions)
        
    return all_missions
```

### 5. Add Rate Limiting and Error Handling

Ensure all scrapers implement proper rate limiting and error handling:

```python
def scrape_with_rate_limit(self, url):
    try:
        # Implement rate limiting
        time.sleep(self.rate_limit)
        
        # Make the request
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {str(e)}")
        return None
```

## Specific Broker Implementations

Based on the existing codebase and common broker websites, I'll implement scrapers for the following broker websites (without authentication):

1. **Experis** (complete the existing implementation)
2. **Academic Work**
3. **Ework Group**
4. **Dfind IT**
5. **Randstad**

Each implementation will follow either the requests-based or Selenium-based pattern depending on the website's complexity.

## Testing Strategy

For each scraper implementation:

1. Test basic connectivity to the website
2. Test parsing of mission data
3. Test error handling and retries
4. Test rate limiting
5. Test integration with the ScraperManager

## Deployment Strategy

1. Implement one scraper at a time
2. Test thoroughly before moving to the next
3. Update the SCRAPER_MAP as each scraper is completed
4. Integrate with the existing system

## Future Enhancements

1. Add support for authenticated broker websites
2. Implement more sophisticated rate limiting
3. Add support for proxy rotation
4. Implement more robust error handling and logging
5. Add support for scheduled scraping
