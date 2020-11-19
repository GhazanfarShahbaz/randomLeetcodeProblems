import requests
from bs4 import BeautifulSoup
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
# fron sele
import pandas as pd 
import time
from selenium.webdriver.support.ui import Select


tags = {
    "Arrays": "https://leetcode.com/problemset/all/?topicSlugs=array",
    "Hash Table": "https://leetcode.com/problemset/all/?topicSlugs=hash-table",
    "Linked Lists": "https://leetcode.com/problemset/all/?topicSlugs=linked-list",
    "Math": "https://leetcode.com/problemset/all/?topicSlugs=math",
    "Two Pointers": "https://leetcode.com/problemset/all/?topicSlugs=two-pointers",
    "String": "https://leetcode.com/problemset/all/?topicSlugs=string",
    "Binary Search": "https://leetcode.com/problemset/all/?topicSlugs=binary-search",
    "Divide and Conquer": "https://leetcode.com/problemset/all/?topicSlugs=divide-and-conquer",
    "Dynamic Programming": "https://leetcode.com/problemset/all/?topicSlugs=dynamic-programming",
    "Backtracking": "https://leetcode.com/problemset/all/?topicSlugs=backtracking",
    "Stack": "https://leetcode.com/problemset/all/?topicSlugs=stack",
    "Heap": "https://leetcode.com/problemset/all/?topicSlugs=heap",
    'Greedy': "https://leetcode.com/problemset/all/?topicSlugs=greedy",
    "Sort": "https://leetcode.com/problemset/all/?topicSlugs=sort",
    "Bit Manipulation": "https://leetcode.com/problemset/all/?topicSlugs=bit-manipulation",
    "Tree": "https://leetcode.com/problemset/all/?topicSlugs=tree",
    "Depth First Search": "https://leetcode.com/problemset/all/?topicSlugs=depth-first-search",
    "Breadth First Search": "https://leetcode.com/problemset/all/?topicSlugs=breadth-first-search",
    "Union Find": "https://leetcode.com/problemset/all/?topicSlugs=union-find",
    "Graph": "https://leetcode.com/problemset/all/?topicSlugs=graph",
    "Design": "https://leetcode.com/problemset/all/?topicSlugs=design",
    "Topological Sort": "https://leetcode.com/problemset/all/?topicSlugs=topological-sort",
    "Trie": "https://leetcode.com/problemset/all/?topicSlugs=trie",
    "Binary Indexed Tree": "https://leetcode.com/problemset/all/?topicSlugs=binary-indexed-tree",
    "Segment Tree": "https://leetcode.com/problemset/all/?topicSlugs=segment-tree",
    "Binary Search Tree": "https://leetcode.com/problemset/all/?topicSlugs=binary-search-tree",
    "Recursion": "https://leetcode.com/problemset/all/?topicSlugs=recursion",
    "Brain Teaser": "https://leetcode.com/problemset/all/?topicSlugs=brainteaser",
    "Memoization": "https://leetcode.com/problemset/all/?topicSlugs=memoization",
    "Queue": "https://leetcode.com/problemset/all/?topicSlugs=queue",
    "Minimax": "https://leetcode.com/problemset/all/?topicSlugs=minimax",
    "Reservoir Sampling": "https://leetcode.com/problemset/all/?topicSlugs=reservoir-sampling",
    "Ordered Map": "https://leetcode.com/problemset/all/?topicSlugs=ordered-map",
    "Geometry": "https://leetcode.com/problemset/all/?topicSlugs=geometry",
    "Random": "https://leetcode.com/problemset/all/?topicSlugs=random",
    "Rejection Sampling": "https://leetcode.com/problemset/all/?topicSlugs=rejection-sampling",
    "Sliding Window": "https://leetcode.com/problemset/all/?topicSlugs=sliding-window",
    "Line Sweep": "https://leetcode.com/problemset/concurrency/?topicSlugs=line-sweep",
    "Rolling Hash": "https://leetcode.com/problemset/concurrency/?topicSlugs=rolling-hash",
    "Suffix Array": "https://leetcode.com/problemset/concurrency/?topicSlugs=suffix-array"
}

def getData(tag, link, data):
    driver = webdriver.Safari()
    driver.get(link)
    try:
        Select(driver.find_element_by_xpath('//select[@class = "form-control"]'))
        # select.select_by_value('9007199254740991')  
    except:
        driver.close()
        return
    try:
        driver.find_element_by_xpath('//select[@class = "form-control"]').click()
        select = Select(driver.find_element_by_xpath('//select[@class = "form-control"]'))
        select.select_by_visible_text('all')
    except:
        driver.close()
        return

    start = True
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    for trTags in soup.find_all("tr"):
        if(start):
            start = False
            continue
        else:
            parser = 0
            for row in trTags.find_all('td'):
                if parser == 1:
                    data[int(row.text.strip())].append(tag)
                parser += 1 

    driver.close() 

def dataByTag():
    data = {index: [] for index in range(1,1660)}
    # print(data)

    for tag, link in tags.items():
        print(tag)
        getData(tag, link, data)

        # time.sleep(2)
    print(data)
    df = pd.DataFrame.from_dict(data, orient='index')
    # df = df.transpose()
    try:
        df.to_csv("tagData.csv")
    except:
        df = df.transpose()
        df.to_csv("tagData.csv")
    else:
        df.to_csv("tagData.csv")



    




if __name__ == "__main__":
    dataByTag()