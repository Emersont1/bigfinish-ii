import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def build_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

    return driver

def login(email, password):
    driver = build_driver()
    driver.get("https://www.bigfinish.com/customers/login")
    e = driver.find_element_by_css_selector(".login-form .email input")
    driver.execute_script("arguments[0].value = arguments[1]", e, email)
    p = driver.find_element_by_css_selector(".login-form .pswd input")
    driver.execute_script("arguments[0].value = arguments[1]", p, password)
    b = driver.find_element_by_css_selector(".login-form #submit-btn")
    driver.execute_script("arguments[0].click()", b)

    

    session = requests.session()
    
    session.headers.update({ # Set the User Agent
    'User-Agent':driver.execute_script("return navigator.userAgent"),
    })

    cookies = {c["name"]:c["value"] for c in driver.get_cookies()}  # Get the cookies
    session.cookies = requests.utils.cookiejar_from_dict(cookies)  # Set the cookies

    driver.close()

    return session