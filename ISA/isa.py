from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from bs4 import BeautifulSoup

# Eventuellement, demander à l'utilisateur de saisir son mail et mot de passe
username = 'kevin.bourquenoud@studentfr.ch'
password = 'UC9z37h8mn'

driver = webdriver.Safari()

print('\nExecuting script. Please wait while we log you in...\n')

def save_to_local_file(content, file_path):
    """
    Save the content to a local file at the specified file path.
    
    Parameters:
    content (str): The content to be saved.
    file_path (str): The full path of the file where the content will be saved.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f'Content successfully saved to {file_path}\n')

def extract_data_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    extracted_data = {
        'periode': '',
        'room': '',
        'matiere': '',
        'enseignant': ''
    }

    collapsible_div = soup.find('div', id='collapsible11')

    if collapsible_div:
        span_elements = collapsible_div.find_all('span', class_='text')

        for span in span_elements:
            title_tag = span.find_previous('span', class_='tag')
            title_text = title_tag.get_text(strip=True) if title_tag else 'Title Not Found'

            data_tag = span.find_next('data')
            data_value = span.get_text(strip=True) + ' ' + data_tag.get_text(strip=True) if data_tag else span.get_text(strip=True)

            if 'periode' in title_text.lower():
                extracted_data['periode'] = data_value
            elif 'room' in title_text.lower():
                extracted_data['room'] = data_value
            elif 'matiere' in title_text.lower():
                extracted_data['matiere'] = data_value
            elif 'enseignant' in title_text.lower():
                extracted_data['enseignant'] = data_value

        return extracted_data
    else:
        print("No div with id 'collapsible11' found.")
        return None

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

    file_path = "/Users/kevin/Desktop/test.html"
    save_to_local_file(xml_content, file_path)

    extracted_data = extract_data_from_html(file_path)

    if extracted_data:
        periode = extracted_data.get('periode')
        room = extracted_data.get('room')
        matiere = extracted_data.get('matiere')
        enseignant = extracted_data.get('enseignant')

        print('---------------------------------------------------\n')
        print(f'Data - prochain cours:\n\nPériode: {periode}\nSalle: {room}\nMatière: {matiere}\nEnseignant: {enseignant}\n')
        print('---------------------------------------------------\n')

finally:
    driver.quit()
    if xml_content is not None:
        print('\nDone Successfully !\n')
    else:
        print('Something bad happened ...\n')