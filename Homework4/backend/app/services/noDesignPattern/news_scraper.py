from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from datetime import datetime
import json
import time
from typing import List, Dict, Any

# Just the first 5 companies for testing
TEST_COMPANIES = [
    "Комерцијална банка АД Скопје",
    "Алкалоид АД Скопје",
    "Макпетрол АД Скопје",
    "Стопанска банка АД Скопје",
    "Македонски Телеком АД Скопје"
]

class NewsScraper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.articles_per_source = 3  # Limit to 3 articles per source
        self.wait_time = 10

    def wait_and_get_element(self, driver, by, selector, timeout=10, retries=3):
        for _ in range(retries):
            try:
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((by, selector))
                )
                return element
            except StaleElementReferenceException:
                time.sleep(1)
                continue
            except TimeoutException:
                return None
        return None

    def wait_and_get_elements(self, driver, by, selector, timeout=10, retries=3):
        for _ in range(retries):
            try:
                elements = WebDriverWait(driver, timeout).until(
                    EC.presence_of_all_elements_located((by, selector))
                )
                return elements[:self.articles_per_source]  # Only take first 3 articles
            except StaleElementReferenceException:
                time.sleep(1)
                continue
            except TimeoutException:
                return []
        return []

    def clean_company_name(self, name: str) -> str:
        removables = ["АД", "Скопје", "Битола", "Тетово", "Прилеп", "Кавадарци", "Охрид"]
        cleaned = name
        for term in removables:
            cleaned = cleaned.replace(term, "").strip()
        return cleaned

    def scrape_kapital(self, company_name: str) -> List[Dict[str, Any]]:
        driver = webdriver.Chrome(options=self.options)
        articles = []
        
        try:
            search_name = self.clean_company_name(company_name)
            print(f"Scraping Kapital.mk for {company_name}")
            
            url = f'https://kapital.mk/?s={search_name}'  # Only first page
            driver.get(url)
            time.sleep(2)
            
            article_list = self.wait_and_get_elements(driver, By.CSS_SELECTOR, ".mvp-blog-story-list li")

            for article in article_list:
                try:
                    link_element = self.wait_and_get_element(article, By.CSS_SELECTOR, "a")
                    if not link_element:
                        continue
                        
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
                            
                        articles.append({
                            'date': datetime.fromisoformat(date).strftime("%Y-%m-%d"),
                            'title': title,
                            'content': content,
                            'url': link,
                            'source': 'kapital.mk'
                        })
                        print(f"Scraped article: {title[:50]}...")
                        
                except Exception as e:
                    print(f"Error scraping article: {str(e)}")
                    continue
                    
                if len(articles) >= self.articles_per_source:
                    break
                    
        finally:
            driver.quit()
            
        return articles

    def scrape_biznis_info(self, company_name: str) -> List[Dict[str, Any]]:
        driver = webdriver.Chrome(options=self.options)
        articles = []
        
        try:
            search_name = self.clean_company_name(company_name)
            print(f"Scraping BiznisInfo.mk for {company_name}")
            
            url = f'https://biznisinfo.mk/?s={search_name}'  # Only first page
            driver.get(url)
            time.sleep(2)
            
            article_list = self.wait_and_get_elements(driver, By.CSS_SELECTOR, ".td_module_10")

            for article in article_list:
                try:
                    link_element = self.wait_and_get_element(article, By.CSS_SELECTOR, "a")
                    if not link_element:
                        continue
                        
                    link = link_element.get_attribute('href')
                    driver.get(link)
                    time.sleep(2)
                    
                    title_element = self.wait_and_get_element(driver, By.CSS_SELECTOR, "h1.entry-title")
                    date_element = self.wait_and_get_element(driver, By.CSS_SELECTOR, 'time')
                    content_element = self.wait_and_get_element(driver, By.CSS_SELECTOR, ".td-post-content")
                    
                    if all([title_element, date_element, content_element]):
                        title = title_element.text
                        date = date_element.text
                        content = content_element.text
                        
                        if content:
                            content = content.split('Можеби ќе ве интересира')[0]
                            
                        articles.append({
                            'date': datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d"),
                            'title': title,
                            'content': content,
                            'url': link,
                            'source': 'biznisinfo.mk'
                        })
                        print(f"Scraped article: {title[:50]}...")
                        
                except Exception as e:
                    print(f"Error scraping article: {str(e)}")
                    continue
                    
                if len(articles) >= self.articles_per_source:
                    break
                    
        finally:
            driver.quit()
            
        return articles

    def scrape_all_news(self) -> None:
        all_news = {}
        total_companies = len(TEST_COMPANIES)
        
        print(f"Starting news scraping for {total_companies} test companies...")
        print(f"Will get {self.articles_per_source} articles per source (total {self.articles_per_source * 2} per company)")
        print("-" * 50)
        
        for i, company in enumerate(TEST_COMPANIES, 1):
            print(f"\nProgress: {i}/{total_companies} companies")
            print(f"Starting news scrape for: {company}")
            company_news = []
            
            try:
                kapital_news = self.scrape_kapital(company)
                company_news.extend(kapital_news)
                print(f"Found {len(kapital_news)} articles from Kapital.mk")
            except Exception as e:
                print(f"Error scraping Kapital.mk: {str(e)}")
            
            try:
                biznis_news = self.scrape_biznis_info(company)
                company_news.extend(biznis_news)
                print(f"Found {len(biznis_news)} articles from BiznisInfo.mk")
            except Exception as e:
                print(f"Error scraping BiznisInfo.mk: {str(e)}")
            
            if company_news:
                all_news[company] = company_news
                
            print(f"Total articles found for {company}: {len(company_news)}")
            print("-" * 50)
            
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'scraped_news_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_news, f, ensure_ascii=False, indent=2)
            
        print(f"\nNews scraping completed!")
        print(f"Results saved to: {filename}")
        print(f"Total companies processed: {total_companies}")
        print(f"Total articles found: {sum(len(news) for news in all_news.values())}")

if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.scrape_all_news()