#!/usr/bin/env python3

# Learning Python - Planszeo Best Deals!
# Since I am interested in board games, I browse the best deals at Planszeo.pl.
# Browsing through all the pages is quite tiring and keeping track of changes 
# is difficult, so I created this script for my convenience.

import glob
import pickle
import requests
import time
import sys
import os
from datetime import datetime
from bs4 import BeautifulSoup
from operator import itemgetter

# Function retrieving pages from web
def getdatafromweb(url: str ):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36', 
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
               'Accept-Language': 'pl,en-GB;q=0.9,en;q=0.8,pl-PL;q=0.7'}

    try:
        response = requests.get(url, headers=headers, timeout=120)
    except requests.exceptions.RequestException as e:
        print('Request failed on URL: ', url)
        sys.exit(e)
    return response

# Function retrieving all pages from https://planszeo.pl/okazje and parse html data do list
def getplanszeo() -> list:
    page = 1
    last = 1
    url = 'https://planszeo.pl/okazje?page='
    result = []

    while page <= last:
        
        print("... retrieving page", str(page), end='', flush=True)
        tis = time.time()
        response = getdatafromweb(url+str(page))
        tie = time.time()
        print(f" - it takes {tie-tis} seconds")
        soup = BeautifulSoup(response.content, 'html.parser')
        if page == 1:
            try:
                last = soup.find("i", class_="fa-angle-double-right").parent['href']
                last = last[last.find("page=")+5:]
                print(f"... found {last} pages")
                last = int(last)
            except:
                print(f"... found only one page (check it!)")

        games = soup.find_all("div", class_="grid grid-cols-12 gap-1 lg:gap-2")
        for game in games:
            result.append([game.find("div", class_="text-xl w-full text-gray-600 font-extrabold").text,
                        int(game.find_all("div", class_="text-lg")[0].text.strip()[1:].strip("%")),
                        float(game.find("div", class_="text-purple-600 font-extrabold").text.strip().strip(" zł").replace(",","."))])
        print("... delay 1 sec")
        time.sleep(1) 
        page += 1
    
    return result

# Function listing cache files and asking the user to select specific ones 
def choosedata(start: int, end: int) -> int:
    for i in range(start,end):
        print(f"    {i+1}. {datetime.strftime( datetime.strptime(cache_files[i][ln:ln+10], '%Y%m%d%H'), '%Y-%m-%d g.%H')}")
    while True:
        d = input(f"... Enter number from {start+1} to {end} (default: {start+1}):")
        if d == "":
            return start+1
        if d.isnumeric() and int(d) > start and int(d) <= end:
            return int(d)



print("\n### Best deals not only for Black Week by Planszeo.pl ###\n")

# Path to current cache file
path_cache = os.path.basename(__file__).split('.')[0] + "_" + time.strftime('%Y%m%d%H') + ".cache"

# Make current cache file if doesn't exits
if os.path.exists(path_cache):
    print(f"... Founded cache file for current hour, retrieving new data omitted")
else:
    print("... I can't find cache file for current hour, starting retrieving new data!")
    temp = getplanszeo()
    with open(path_cache, "wb") as f:
        pickle.dump(temp, f)
    print(f"... cache file created in {path_cache}")

# Get names of all cache files, count and sort them
cache_files = glob.glob(os.path.basename(__file__).split('.')[0]+"_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].cache")
count = len(cache_files)
cache_files.sort(reverse=True)

# If there is only 1 cache file - show it, if are more cache files user can chose two to compare.
if count >= 2:
    ln = len(os.path.basename(__file__).split('.')[0])+1

    print("\n... Please, choose newer data:")
    c1 = choosedata(0,count-1)

    print("\n... Please, choose older data: ")
    c2 = choosedata(c1,count)

    with open(cache_files[c1-1], "rb") as f:
        cache1 = pickle.load(f)
    with open(cache_files[c2-1], "rb") as f:
        cache2 = pickle.load(f)

    helper = dict( map(lambda i: (i[0], i[2]), cache2) )

elif count == 1:
    print("... too less cache files found, so loading only last cached data\n")
    with open(cache_files[0], "rb") as f:
        cache1 = pickle.load(f)
else:
    exit("!!! Something wrong, there are no data !!!")

# Get longest title to cut and fill up line with dots
l = max( map(lambda i: len(i[0]), cache1) )
cache1.sort(key=itemgetter(0))
counter = 0
print("\nResults (@ - new position, $ - changed price)")

# Show list of best deals (chosen cache)
for i in cache1:
    counter += 1
    temp = f"{counter}. {i[0]:.<{l}} - {i[2]:.2f} zł ({i[1]}%)"
    if count == 1 or i in cache2:
        print("  "+temp)
    elif i[0] in helper:
        if i[2] == helper.get(i[0]):
            print("  "+temp)
        else:
            print("$ " + temp + f" < {helper.get(i[0]):.2f} zł")
    else:
        print("@ "+temp)
        