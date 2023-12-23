#!/usr/bin/env python3

# Learning Python and Selenium
# Logging to BoardGameGeek website
# (CLI + Selenium)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from getpass import getpass
import sys
import time

driver = webdriver.Chrome()

driver.get("https://boardgamegeek.com")


driver.implicitly_wait(2)
btnLogin = driver.find_element(By.XPATH, "/html/body/gg-app/div/gg-header/header/nav/div/div[1]/div/div[2]/gg-menu-nav-nouser/ul/li[1]/a")

actions = ActionChains(driver)
actions.click(btnLogin)
actions.perform()

def loginBGG() -> bool:
    """ Login to BGG and check if logged """
    
    elUsername = driver.find_element(By.ID, "inputUsername")
    elPassword = driver.find_element(By.ID, "inputPassword")
    elUsername.clear()
    elUsername.send_keys("Przełącz do konsoli i tam podaj dane logowania :-)")
    
    print("Nazwa użytkownika BGG:")
    inputUsername = input()
    print("Hasło użytkownika BGG (" + inputUsername + "):")
    inputPassword = getpass()

    elUsername.clear()
    elPassword.clear()
    elUsername.send_keys(inputUsername)
    elPassword.send_keys(inputPassword)
    actions.click(driver.find_element(By.XPATH, '//*[@id="cdk-dialog-0"]/gg-login-modal/gg-login-form/form/fieldset/div[3]/button[1]'))
    actions.perform()
    
    driver.implicitly_wait(2)
    try:
        err = driver.find_element(By.XPATH, '//*[@id="cdk-dialog-0"]/gg-login-modal/gg-login-form/form/fieldset/div[2]/p')
        print("Komunikat ze strony: " + err.text)
        return False
    except NoSuchElementException:
        return True

### Wywołanie trzech prób logowania do BGG, w przypadku niepowodzenia, wyjście ; )
for i in range(3):
    print(f"Logowanie do BGG ({str(i+1)}/3)\n")
    if loginBGG():
        print("Zalogowano poprawnie :-)\n")
        break
    elif i < 2:
        print("Logowanie poszło źle! Spóbuj raz jeszcze :-)\n")
    else:
        driver.quit()
        sys.exit("Za dużo prób logowania, wyłączam skrypt!")
        

print("Pacnij enter, aby się wylogować!")
input()
print("Papa!")
driver.get("https://boardgamegeek.com/logout")
time.sleep(5)
driver.quit()
