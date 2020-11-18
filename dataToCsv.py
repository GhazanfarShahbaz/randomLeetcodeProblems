import requests
from bs4 import BeautifulSoup
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd 
import time
 
# Wait for 5 seconds


def parseNewPage(driver, data):
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    # while True:
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
                if(parser == 1):
                    currentData["number"] = row.text.strip()
                elif(parser == 2):
                    val = row.text.strip()
                    currentData["name"] = val
                    link = "https://leetcode.com/problems/"
                    for letter in val:
                        if letter == " ":
                            link += "-"
                        elif letter.isalnum():
                            link += letter.lower()
                    currentData["link"] = link
                elif(parser == 4):
                    currentData["acceptance"] = row.text
                elif(parser == 5):
                    currentData["difficulty"] = row.text
                    break

                parser += 1 

            if currentData:
                # print(currentData["number"])
                data["values"].append(currentData)

def saveDataAsCsv():
    driver = webdriver.Safari()
    driver.get("https://leetcode.com/problemset/all/")
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    data = {}
    data["values"] = []
    count = 0
    while count < 34:
        parseNewPage(driver, data)
        try:
            driver.find_element_by_xpath('//a[@class = "reactable-next-page"]')
        except:
            break
        
        driver.find_element_by_xpath('//a[@class = "reactable-next-page"]').click()
        count += 1
        print(count)
    print("done")
    driver.close()
    df = pd.DataFrame.from_dict(data["values"])
    df.to_csv("leetcodeData.csv")



if __name__ == "__main__":
    saveDataAsCsv()
    