import getpass

from db_connector import shop_db
from selenium import webdriver # main webdriver
from selenium.webdriver.common.keys import Keys # for sending keys

def login(driver):

    username, password = prompts()

    driver.get('https://www.amazon.com')
    driver.implicitly_wait(10)

    signin = driver.find_element_by_id("nav-link-accountList")
    signin.click()

    driver.implicitly_wait(3)
    email_box = driver.find_element_by_id("ap_email")
    email_box.send_keys(username)
    email_box.send_keys(Keys.RETURN)

    # Incorrect username
    driver.implicitly_wait(3)
    alert = driver.find_elements_by_class_name("a-alert-heading")

    if len(alert) >= 1 and alert[0].text.lower() == "there was a problem":
        print("Error: Incorrect Password or Email, try again")
        print()
        login(driver) # Try again

    passwd_box = driver.find_element_by_id("ap_password")
    passwd_box.send_keys(password)
    passwd_box.send_keys(Keys.RETURN)


    # Incorrect Password
    driver.implicitly_wait(3)
    alert = driver.find_elements_by_class_name("a-alert-heading")

    if len(alert) >= 1 and alert[0].text.lower() == "there was a problem":
        print("Error: Incorrect Password or Email, try again")
        print()
        login(driver) # Try again

    # Requires 2FA
    driver.implicitly_wait(3)
    alert = driver.find_elements_by_xpath("//*[@class='a-row a-spacing-small']")

    if len(alert) >= 1 and alert[0].text.lower() == "authentication required":
        print("Error, 2FA is not supported. Please disable or continue without login")
        return 1

    # DATABASE
    userid = getId(username);
    cursor = shop_db.cursor()
    cursor.execute("INSERT INTO User (UserId, Email, Password) VALUES (%s, %s, %s)", (userid, username, password));

    #Commit new entry into the database
    shop_db.commit()



def getId(username):
  values = [ord(c) for c in username]
  total = sum(values)

  return total;

def prompts():
    username= input("Amazon Username/Email: ")
    userid = getId(username)
    password =getpass.getpass(prompt='Amazon Password: ', stream=None)

    return username, password
