#!/usr/bin/env python3

""" Learning Python and Selenium

Get 3 best boardgames from BGG
First thing with Selenium
(CLI, Selenium)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://boardgamegeek.com/browse/boardgame")

szukaj_klasy = driver.find_elements(By.CLASS_NAME, "primary")

for i in range(3):
    print(szukaj_klasy[i].text)

driver.quit()
