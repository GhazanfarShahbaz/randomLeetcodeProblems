import requests
from bs4 import BeautifulSoup
# import soupsieve
from random import randint
from selenium import webdriver


def getRandomProblem() -> str:
    driver = webdriver.Safari()
    driver.get(f"https://leetcode.com/problemset/all/?search={randint(1, 1649)}")
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    count = 0
    problemLink = ""
    for link in soup.find_all('a', href = True):
        if "/problems/" in link.get("href"):
            count += 1
            if count == 2:
                problemLink = link.get("href")
                break
    driver.close()

    return f"https://leetcode.com{problemLink}"


if __name__ == "__main__":
    print(getRandomProblem())
