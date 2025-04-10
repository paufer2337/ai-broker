"""
DFind IT Scraper

This module implements a scraper for DFind IT job listings.
It extracts mission data from the DFind IT website without requiring authentication.
"""

from ..base import BaseScraper
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time
import re

class DFindITScraper(BaseScraper):
    """
    Scraper for DFind IT job listings.
    
    This scraper uses requests and BeautifulSoup to extract job listings from the DFind IT website.
    It handles pagination and extracts detailed information about each job.
    """
    
    def __init__(self, broker):
        """
        Initialize the DFind IT scraper.
        
        Args:
            broker: The broker object containing information about the broker.
        """
        super().__init__(broker)
        self.base_url = "https://www.dfind.se/it/lediga-jobb"
        self.rate_limit = 3  # seconds between requests
        self.max_retries = 3
        self.max_pages = 5  # Maximum number of pages to scrape
    
    def extract_job_details(self, job_element):
        """
        Extract job details from a job listing element.
        
        Args:
            job_element: The BeautifulSoup element containing the job listing.
            
        Returns:
            dict: Dictionary containing job details.
        """
        try:
            # Extract job title
            title_element = job_element.find('h2', class_='job-title')
            title = title_element.text.strip() if title_element else "Unknown Title"
            
            # Extract job URL
            job_url = ""
            if title_element and title_element.find('a'):
                job_url = title_element.find('a').get('href', '')
                if job_url and not job_url.startswith('http'):
                    job_url = f"https://www.dfind.se{job_url}"
            
            # Extract location
            location_element = job_element.find('div', class_='job-location')
            location = location_element.text.strip() if location_element else "Unknown Location"
            
            # Extract job type
            job_type_element = job_element.find('div', class_='job-type')
            job_type = job_type_element.text.strip() if job_type_element else ""
            
            # Extract description snippet
            description_element = job_element.find('div', class_='job-description')
            description_snippet = description_element.text.strip() if description_element else ""
            
            # Extract posting date
            date_element = job_element.find('div', class_='job-date')
            posted_date = date_element.text.strip() if date_element else ""
            
            # Combine all information into a description
            description = f"Position: {title}\n"
            description += f"Location: {location}\n"
            if job_type:
                description += f"Job Type: {job_type}\n"
            if posted_date:
                description += f"Posted: {posted_date}\n"
            description += f"URL: {job_url}\n\n"
            if description_snippet:
                description += f"Description: {description_snippet}\n"
            
            # Extract skills from the title and description
            skills = self.extract_skills(title, description_snippet)
            
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
        
        except Exception as e:
            logging.error(f"Error extracting job details: {str(e)}")
            return None
    
    def extract_skills(self, title, description=""):
        """
        Extract potential skills from the job title and description.
        
        Args:
            title: The job title string.
            description: The job description string.
            
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
        
        # Extract skills from title and description
        found_skills = []
        text_to_search = f"{title} {description}"
        
        for skill in common_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_to_search, re.IGNORECASE):
                found_skills.append(skill)
        
        return found_skills
    
    def scrape_page(self, page_num=1):
        """
        Scrape a single page of job listings.
        
        Args:
            page_num: The page number to scrape.
            
        Returns:
            list: List of mission data dictionaries.
        """
        missions = []
        
        try:
            # Construct URL with page parameter
            url = self.base_url
            if page_num > 1:
                url = f"{self.base_url}?page={page_num}"
            
            # Make request with retry logic
            retry_count = 0
            response = None
            
            while retry_count < self.max_retries:
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    break
                except requests.exceptions.RequestException as e:
                    retry_count += 1
                    logging.warning(f"Request error on attempt {retry_count}: {str(e)}")
                    if retry_count >= self.max_retries:
                        logging.error(f"Failed to retrieve page {page_num} after {self.max_retries} attempts")
                        return []
                    time.sleep(self.rate_limit)
            
            if not response:
                return []
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all job elements
            job_elements = soup.find_all('div', class_='job-listing')
            logging.info(f"Found {len(job_elements)} jobs on page {page_num}")
            
            # Extract data from each job element
            for element in job_elements:
                mission_data = self.extract_job_details(element)
                if mission_data:
                    missions.append(mission_data)
            
            # Respect rate limit
            time.sleep(self.rate_limit)
            
            return missions
        
        except Exception as e:
            logging.error(f"Error scraping page {page_num}: {str(e)}")
            return []
    
    def scrape(self):
        """
        Scrape job listings from DFind IT.
        
        Returns:
            list: List of mission data dictionaries.
        """
        all_missions = []
        
        try:
            # Scrape each page up to max_pages
            for page_num in range(1, self.max_pages + 1):
                logging.info(f"Scraping page {page_num} of DFind IT")
                page_missions = self.scrape_page(page_num)
                
                if not page_missions:
                    break  # No more results or error occurred
                
                all_missions.extend(page_missions)
        
        except Exception as e:
            logging.error(f"Unexpected error during scraping: {str(e)}")
        
        logging.info(f"Scraped {len(all_missions)} total missions from DFind IT")
        return all_missions
