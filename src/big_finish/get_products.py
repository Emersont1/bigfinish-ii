import re
import requests
from bs4 import BeautifulSoup

def get_products():
    
    n = 1
    urls = []
    while True:
        print(f"Scraping page {n}")
        url = f"https://bigfinish.com/releases/index/page:{n}"

        rsp =   requests.get(url)
        soup = BeautifulSoup(rsp.text, 'html.parser')

        if soup.h1 and soup.h1.text == "Error 404":
            break

        urls.extend([a.get('href') for a in soup.select(".release-items h3 a")])      
        n += 1
    return urls
