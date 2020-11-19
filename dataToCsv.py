import requests
from bs4 import BeautifulSoup
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd 
import time
from selenium.webdriver.support.ui import Select

# Wait for 5 seconds


def parsePage(driver, data):
    # soup = BeautifulSoup(driver.page_source, features="html.parser")

    start = True
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    
    for trTags in soup.find_all("tr"):
        if(start):
            start = False
            continue
        else:
            parser = 0
            currentData = {}
            for row in trTags.find_all('td'):
                if parser == 1:
                    currentData["number"] = row.text.strip()
                elif parser == 2:
                    val = row.text.strip()
                    currentData["name"] = val
                    currentData["subscription"] = "No" if len(row.findChild().contents) == 2 else "Yes"
                    currentData["link"] = f"https://leetcode.com{row.findChild().findChild()['href']}"
                elif parser == 4:
                    currentData["acceptance"] = row.text
                elif parser == 5:
                    currentData["difficulty"] = row.text
                    break
                parser += 1 

            if currentData:
                data.append(currentData)

def saveDataAsCsv():
    driver = webdriver.Safari()
    driver.get("https://leetcode.com/problemset/all/")
    driver.find_element_by_xpath('//select[@class = "form-control"]').click()

    select = Select(driver.find_element_by_xpath('//select[@class = "form-control"]'))
    select.select_by_visible_text('all')

    data = []

    parsePage(driver, data)

    # driver.close()
    # df = pd.DataFrame.from_dict(data)
    # df.to_csv("leetcodeData.csv")



if __name__ == "__main__":
    saveDataAsCsv()
    