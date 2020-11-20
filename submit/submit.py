import requests
from bs4 import BeautifulSoup
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CODE_DRIVER = webdriver.Safari()
href = "https://leetcode.com/problems/two-sum/submissions/"

CODE_DRIVER.get(href)
CODE_DRIVER.find_element_by_xpath('//button[@data-cy="submit-code-btn"]').click()
CODE_DRIVER.find_element_by_xpath("//*[@id ='id_login']").send_keys("TEST")


# wait = WebDriverWait(CODE_DRIVER,10)
# code = ""

# CODE_DRIVER.get(href)

# reset_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "code-btn")))
# reset_button.click()

# confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "confirmRecent"]'
#                                                                     ' / div / div / div[3] / button[2]')))
# confirm_button.click()

# CODE_DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# time.sleep(TIME_DELAY + 2)

# code_elem = CODE_DRIVER.find_element_by_class_name("ace_text-input")
# code_elem.send_keys(Keys.LEFT_CONTROL, 'a')
# code_elem.send_keys(Keys.LEFT_CONTROL, 'c')

# code = ROOT.clipboard_get()
 
print(code)