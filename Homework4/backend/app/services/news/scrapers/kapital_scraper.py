from datetime import datetime
from .base_scraper import NewsScraper
from selenium.webdriver.common.by import By
import time

class KapitalScraper(NewsScraper):
    def get_source_name(self) -> str:
        return "kapital.mk"

    def get_search_url(self, search_term: str) -> str:
        return f'https://kapital.mk/?s={search_term}'

    def get_article_list(self, driver):
        return self.wait_and_get_elements(
            driver, 
            By.CSS_SELECTOR, 
            ".mvp-blog-story-list li"
        )

    def extract_article_data(self, driver, article_element):
        link_element = self.wait_and_get_element(article_element, By.CSS_SELECTOR, "a")
        if not link_element:
            return None
            
        link = link_element.get_attribute('href')
        driver.get(link)
        time.sleep(2)
        
        title_element = self.wait_and_get_element(driver, By.CSS_SELECTOR, "h1")
        date_element = self.wait_and_get_element(driver, By.CSS_SELECTOR, 'time')
        content_element = self.wait_and_get_element(driver, By.CSS_SELECTOR, ".mvp-post-soc-out")
        
        if all([title_element, date_element, content_element]):
            title = title_element.text
            date = date_element.get_attribute('datetime')
            content = content_element.text
            
            if content:
                content = content.split('ПОВРЗАНИ ТЕМИ:')[0]
                
            return {
                'date': datetime.fromisoformat(date).strftime("%Y-%m-%d"),
                'title': title,
                'content': content,
                'url': link,
                'source': self.get_source_name()
            }
        return None