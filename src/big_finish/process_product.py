import re
import requests
from bs4 import BeautifulSoup

disallowed_chars = [":", ";", ",", "!", "?", "\""]

def remove_duplicates(l):
    return list(dict.fromkeys(l))

def process_product(url):
    # Get the page
    rsp = requests.get(f"https://bigfinish.com{url}")
    soup = BeautifulSoup(rsp.text, 'html.parser')

    # Get the product Lines - These will be folders
    lines = [g.text.strip()
             for g in soup.select(".bread-crumb-left ul li a")[2:]]
    lines = "-".join(lines).split("-")
    lines = [l.strip() for l in lines]
    lines = remove_duplicates(lines)

    # Get the product name
    name = soup.select("h3")[0].text.strip()
    for l in lines:
        name = name.replace(l, "")
        if l[-1] == 's': # Remove plural
            name = name.replace(l[:-1], "")

    for c in disallowed_chars:
        name = name.replace(c, " ")

    name = name.replace(" - ", " ")

    name = re.sub(r'\s+', ' ', name).strip()

    # Make the folder Path
    lines.append(name)

    path = "/".join(lines)

    # Get the product id
    image_url = soup.select_one('.detail-page-image img').get('src')
    id = re.search(r'\d+', image_url).group(0)

    return (id, path)
