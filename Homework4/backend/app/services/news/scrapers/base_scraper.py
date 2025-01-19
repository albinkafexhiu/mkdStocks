from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
from typing import List, Dict, Any, Optional

class NewsScraper(ABC):
    def __init__(self, articles_per_source: int = 3):
        self.articles_per_source = articles_per_source
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.wait_time = 10

    def scrape_company_news(self, company_name: str) -> List[Dict[str, Any]]:
        """Template method defining the scraping algorithm"""
        driver = webdriver.Chrome(options=self.options)
        articles = []
        
        try:
            search_name = self.clean_company_name(company_name)
            print(f"Scraping {self.get_source_name()} for {company_name}")
            
            # Get search URL
            url = self.get_search_url(search_name)
            driver.get(url)
            time.sleep(2)
            
            # Get article list
            article_elements = self.get_article_list(driver)
            
            for article in article_elements[:self.articles_per_source]:
                try:
                    article_data = self.extract_article_data(driver, article)
                    if article_data:
                        articles.append(article_data)
                        print(f"Scraped article: {article_data['title'][:50]}...")
                except Exception as e:
                    print(f"Error scraping article: {str(e)}")
                    continue
                    
        finally:
            driver.quit()
            
        return articles

    def wait_and_get_element(self, driver, by, selector, timeout=10, retries=3) -> Optional[Any]:
        for _ in range(retries):
            try:
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((by, selector))
                )
                return element
            except (StaleElementReferenceException, TimeoutException):
                time.sleep(1)
        return None

    def wait_and_get_elements(self, driver, by, selector, timeout=10, retries=3) -> List[Any]:
        for _ in range(retries):
            try:
                elements = WebDriverWait(driver, timeout).until(
                    EC.presence_of_all_elements_located((by, selector))
                )
                return elements[:self.articles_per_source]
            except (StaleElementReferenceException, TimeoutException):
                time.sleep(1)
        return []

    def clean_company_name(self, name: str) -> str:
        removables = ["АД", "Скопје", "Битола", "Тетово", "Прилеп", "Кавадарци", "Охрид"]
        cleaned = name
        for term in removables:
            cleaned = cleaned.replace(term, "").strip()
        return cleaned

    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of the news source"""
        pass

    @abstractmethod
    def get_search_url(self, search_term: str) -> str:
        """Generate search URL for the news source"""
        pass

    @abstractmethod
    def get_article_list(self, driver: webdriver.Chrome) -> List[Any]:
        """Get list of article elements from search results"""
        pass

    @abstractmethod
    def extract_article_data(self, driver: webdriver.Chrome, article_element: Any) -> Dict[str, Any]:
        """Extract data from individual article"""
        pass