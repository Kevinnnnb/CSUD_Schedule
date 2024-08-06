from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import xml.etree.ElementTree as ET

#enentually ask the user to input his mail ans password but that will come later
username = 'kevin.bourquenoud@studentfr.ch'
password = 'UC9z37h8mn'

driver = webdriver.Safari()

print('Executing script...\n')

try:
    url = "https://isa.fr.ch"
    driver.get(url)
    time.sleep(5) 
    
    driver.find_element(By.NAME, "loginfmt").send_keys(username) 
    driver.find_element(By.ID, "idSIButton9").send_keys(Keys.RETURN)
    time.sleep(5)
    driver.find_element(By.NAME, "passwd").send_keys(password)
    driver.find_element(By.ID, "idSIButton9").send_keys(Keys.RETURN)
    time.sleep(5)

    image_element = driver.find_element(By.CLASS_NAME, "tile-img")
    image_element.click()
    time.sleep(5)
    
    verification_code = input("Enter the SMS verification code you received: ")
    
    driver.find_element(By.ID, "idTxtBx_SAOTCC_OTC").send_keys(verification_code) 
    driver.find_element(By.ID, "idSubmit_SAOTCC_Continue").send_keys(Keys.RETURN)
    time.sleep(5) 
    driver.find_element(By.ID, "idSIButton9").send_keys(Keys.RETURN)
    time.sleep(5)

    print('\nACCESS GRANTED !\n')


    driver.switch_to.window(driver.window_handles[-1])
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
    if xml_content is not None:
        print('Done Successfully !\n')
    else:
        print('Something bad happend ...\n')


'''
Penser à ajouter le code pour chocher le fait de rester connecté pour voir si du coup j'arrive à ne pas redemander le code de verification 
(probleme si je fais ça c'est que faudra detecter si j'arrive sur la page d'acceuil ou la page de connection parce que sinon ça va planter ...)
'''