from fastapi import FastAPI, Depends, HTTPException,Header
from typing import Optional
from scraper import Scraper
from database import Database
from cache import cache
from config import TOKEN
from notification import notify


app = FastAPI()
    
def verify_token(authorization: Optional[str] = Header(None)):
    if authorization is None or authorization != f"Bearer {TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
def welcomne():
    return {"message": f"hello"}


@app.post("/scrape/", dependencies=[Depends(verify_token)])
def scrape_site(page_limit: int = 5, proxy: str = None):
    scraper = Scraper(base_url="https://dentalstall.com/shop", page_limit=page_limit, proxy=proxy)
    products = scraper.scrape()
    
    db = Database()

    new_products = []
    for product in products:
        #multiple products have same tittle as tittle is truncated on main page so using image name insted
        cached_price = cache.get_cached_price(product['path_to_image'])
        if cached_price != float(product['product_price'][1:]):
            new_products.append(product)
            cache.set_cached_price(product['path_to_image'], float(product['product_price'][1:]))

    db.update_if_needed(new_products)
    notify.log( f"Scraped {len(products)} and updated {len(new_products)} products.")
    return products
