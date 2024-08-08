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


i = 1
time_running = 0

while True:
    print(f'\nIteration : {i} \nTime from start : {time_running} min\n')


    print('Starting script, please wait ...\n')

    time.sleep(2)

    username = 'kevin.bourquenoud@studentfr.ch'
    password = 'UC9z37h8mn'

    cookies_file = "/Users/kevin/Desktop/cookies.pkl"

    driver = webdriver.Safari()

    erreur = False

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
            print("\nNo div with id 'collapsible11' found\n")
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

    def reconnect_with_cookies(driver, url, cookies_file):
        try:
            driver.get(url)
            time.sleep(5)
            
            if os.path.exists(cookies_file) and os.path.getsize(cookies_file) > 0:
                load_cookies(driver, cookies_file)
                driver.refresh()
                time.sleep(5)
                
                # Vérifier si les cookies sont valides en tentant de trouver un élément qui n'est disponible qu'après connexion
                if "Login" in driver.title or "Sign In" in driver.title:
                    print("Cookies invalides ou expirés, reconnectez-vous.")
                    return False
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occurred during reconnection: {e}\n")
            return False

    try:
        url = "https://appls.edufr.ch/isaweb/!PORTAL17S.portalCell?ww_k_cell=456253168&zz_b_firstloading=1&ww_n_cellkey=696656199&ww_n_ctrlKey=330989937"
        
        logged_in_with_cookies = reconnect_with_cookies(driver, url, cookies_file)

        if  logged_in_with_cookies == False :
            driver.get(url)
            time.sleep(5)
            
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "loginfmt"))
            )
            username_field.send_keys(username)
            
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "idSIButton9"))
            )
            submit_button.send_keys(Keys.RETURN)
            time.sleep(5)
            
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "passwd"))
            )
            password_field.send_keys(password)
            
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "idSIButton9"))
            )
            submit_button.send_keys(Keys.RETURN)
            time.sleep(5)

            image_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tile-img"))
            )
            image_element.click()
            time.sleep(5)
            
            verification_code = input_with_timeout("Enter the SMS verification code you received: ", 45)
            if verification_code is None:
                raise TimeoutError("No input received within the timeout period.")
            
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
            print('\n\n                 ACCESS GRANTED !\n\n')
            date = extracted_data.get('date')
            periode = extracted_data.get('periode')
            room = extracted_data.get('room')
            matiere = extracted_data.get('matiere')
            enseignant = extracted_data.get('enseignant')

            print('-------------- Data - prochain cours --------------\n')
            print(f'Date: {date}\nPériode: {periode}\nSalle: {room}\nMatière: {matiere}\nEnseignant: {enseignant}\n')
            print('---------------------------------------------------\n')

            save_cookies(driver, cookies_file)

    except TimeoutError as te:
        print('---------------------------------------------------')
        print(f'\nSorry, something bad happened. Please check your Login informations and try again ...\n')
        erreur = True
        break

    except Exception as e:
        print('---------------------------------------------------')
        print(f'\nSorry, something bad happened. Please try again later ...\n')
        print(f'Error: {e}\n')
        break

    finally:
        driver.quit()
        if 'xml_content' in locals() and xml_content is not None:
            print('\n################ End of the Script ################\n\n')
        else:
            if not erreur:
                print('Something bad happened ...\n')
                break

    i += 1
    time_running += 10


    MAX_RETRIES = 3
    retry_count = 0


    #Faire en sorte d'appuyer sur le bouton "Attendre un nouvel accès" toutes les 10 minutes ou alors touver le lien de la requette mais bon ... 

    #dans la console dev il quand on clique sur le bouton "Attendre un nouvel accès" il y a cette requette /PORTAL17S.htm dans la balise href donc en soit c'est assez simple

    #faudrait peut être juste changer le timeout pour la recherche de l'élément ---- Demander à ChatGPT


    try:
        element = driver.find_element_by_link_text("Attendre un nouvel accès")
        element.click()
    except Exception as e:
        print(f"Erreur lors du clic sur l'élément: {e}")
    submit_button.send_keys(Keys.RETURN)

    time.sleep(5)
    save_cookies(driver, '/Users/kevin/Desktop/cookies.pkl')