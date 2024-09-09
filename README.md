# Scraping Tool

can find the sample results of Scraping in data.json file and images can be found in Images folder

static token for autorization can be found in config.py

used redis cache for caching which can be found on cache.py

all the requirements can be found in requirements.txt

all the operations for read and writing to databse were implemented in databse.py

notification.py contains the logger for logs and error

scraper.py contains Scraper class containing the functions used for scrapping

can find api in app.py

`/scrape/` endpoint is used for scrapping which takes two optional parameters `page_limit` and `proxy` for scrapping

currently scrapper retries 3 times on fail with a gap of 2sec each before giving error
