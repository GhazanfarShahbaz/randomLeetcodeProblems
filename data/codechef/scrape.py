import requests
from bs4 import BeautifulSoup
import pandas as pd 

website_link = 'https://www.codechef.com/problems/'
endpoints = {"school" : "beginner",
            'easy': "easy",
            'medium': "medium",
            'hard': "hard",
            'challenge': "challenge",
            'peer': "extcontest"
            }

globalData = []


for z, t in endpoints.items():
    response =requests.get(website_link + z)
    soup = BeautifulSoup(response.content, features="html.parser")
    for x in soup.find_all('tr', class_="problemrow"):
        parse = 1
        data = {}
        for y in x:
            if parse == 1:
                try:
                    link = y.find('a').get('href')
                    # name = f"\'{y.find('a').find('b').text}\'"
                    name = y.find('a').find('b').text
                    ph = ""
                    for x in name:
                        if x.isalnum():
                            ph += x
                        else:
                            ph += " "
                    data['name'] = ph
                    data['link'] = "https://www.codechef.com" + link
                except:
                    data['link'] = ""
                    data['name'] = ""
            if(parse == 2):
                try:
                    submitLink = y.find('a').get('href')
                    data['submitLink'] = "https://www.codechef.com" + submitLink
                except:
                     data['submitLink'] = ""
            if(parse == 3):
                try:
                    submittedSolutions = y.find('div').text
                    data['submittedSolutions'] = submittedSolutions
                except:
                    data['submittedSolutions'] = ""
            if(parse == 4):
                try:
                    aTag = y.find('a')
                    data['accuracy'] = aTag.text
                    data['statusLink'] = "https://www.codechef.com" +  aTag.get('href')
                except:
                    data['accuracy'] = ""
                    data['statusLink'] = ""
            parse+=1 
        data['difficulty'] = t
        globalData.append(data)

for x in globalData:
    print(x)

df = pd.DataFrame.from_dict(globalData)
df.to_csv("codechef.csv")
        
