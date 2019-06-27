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

# ## IMPORTS

from lxml import html
import requests
import csv
import datetime
import time

# ## INPUTS

start = "2018-07-01"
end = "2018-12-31"

# ## EXTRACTION

# Conversion of string to datetime objects
start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
end_date = datetime.datetime.strptime(end, "%Y-%m-%d")

# +
# The output file is created with headers
headers = ["name","date","time","going","surface","url"]

with open('links.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
# -

# The while operator makes sure to only extract information between the start and end dates
while start_date <= end_date:
    time.sleep(5)
    print ("\n", start_date)
    
    # Construct the URL for each day and perform the request
    url = "https://www.sportinglife.com/racing/racecards/" + str(start_date.year) + "-" + str(start_date.month) + "-" + str(start_date.day)
    print("Performing requests, please wait...")
    page = requests.get(url)
    tree = html.fromstring(page.content)
    date_or = str(start_date.year) + "-" + str(start_date.month) + "-" + str(start_date.day)

    # Using xpaths, navigate through the content of the site to get to the section that lists all locations and races
    places = tree.xpath('//div[@class="collapsibleSection"]')

    # This for loop goes through each location in which was a race during that day
    for k in places:
        urls = []
        
        # There are some races that were cancelled or rescheduled. This if makes sure to grab the URL of those races that were run
        if k.xpath('div[@class="dividerRow"]/h2/a[not(contains(text(),"OFF"))]') and k.xpath('div[2]/ul/li[1]/div[@class="hr-meeting-race-result-fulllink"]'):
            
            # Using xpaths, get the name, going and surface of each location
            name = k.xpath('div[@class="dividerRow"]/h2/a/text()')[0]
            going = k.xpath('div[2]/div/div[@class="hr-meeting-meta-going"]/span[@class="hr-meeting-meta-value"]/text()')[0]
            surface = k.xpath('div[2]/div/div[@class="hr-meeting-meta-surface"]/span/text()')[0]
            print("\t" + name)

            # Perform a for loop through the races in each location
            races = k.xpath('div[2]/ul/li')
            for l in races:
                
                # Use xpaths to get the url and the time of each race
                link = "https://www.sportinglife.com" + l.xpath('a/@href')[0]
                time_or = l.xpath('a/span/text()')[0]
                
                # For each race, append the extracted information to a list
                urls.append([name,date_or,time_or,going,surface,link])
        
        # Write the list of URLs and race information to the csv file. This operation is done for every location of every day
        with open('links.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerows(urls)
    
    # Increment the start_date variable by one day
    start_date += datetime.timedelta(days=1)

    
