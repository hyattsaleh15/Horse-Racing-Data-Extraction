# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import csv
import requests
from lxml import html
import time
import numpy as np

data = pd.read_csv("links.csv")

data.head()

# +
headers = ["location","date","time","going","surface","lenght","pos","distance_ff","stall","h_name","h_age","weight","odds","trainer","jockey"]

first_row = 5108

if first_row == 0:
    with open("data.csv",'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

# -

for index, row in data.iterrows():

    if index < first_row:
        continue
    
    url = row["url"]
    #url = "https://www.sportinglife.com/racing/results/2018-07-01/curragh/480933/lyndsey-and-eleanor-comer-trust-handicap-premier-handicap"
    url = url.replace("racecards","results").replace("racecard/","")
    
    time.sleep(np.random.uniform(1,4))
    
    page = requests.get(url)
    tree = html.fromstring(page.content)
    
    lenght = tree.xpath('//li[@class="hr-racecard-summary-race-distance hr-racecard-summary-always-open"]/text()')[0]
    
    main = [row["name"],row["date"],row["time"],row["going"],row["surface"],lenght]
    entries = []
    
    horses = tree.xpath('//div[@class="hr-racing-racecard-wrapper"]/div/section/section[@class="hr-racing-runner-wrapper"]')
    for i in horses:
        entry = main.copy()
        
        pos = "N/A"
        if i.xpath('div/div/div/span[@class="hr-racing-runner-position-no"]/span/text()'):
            pos = i.xpath('div/div/div/span[@class="hr-racing-runner-position-no"]/span/text()')[0]
        entry.append(pos)
                
        dist = 0
        if i.xpath('div/div[@class="hr-racing-runner-space-from-winner"]/text()'):
            dist = i.xpath('div/div[@class="hr-racing-runner-space-from-winner"]/text()')[0]
        entry.append(dist)
        
        stall = "N/A"
        if i.xpath('div/div/div/span[@class="hr-racing-runner-saddle-cloth-no"]/text()'):
            stall = i.xpath('div/div/div/span[@class="hr-racing-runner-saddle-cloth-no"]/text()')[0]
        entry.append(stall)
        
        name = "N/A"
        if i.xpath('div/div/div/span[@class="hr-racing-runner-horse-name"]/a/text()'):
            name = i.xpath('div/div/div/span[@class="hr-racing-runner-horse-name"]/a/text()')[0]
        entry.append(name)
        
        age = "N/A"
        if i.xpath('div/div[@class="hr-racing-runner-horse-info"]/div[2]/div/span[1]/text()'):
            age = i.xpath('div/div[@class="hr-racing-runner-horse-info"]/div[2]/div/span[1]/text()')[0]
        entry.append(age)
        
        weight = "N/A"
        if i.xpath('div/div[@class="hr-racing-runner-horse-info"]/div[2]/div/span[2]/text()'):
            weight = i.xpath('div/div[@class="hr-racing-runner-horse-info"]/div[2]/div/span[2]/text()')[0]
        entry.append(weight)
        
        odds = "N/A"
        if i.xpath('div/div[@class="hr-racing-runner-betting-odds"]/span/text()'):
            odds = i.xpath('div/div[@class="hr-racing-runner-betting-odds"]/span/text()')[0]
        entry.append(odds)
        
        trainer = "N/A"
        if i.xpath('div/div/div/a[@class="hr-racing-runner-form-trainer"]/span/text()'):
            trainer = i.xpath('div/div/div/a[@class="hr-racing-runner-form-trainer"]/span/text()')[0]
        entry.append(trainer)
        
        jockey = "N/A"
        if i.xpath('div/div/div/a[@class="hr-racing-runner-form-jockey"]/span[1]/text()'):
            jockey = i.xpath('div/div/div/a[@class="hr-racing-runner-form-jockey"]/span[1]/text()')[0]
        entry.append(jockey)
        
        entries.append(entry)

    with open('data.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerows(entries)
        
    print(index, "/", len(data))


