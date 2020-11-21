import requests
from bs4 import BeautifulSoup
from random import randint
from os import environ
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
load_dotenv()

driver = webdriver.Chrome()
href = "https://leetcode.com/problems/add-two-numbers/submissions/"


# driver.get(href)
driver.get(href)
# driver.implicitly_wait(2)
driver.find_element_by_xpath('//button[@class="btn__1eiM btn-lg__2g-N "]').click()
driver.find_element_by_xpath('// *[ @ id = "id_login"]').send_keys(environ.get("LEETCODE_EMAIL"))
driver.find_element_by_xpath('// *[ @ id = "id_password"]').send_keys(environ.get("LEETCODE_PASS"))
driver.find_element_by_xpath('// *[ @ id = "id_password"]').send_keys(Keys.ENTER)

soup = BeautifulSoup(driver.page_source, features="html.parser")
test = soup.find_all('span', {"role" : "presentation"})

template = ""
for x in test:
    template += x.text + "\n"

print(template)
driver.close()