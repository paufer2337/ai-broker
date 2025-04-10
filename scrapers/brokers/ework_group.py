"""
Ework Group Scraper

This module implements a scraper for Ework Group job listings.
It extracts mission data from the Ework Verama platform without requiring authentication.
"""

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
import re

class EworkGroupScraper(BaseScraper):
    """
    Scraper for Ework Group job listings.
    
    This scraper uses Selenium to navigate the Ework Verama platform and extract job listings.
    It handles pagination and extracts detailed information about each job.
    """
    
    def __init__(self, broker):
        """
        Initialize the Ework Group scraper.
        
        Args:
            broker: The broker object containing information about the broker.
        """
        super().__init__(broker)
        self.base_url = "https://app.verama.com/en/job-requests"
        self.rate_limit = 2  # seconds between requests
        self.max_retries = 3
        self.max_pages = 5  # Maximum number of pages to scrape
    
    def setup_driver(self):
        """
        Set up the Selenium WebDriver with appropriate options.
        
        Returns:
            WebDriver: Configured Chrome WebDriver instance.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    
    def extract_job_details(self, element):
        """
        Extract job details from a job listing element.
        
        Args:
            element: The WebElement containing the job listing.
            
        Returns:
            dict: Dictionary containing job details.
        """
        try:
            # Extract job title and ID
            title_text = element.find_element(By.CSS_SELECTOR, "h3").text.strip()
            # The title often contains the job ID in the format "Title - JR-XXXXX"
            title_parts = title_text.split("JR-")
            title = title_parts[0].strip()
            job_id = "JR-" + title_parts[1].split()[0] if len(title_parts) > 1 else ""
            
            # Extract company
            company_element = element.find_element(By.CSS_SELECTOR, "span:nth-child(2)")
            company = company_element.text.strip() if company_element else ""
            
            # Extract location
            location_element = element.find_element(By.CSS_SELECTOR, "span:nth-child(3)")
            location = location_element.text.strip() if location_element else ""
            
            # Extract posting time
            time_element = element.find_element(By.CSS_SELECTOR, "span.time")
            posted_time = time_element.text.strip() if time_element else ""
            
            # Get the job URL
            job_url_element = element.find_element(By.CSS_SELECTOR, "a")
            job_url = job_url_element.get_attribute("href") if job_url_element else ""
            
            # Combine all information into a description
            description = f"Position: {title}\n"
            if job_id:
                description += f"Job ID: {job_id}\n"
            description += f"Company: {company}\n"
            description += f"Location: {location}\n"
            description += f"Posted: {posted_time}\n"
            description += f"URL: {job_url}\n"
            
            # Extract skills from the title
            skills = self.extract_skills(title)
            
            # Create mission data dictionary
            mission_data = {
                'title': title,
                'description': description,
                'location': location,
                'required_skills': ", ".join(skills),
                'broker_id': self.broker.id,
                'posted_date': datetime.utcnow(),
                'status': 'active'
            }
            
            return mission_data
        
        except NoSuchElementException as e:
            logging.error(f"Missing element in job card: {str(e)}")
            return None
    
    def extract_skills(self, title):
        """
        Extract potential skills from the job title.
        
        Args:
            title: The job title string.
            
        Returns:
            list: List of extracted skills.
        """
        # Common IT skills to look for
        common_skills = [
            "Python", "Java", "JavaScript", "React", "Angular", "Vue", 
            "Node.js", "C#", ".NET", "SQL", "NoSQL", "AWS", "Azure", 
            "DevOps", "Docker", "Kubernetes", "Machine Learning", "AI",
            "Data Science", "Full Stack", "Frontend", "Backend", "UX", "UI",
            "Project Manager", "Scrum Master", "Product Owner", "Agile",
            "Architect", "Designer", "Engineer", "Developer"
        ]
        
        # Extract skills from title
        found_skills = []
        for skill in common_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', title, re.IGNORECASE):
                found_skills.append(skill)
        
        return found_skills
    
    def handle_cookie_consent(self, driver):
        """
        Handle cookie consent dialog if it appears.
        
        Args:
            driver: The WebDriver instance.
        """
        try:
            # Wait for cookie policy button to appear
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cookie-policy-button"))
            )
            cookie_button.click()
            time.sleep(1)  # Wait for dialog to close
            logging.info("Handled cookie consent dialog")
        except TimeoutException:
            # Cookie dialog might not appear, which is fine
            logging.info("No cookie consent dialog found")
            pass
    
    def scrape_page(self, driver, page_num=1):
        """
        Scrape a single page of job listings.
        
        Args:
            driver: The WebDriver instance.
            page_num: The page number to scrape.
            
        Returns:
            list: List of mission data dictionaries.
        """
        missions = []
        
        try:
            # Navigate to the page
            if page_num > 1:
                # Click on the pagination button for the specific page
                pagination_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"button[aria-label='Page {page_num}']"))
                )
                pagination_button.click()
                time.sleep(self.rate_limit)
            
            # Wait for job listings to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-card"))
            )
            
            # Find all job elements
            job_elements = driver.find_elements(By.CSS_SELECTOR, "div.job-card")
            logging.info(f"Found {len(job_elements)} jobs on page {page_num}")
            
            # Extract data from each job element
            for element in job_elements:
                mission_data = self.extract_job_details(element)
                if mission_data:
                    missions.append(mission_data)
            
            return missions
        
        except TimeoutException:
            logging.warning(f"Timeout waiting for elements on page {page_num}")
            return []
        except Exception as e:
            logging.error(f"Error scraping page {page_num}: {str(e)}")
            return []
    
    def scrape(self):
        """
        Scrape job listings from Ework Group.
        
        Returns:
            list: List of mission data dictionaries.
        """
        driver = None
        retry_count = 0
        all_missions = []
        
        try:
            while retry_count < self.max_retries:
                try:
                    driver = self.setup_driver()
                    logging.info(f"Scraping {self.base_url}")
                    
                    # Load the initial page
                    driver.get(self.base_url)
                    time.sleep(self.rate_limit)
                    
                    # Handle cookie consent if it appears
                    self.handle_cookie_consent(driver)
                    
                    # Scrape each page up to max_pages
                    for page_num in range(1, self.max_pages + 1):
                        page_missions = self.scrape_page(driver, page_num)
                        
                        if not page_missions:
                            break  # No more results or error occurred
                        
                        all_missions.extend(page_missions)
                        time.sleep(self.rate_limit)
                    
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
        
        logging.info(f"Scraped {len(all_missions)} total missions from Ework Group")
        return all_missions
