#!/usr/bin/python3

# standard
import sys

# external
from selenium import webdriver # main webdriver
from selenium.webdriver.chrome.options import Options # for chrome
from selenium.webdriver.firefox.options import Options as FirefoxOptions # for firefox

# self
from searchAmazon import search
from userlogin import login

def main(nonterm, search_term):

    # Welcome
    if nonterm == 0:
        print("\tWelcome to your Amazon personal shopper bot!\n\t\t\tHappy shopping")
        print()

    driver = parseArguements(nonterm)

    # Login
    userid = -1
    if nonterm == 0:
        print("You are not logged in")
        log = input("Login? (y/n): ")
        if log.lower() == 'y':
          userid =login(driver)

    # Search
    #TODO figure if mysql installed
    use_database = 0
    output = search(driver, userid, use_database, search_term)


    driver.close()
    return output

def parseArguements(nonterm = 0):
    options = Options()

    #run headless chrome (default)
    if nonterm == 1 or len(sys.argv) == 1:
        options.headless = True
        driver = webdriver.Chrome( chrome_options=options)

    # run with chrome GUI
    if len(sys.argv) == 2 and sys.argv[1] == "-g":
        options.headless = False
        driver = webdriver.Chrome( chrome_options=options)

    #run with firefox 32bit
    if len(sys.argv) == 2 and sys.argv[1] == "-f":
        driver=webdriver.Firefox(executable_path=r"./drivers/geckodriver")

    #run with firefox 32bit headless
    if len(sys.argv) ==3 and sys.argv[2] == "-h":
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=r"./drivers/geckodriver", options=options)

    return driver


if __name__ == '__main__':
    main(0, 0) # run in terminal mode
