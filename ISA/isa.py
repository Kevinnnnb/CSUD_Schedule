from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pickle
from bs4 import BeautifulSoup
import threading

# Eventuellement, demander à l'utilisateur de saisir son mail et mot de passe
username = 'kevin.bourquenoud@studentfr.ch'
password = 'UC9z37h8mn'

cookies_file = "/Users/kevin/Desktop/cookies.pkl"

# Variable pour gérer l'état de la connexion
logged_in_with_cookies = False

driver = webdriver.Safari()

erreur = False

print('\nStarting, please wait while we log you into IS-Academia ...\n')

def save_to_local_file(content, file_path):
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
        print("No div with id 'collapsible11' found\n")
        return None

def input_with_timeout(prompt, timeout):
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

def save_cookies(driver, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)

        logged_in_with_cookies = True
    else:
        #print("No cookies found, we are going to log you in ...\n")
        pass

def reconnect_with_cookies(driver, url, cookies_file):
    try:
        #print("Attempting to load page with cookies\n")
        driver.get(url)
        time.sleep(5)
        
        if os.path.exists(cookies_file) and os.path.getsize(cookies_file) > 0:
            #print("Loading cookies from file...\n")
            load_cookies(driver, cookies_file)
            driver.refresh()
            time.sleep(5)
            #print("Cookies loaded and page refreshed.\n")
            return True
        
        else:
            #print("Cookies file does not exist or is empty. We are going to log you in the classic way ...\n")
            return False
    except Exception as e:
        print(f"An error occurred during reconnection: {e}\n")
        return False

try:
    url = "https://appls.edufr.ch/isaweb/!PORTAL17S.portalCell?ww_k_cell=456253168&zz_b_firstloading=1&ww_n_cellkey=696656199&ww_n_ctrlKey=330989937"
    
    logged_in_with_cookies = reconnect_with_cookies(driver, url, cookies_file)

    if  logged_in_with_cookies == False :
        print("Trying to log you in\n")
        driver.get(url)
        time.sleep(5)
        
        #print("Entering username\n")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "loginfmt"))
        )
        username_field.send_keys(username)
        
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        submit_button.send_keys(Keys.RETURN)
        time.sleep(5)
        
        #print("Entering password\n")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "passwd"))
        )
        password_field.send_keys(password)
        
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        submit_button.send_keys(Keys.RETURN)
        time.sleep(5)

        #print("Getting sms verification\n")
        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tile-img"))
        )
        image_element.click()
        time.sleep(5)
        
        verification_code = input_with_timeout("Enter the SMS verification code you received: ", 45)
        if verification_code is None:
            raise TimeoutError("No input received within the timeout period.")
        
        #print("\nVerifying verification code ...\n")
        verification_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idTxtBx_SAOTCC_OTC"))
        )
        verification_field.send_keys(verification_code)
        
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "idSubmit_SAOTCC_Continue"))
        )
        submit_button.send_keys(Keys.RETURN)
        time.sleep(5)
        
        final_submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        final_submit_button.send_keys(Keys.RETURN)
        time.sleep(5)
        save_cookies(driver, cookies_file)

    else:
        #print('Connecting with cookies\n')
        pass
        
    
    driver.switch_to.window(driver.window_handles[-1])
    new_tab_url = "https://appls.edufr.ch/isaweb/!PORTAL17S.portalCell?ww_k_cell=456253168&zz_b_firstloading=1&ww_n_cellkey=696656199&ww_n_ctrlKey=330989937"
    #print("Opening new tab\n")
    driver.get(new_tab_url)
    time.sleep(5)

    #print("Saving page source\n")
    page_source = driver.page_source
    xml_content = page_source

    file_path = "/Users/kevin/Desktop/test.html"
    save_to_local_file(xml_content, file_path)

    #print("Extracting data from HTML\n")
    extracted_data = extract_data_from_html(file_path)

    if extracted_data:
        print('\n\n                 ACCESS GRANTED !\n\n')
        date = extracted_data.get('date')
        periode = extracted_data.get('periode')
        room = extracted_data.get('room')
        matiere = extracted_data.get('matiere')
        enseignant = extracted_data.get('enseignant')

        print('-------------- Data - prochain cours --------------\n')
        print(f'Date: {date}\nPériode: {periode}\nSalle: {room}\nMatière: {matiere}\nEnseignant: {enseignant}\n')
        print('---------------------------------------------------\n')

except TimeoutError as te:
    print('---------------------------------------------------')
    print(f'\nSorry, something bad happened. Please check your Login informations and try again ...\n')
    erreur = True

except Exception as e:
    print('---------------------------------------------------')
    print(f'\nSorry, something bad happened. Please try again later ...\n')
    print(f'Error: {e}\n')

finally:
    driver.quit()
    if 'xml_content' in locals() and xml_content is not None:
        print('\n################ End of the Script ################\n\n')
    else:
        if not erreur:
            print('Something bad happened ...\n')