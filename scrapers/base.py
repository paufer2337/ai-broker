from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import logging

class BaseScraper(ABC):
    def __init__(self, broker):
        self.broker = broker
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Configure logging for this scraper instance
        self.logger = logging.getLogger(f"scraper.{self.__class__.__name__}")
        self.logger.setLevel(logging.INFO)
        
        # Add a file handler if not already present
        if not self.logger.handlers:
            fh = logging.FileHandler(f"logs/{self.__class__.__name__}.log")
            fh.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(fh)
    
    def log_request_start(self, url):
        """Log the start of a request"""
        self.logger.info(f"Starting request to: {url}")
        self.logger.debug(f"Headers: {self.headers}")
    
    def log_request_success(self, url, status_code=None, content_length=None):
        """Log a successful request"""
        msg = f"Successfully accessed: {url}"
        if status_code:
            msg += f" (Status: {status_code})"
        if content_length:
            msg += f" (Content Length: {content_length})"
        self.logger.info(msg)
    
    def log_request_error(self, url, error):
        """Log a request error"""
        self.logger.error(f"Error accessing {url}: {str(error)}")
        if hasattr(error, 'response'):
            self.logger.error(f"Response status code: {error.response.status_code}")
            self.logger.error(f"Response headers: {error.response.headers}")
    
    def log_scraping_progress(self, current, total, success_count):
        """Log scraping progress"""
        self.logger.info(f"Scraped {current}/{total} items. Successfully extracted: {success_count}")
    
    def log_scraping_complete(self, total_items, success_count, time_taken=None):
        """Log scraping completion"""
        msg = f"Scraping complete. Found {total_items} items, successfully extracted {success_count}"
        if time_taken:
            msg += f" (Time taken: {time_taken:.2f}s)"
        self.logger.info(msg)
    
    @abstractmethod
    def scrape(self):
        """
        Scrape job listings from the broker's website.
        Must be implemented by each scraper.
        
        Returns:
            list: List of mission data dictionaries
        """
        pass 