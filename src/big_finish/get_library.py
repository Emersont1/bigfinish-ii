from .process_product import process_product

from bs4 import BeautifulSoup

def parse(div):
    img_panel = div.select_one(".release-image a")
    url = img_panel.get("data-src").replace("/releases/a/", "/releases/v/")
    id, path = process_product(url)

    main_downloads = [a.get('href') for a in div.select(".desktop-downloads a")]
    supp_downloads = [a.get('href') for a in div.select(".supplementaryMedia ul li a")]

    return (id, path, main_downloads, supp_downloads)


def get_library(s):
    import re

    n = 1
    objects = []
    while True:
        print(f"Scraping page {n}")
        url = f"https://bigfinish.com/customers/my_account/page:{n}"

        rsp =  s.get(url)
        soup = BeautifulSoup(rsp.text, 'html.parser')

        if soup.h1 and soup.h1.text == "Error 404":
            break

        objects.extend([parse(div) for div in soup.select(".account-release-download")]) 
        n += 1
    return objects
