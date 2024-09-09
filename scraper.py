import requests
from bs4 import BeautifulSoup
from time import sleep
from typing import List, Dict, Optional
import os
from notification import notify
from cache import cache

class Scraper:
    def __init__(self, base_url: str, page_limit: int = 5, proxy: Optional[str] = None):
        self.base_url = base_url
        self.page_limit = page_limit
        self.proxy = proxy
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_page(self, page_number: int, retry_count: int = 0) -> Optional[str]:
        if retry_count > 2:
            notify.error(f"Error fetching page after retires {page_number}: {e}")
            return None
        try:
            url = f"{self.base_url}/"
            if page_number > 1:
                url = f"{self.base_url}/page/{page_number}"
            proxies = {'http': self.proxy, 'https': self.proxy} if self.proxy else None
            response = requests.get(url, headers=self.headers, proxies=proxies)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            notify.error(f"Error fetching page {page_number}: {e}")
            sleep(2) #retry after 2 secons
            return self.fetch_page(page_number, retry_count + 1)

    def scrape(self) -> List[Dict]:
        products = []
        for page in range(1, self.page_limit + 1):
            html_content = self.fetch_page(page)
            if not html_content:
                continue  # Retry or skip
            soup = BeautifulSoup(html_content, 'html.parser')


            product_cards = soup.find_all('div', {'class': 'product-inner'})


            for card in product_cards:
                title = card.find('h2', {'class': 'woo-loop-product__title'}).text.strip()
                price = card.find('span', {'class': 'woocommerce-Price-amount'}).text.strip()
                image_url = card.find('img', {'class': 'attachment-woocommerce_thumbnail'})["data-lazy-src"]
                image_path = self.save_image(image_url, float(price[1:]))
                products.append({
                    "product_title": title,
                    "product_price": price,
                    "path_to_image": image_path
                })
            sleep(1)
        return products

    def save_image(self, image_url: str, price: float = -1) -> str:
        image_name = os.path.basename(image_url)
        image_path = f'./Images/{image_name}'
        cached_price = cache.get_cached_price(image_path)
        if cached_price==price:
            #Saving image only when price is updated to reduce overwriting same image again and again
            return image_path
        image_content = requests.get(image_url).content
        with open(image_path, 'wb') as img_file:
            img_file.write(image_content)
        return image_path

