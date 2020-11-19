import requests
from bs4 import BeautifulSoup
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
# fron sele
import pandas as pd 
import time
from selenium.webdriver.support.ui import Select



tags = []
driver = webdriver.Safari()
driver.get("https://leetcode.com/problemset/all/")

	
# time.sleep(5)
# driver.implicitly_wait(40)
driver.find_element_by_xpath('//select[@class = "form-control"]').click()

select = Select(driver.find_element_by_xpath('//select[@class = "form-control"]'))
select.select_by_value('9007199254740991')

# soup = BeautifulSoup(driver.page_source, features="html.parser")

# data = ""
# with wait_for_page_load(driver):
#    data.find_all('div', class_ = "filter-dropdown-menu-item")

# print(data)
# 9007199254740991
# 9007199254740991
# for x in soup.find_all('div', class_ = "filter-dropdown-menu-item"):
#     print(x)
    # break

# driver.close()