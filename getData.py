import requests
from bs4 import BeautifulSoup
# import soupsieve
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Safari()
driver.get("https://leetcode.com/problemset/all/")
soup = BeautifulSoup(driver.page_source, features="html.parser")

count = 0
problemLink = []
# k = soup.find_all("tbody", class_="reactable_data")
start = True

data = {}
data["values"] = []
for a in soup.find_all("tr"):
    if(start):
        start = False
        continue
    else:
        parser = 0
        currentData = {}
        for b in a.find_all('td'):
            if(parser == 1):
                currentData["number"] = b.text.strip()
            elif(parser == 2):
                val = b.text.strip()
                currentData["name"] = val
                link = "https://leetcode.com/problems/"
                for x in val:
                    if x == " ":
                        link += "-"
                    elif x.isalnum():
                        link +=  x.lower()
                currentData["link"] = link
            elif(parser == 4):
                currentData["acceptance"]  = b.text
            elif(parser == 5):
                currentData["difficulty"] = b.text
                break
            parser+=1
        if currentData:
            data["values"].append(currentData)
    
for x in data["values"]:
    print(x['link'])

        
    # break

# for link in soup.find_all('a', href = True):
#     if "/problems/" in link.get("href"):
#         # count += 1
#         # if count == 2:
#         #     print(link)
#         problemLink.append(link.get("href"))
#             break
# try:
driver.find_element_by_xpath('//a[@class = "reactable-next-page"]').click()
# soup = BeautifulSoup(driver.page_source, features="html.parser")

# data = {}
# data["values"] = []
# for a in soup.find_all("tr"):
#     if(start):
#         start = False
#         continue
#     else:
#         parser = 0
#         currentData = {}
#         for b in a.find_all('td'):
#             if(parser == 1):
#                 currentData["number"] = b.text.strip()
#             elif(parser == 2):
#                 val = b.text.strip()
#                 currentData["name"] = val
#                 link = "https://leetcode.com/problems/"
#                 for x in val:
#                     if x == " ":
#                         link += "-"
#                     elif x.isalnum():
#                         link +=  x.lower()
#                 currentData["link"] = link
#             elif(parser == 4):
#                 currentData["acceptance"]  = b.text
#             elif(parser == 5):
#                 currentData["difficulty"] = b.text
#                 break
#             parser+=1
#         if currentData:
#             data["values"].append(currentData)
    
# for x in data["values"]:
#     print(x['link'])
# except:
#     pass


# soup = BeautifulSoup(driver.page_source, features="html.parser")

# count = 0
# for link in soup.find_all('a', href = True):
#     if "/problems/" in link.get("href"):
#         # count += 1
#         # if count == 2:
#         problemLink.append(link.get("href"))
#             # break




# driver.close()