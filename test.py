from bs4 import BeautifulSoup
from datetime import datetime
import requests


print(datetime.now().month)
# link = "https://projecteuler.net/recent"
# response = requests.get(link)
# soup = BeautifulSoup(response.content, 'html.parser')
# val = 0
# try:
#     val = soup.find('td', class_="id_column").text
# except:
#     print("TEST")
# else:
#     print(val)
# for x in soup.find_all('td', class_="id_column"):
#     print(x.text)