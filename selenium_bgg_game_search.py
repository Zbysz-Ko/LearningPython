#!/usr/bin/env python3

""" Learning Python and Selenium

Get first result for specified boardgame on BGG
(CLI and Selenium)
"""

import sys
import os
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

if len(sys.argv) < 2:
    print("\nPlease, enter the search phrase:")
    print(f"    python {os.path.basename(__file__)} search")
    print(f"    ex. python {os.path.basename(__file__)} neuroshima hex\n")
    sys.exit()

search = " ".join(sys.argv[1:])

if len(search) < 3:
    print("\nSearch phrase at least 3 characters long!")
    print(f"'{search}' is too short.\n")
    sys.exit()

driver = webdriver.Chrome()

print(f"\nI will try to find for you a game called: {search.title()}\n")

driver.get("https://boardgamegeek.com/geeksearch.php?action=search&objecttype=boardgame&q="
           +urllib.parse.quote_plus(search))

try:
    row = driver.find_element(By.ID, "row_")
except NoSuchElementException:
    print(f"Oh no! There is not a '{search}' in BGG database!")
    driver.quit()
    sys.exit()

class Help:
    """Class is a matching object to be returned if data is missing ;-)"""
    def __init__(self):
        self.text = '(n/a)'
    def get_attribute(self):
        return self.text

def find_by_class(classname: str):
    try:
        return row.find_element(By.CLASS_NAME, classname)
    except NoSuchElementException:
        return Help()

game_position = find_by_class("collection_rank")
game_name = find_by_class("primary")
game_year = find_by_class("smallerfont")

print("Result")
print(f" - name: {game_name.text} {game_year.text}")
print(f" -  pos: {game_position.text}")
print(f" - link: {game_name.get_attribute('href')}\n")

driver.quit()

print("What is the next mission? ;-)")
