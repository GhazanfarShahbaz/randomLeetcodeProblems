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
from selenium.webdriver.common.action_chains import ActionChains

# from .utility.messageDict import getLanguageCode
from dotenv import load_dotenv
load_dotenv()

messageSyntax = {
    "c" : "c",
    "c++" : "cpp",
    "java" : "java",
    "python" : "py",
    "python3" : "py",
    "javascript" : "js",
    "ruby" : "ruby",
    "swift" : "swift",
    "go" : "go",
    "scala" : "scala",
    "kotlin" : "kotlin",
    "rust" : "rust",
    "php" : "php",
    "typescript" : "typescript"
}


def getLanguageCode(lang : str) -> None or str:
    return None if lang.lower() not in messageSyntax.keys() else messageSyntax[lang.lower()]


# print(getLanguageCode("Python3"))

driver = webdriver.Chrome()
href = "https://leetcode.com/problems/minimum-value-to-get-positive-step-by-step-sum"
driver.get(href)
soup = BeautifulSoup(driver.page_source, features="html.parser")

problem = "```\n"

problem = "```\n"
for x in soup.find_all("div", class_="content__u3I1 question-content__JfgR"):
    problem += x.text + "\n"
problem += "```"

# print(problem)

# # driver.find_element_by_link_text("Submissions").click()
# driver.find_element_by_xpath('//span[@class="ant-select-arrow"]').click()
# driver.find_element_by_xpath('//li[@data-cy="lang-select-Python3"]').click()
# driver.find_element_by_xpath('//button[@class="btn__1eiM btn-lg__2g-N "]').click()
# driver.find_element_by_xpath('// *[ @ id = "id_login"]').send_keys(environ.get("LEETCODE_EMAIL"))
# driver.find_element_by_xpath('// *[ @ id = "id_password"]').send_keys(environ.get("LEETCODE_PASS"))
# driver.find_element_by_xpath('// *[ @ id = "id_password"]').send_keys(Keys.ENTER)

language = "Kotlin".title()
# langauge = language.title()
xpath = f'//li[@data-cy=\"lang-select-{language}\"]'
# button = wait.until(EC.visibility_of_element_located((By.XPATH, f'//li[@data-cy="lang-select-{language}"]')))
# print(email)

# WebElement response = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//*[@class='i-am-your-class']")));
"lang-select-Kotlin"

element = driver.find_element_by_xpath('//li[@data-cy="lang-select-C"]')
actions = ActionChains(driver)
actions.move_to_element(element).perform()
driver.find_element_by_xpath('//li[@data-cy="lang-select-C"]').click()
# driver.find_element_by_xpath('//span[@class="ant-select-arrow"]').click()
# driver.find_element_by_xpath(xpath).click()

# soup = BeautifulSoup(driver.page_source, features="html.parser")
# code_block = soup.find_all('span', {"role" : "presentation"})
# wait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//li[@data-cy="lang-select-Swift"]'))).click() 
# driver.find_element_by_xpath(f'//li[@data-cy="lang-select-Swift"]').click()
# for x in code_block:
#     template += x.text + "\n"
# template += "```"

# soup = BeautifulSoup(driver.page_source, features="html.parser")
# test = soup.find_all('span', {"role" : "presentation"})

# template = ""
# for x in test:
#     template += x.text + "\n"

# print(template)



# driver.close()