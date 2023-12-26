#!/usr/bin/env python3

# Learning Python
# 
# Get first result for specified boardgame on BGG
# (CLI, urllib, xml.etree.ElementTree)

import sys
import os
import time
import urllib.parse
from urllib.request import Request, urlopen
from urllib.error import URLError
import xml.etree.ElementTree as ET

def getdatafromweb(url: str ):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

    try:
        response = urlopen( Request(url, {}, headers) )
    except URLError as e:
        if hasattr(e, 'reason'):
            print('Urllib. We failed to reach a server.')
            print('Urllib. Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('Urllib. The server couldn\'t fulfill the request.')
            print('Urllib. Error code: ', e.code)
        print('Urllib. URL: ', url)
        sys.exit()
    # print( response.info() )
    return response.read()

def getfromxml(tree, xpath: str, attr: str):
    f = tree.find(xpath)
    if f is None:
        return '(n/a)'
    return f.get(attr)

if len(sys.argv) < 2:
    print("\nPlease, enter the search pharse:")
    print(f"    python {os.path.basename(__file__)} search")
    print(f"    ex. python {os.path.basename(__file__)} neuroshima hex\n")
    sys.exit()

search = " ".join(sys.argv[1:])

if len(search) < 3:
    print("\nSearch pharse at least 3 characters long!")
    print(f"'{search}' is too short.\n")
    sys.exit()

print(f"\nI will try to find for you a game called: {search.title()}\n")

# Try to find a game and game's ID

url = 'https://boardgamegeek.com/xmlapi2/search?type=boardgame&query='+urllib.parse.quote_plus(search)

tree = ET.fromstring( getdatafromweb(url).decode('UTF-8') )

if int(tree.attrib['total']) == 0:
    print(f"Oh no! There is not a '{search}' in BGG database!")
    sys.exit()

gameid = tree[0].attrib['id']

# Reciving information about a game specified by ID

url = 'https://boardgamegeek.com/xmlapi2/thing?stats=1&id='+str(gameid)

tree = ET.fromstring( getdatafromweb(url).decode('UTF-8') )

game_position = getfromxml(tree, "./item/statistics/ratings/ranks/rank[@id='1']", "value")
game_name = getfromxml(tree, "./item/name[@type='primary']", "value")
game_year = getfromxml(tree, "./item/yearpublished", "value")
game_href = 'https://boardgamegeek.com/boardgame/' + str(gameid) + '/'

print("Result")
print(f" - name: {game_name} ({game_year})")
print(f" -  pos: {game_position}")
print(f" - link: {game_href}\n")

print("What is the next mission? ;-)")
