from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import logging

class BaseScraper(ABC):
    def __init__(self, broker):
        self.broker = broker
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    @abstractmethod
    def scrape(self):
        """Each broker scraper must implement this method"""
        pass 