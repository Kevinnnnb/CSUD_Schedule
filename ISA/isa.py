from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import xml.etree.ElementTree as ET

username = 'kevin.bourquenoud@studentfr.ch'
password = 'UC9z37h8mn'

driver = webdriver.Safari()

print('Executing script...\n')

try:
    # Open the login page
    url = "https://isa.fr.ch"
    driver.get(url)
    time.sleep(5) 
    
    driver.find_element(By.NAME, "loginfmt").send_keys(username) 
    time.sleep(5)
    driver.find_element(By.ID, "idSIButton9").send_keys(Keys.RETURN)
    time.sleep(5)
    driver.find_element(By.NAME, "passwd").send_keys(password)
    time.sleep(5)
    driver.find_element(By.ID, "idSIButton9").send_keys(Keys.RETURN)
    time.sleep(5)

    # trying to click on the sms authenticator
    image_element = driver.find_element(By.CLASS_NAME, "tile-img")
    image_element.click()
    time.sleep(5)
    
    verification_code = input("Enter the SMS verification code you received: ")
    
    # Enter the verification code into the appropriate field
    driver.find_element(By.ID, "idTxtBx_SAOTCC_OTC").send_keys(verification_code)  # Update with the actual name attribute
    time.sleep(5)
    driver.find_element(By.ID, "idSubmit_SAOTCC_Continue").send_keys(Keys.RETURN)
    time.sleep(5) 
    driver.find_element(By.ID, "idSIButton9").send_keys(Keys.RETURN)
    time.sleep(0.5)


    driver.switch_to.window(driver.window_handles[-1])
    # Open a new URL in the new tab
    new_tab_url = "https://appls.edufr.ch/isaweb/!PORTAL17S.portalCell?ww_k_cell=456253168&zz_b_firstloading=1&ww_n_cellkey=696656199&ww_n_ctrlKey=330989937"
    driver.get(new_tab_url)
    time.sleep(5) 

    page_source = driver.page_source

    xml_content = page_source

    print('printing page content...\n')
    print(xml_content)
    print('\n')

finally:
    driver.quit()
    print('Done Successfully !\n')