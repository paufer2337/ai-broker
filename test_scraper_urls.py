import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# URLs to test
URLS = {
    'WiseIT': 'https://getwiser.se/lediga-uppdrag',
    'DFindIT': 'https://www.dfind.se/it/lediga-jobb',
    'Academic Work': 'https://www.academicwork.se/lediga-jobb',
    'Ework Group': 'https://app.verama.com/en/job-requests'
}

def test_url_requests(url):
    """Test URL using requests library"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        logging.info(f"Request status code: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Request error: {str(e)}")
        return False

def test_url_selenium(url):
    """Test URL using Selenium"""
    driver = None
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Set page load timeout
        driver.set_page_load_timeout(20)
        
        # Try to load the page
        logging.info(f"Attempting to load {url} with Selenium...")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(5)
        
        # Get page title as verification
        title = driver.title
        logging.info(f"Page title: {title}")
        
        return True
    except Exception as e:
        logging.error(f"Selenium error: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()

def main():
    logging.info("Starting URL tests...")
    
    results = {}
    for name, url in URLS.items():
        logging.info(f"\nTesting {name} ({url})")
        logging.info("-" * 50)
        
        # Test with requests
        logging.info(f"Testing with requests...")
        requests_success = test_url_requests(url)
        
        # Test with Selenium
        logging.info(f"Testing with Selenium...")
        selenium_success = test_url_selenium(url)
        
        results[name] = {
            'url': url,
            'requests_success': requests_success,
            'selenium_success': selenium_success
        }
    
    # Print summary
    logging.info("\nTest Results Summary:")
    logging.info("=" * 50)
    for name, result in results.items():
        logging.info(f"\n{name}:")
        logging.info(f"URL: {result['url']}")
        logging.info(f"Requests Test: {'✓' if result['requests_success'] else '✗'}")
        logging.info(f"Selenium Test: {'✓' if result['selenium_success'] else '✗'}")

if __name__ == "__main__":
    main() 