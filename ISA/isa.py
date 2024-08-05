from selenium import webdriver 
from selenium.webdriver.common.by import By
import time

driver = webdriver.Safari()

try:
    url = "https://appls.edufr.ch/isaweb/!PORTAL17S.portalCell?ww_k_cell=456253168&zz_b_firstloading=1&ww_n_cellkey=696656199&ww_n_ctrlKey=330989937"
    driver.get(url)

    time.sleep(5)  

    data_elements = driver.find_elements(By.XPATH, "//data[@data]")
    
    for elem in data_elements:
        print(elem.get_attribute('outerHTML'))

finally:
    driver.quit()