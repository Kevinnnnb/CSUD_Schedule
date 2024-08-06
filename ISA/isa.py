from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from bs4 import BeautifulSoup
import threading
import sys

# Eventuellement, demander à l'utilisateur de saisir son mail et mot de passe
username = 'kevin.bourquenoud@studentfr.ch'
password = 'UC9z37h8mn'

# Eventuellement, faire en sorte d'utiliser FireFox pour une plus grande compatibilité
driver = webdriver.Safari()

print('\nExecuting script. Please wait\n')
time.sleep(2)
print('Logging into IS-Academia ...\n')
print('!!! AJOUTER LE TRUC POUR GERRER LES COOKIES MAIS DU COUP FAUT AUSSI AJOUTER LA POSSIBILITE DE GERRER LA CONNEXION EN FONCTION DES COOKIES SINON CA VEUT PAS JOEUR !!!\n')

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

def extract_data_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    extracted_data = {
        'date': '',
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
            elif 'date' in title_text.lower():
                extracted_data['date'] = data_value

        return extracted_data
    else:
        print("No div with id 'collapsible11' found.")
        return None

def input_with_timeout(prompt, timeout):
    """
    Prompt user input with a timeout.
    
    Parameters:
    prompt (str): The prompt message to display.
    timeout (int): The time in seconds to wait for input.
    
    Returns:
    str: The user input if provided within the timeout period, otherwise None.
    """
    def ask_input():
        nonlocal user_input
        user_input = input(prompt)
    
    user_input = None
    input_thread = threading.Thread(target=ask_input)
    input_thread.start()
    input_thread.join(timeout)
    
    if input_thread.is_alive():
        return None
    return user_input

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
    
    verification_code = input_with_timeout("Enter the SMS verification code you received: ", 45)
    if verification_code is None:
        raise TimeoutError("No input received within the timeout period.")
    
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
        date = extracted_data.get('date')
        periode = extracted_data.get('periode')
        room = extracted_data.get('room')
        matiere = extracted_data.get('matiere')
        enseignant = extracted_data.get('enseignant')

        print('---------------------------------------------------\n')
        print(f'Data - prochain cours:\n\nDate: {date}\nPériode: {periode}\nSalle: {room}\nMatière: {matiere}\nEnseignant: {enseignant}\n')
        print('---------------------------------------------------\n')

except TimeoutError as te:
    print('\n\n---------------------------------------------------')
    print(f'\nSorry, something bad happened. Please check your Login informations and try again ...\n')
    erreur = True
    

except Exception as e:
    print('\n\n---------------------------------------------------')
    print(f'\nSorry, something bad happened. Please try again later ...\n')
    
    

finally:
    driver.quit()
    if 'xml_content' in locals() and xml_content is not None:
        print('Done Successfully !\n')
    else:
        if erreur is not True:
            print('Something bad happened ...\n')