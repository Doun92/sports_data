from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import time

main_url = "https://olympics.com"

# Au besoin, si je dois attendre un peu
def wait(n):
    time.sleep(n)

# à la fin
def close_driver(d):
    d.close()

def refuse_cookies(d):
    wait(10)
    refuse = d.find_element(By.ID, 'onetrust-reject-all-handler')
    d.execute_script("arguments[0].click();", refuse)

def get_liste_discplines_and_results_urls(d):
    section = d.find_element(By.ID,"globalTracking").find_element(By.TAG_NAME,"section")
    disciplin_section = section.find_elements(By.TAG_NAME,"section")
    liste_disciplines = disciplin_section[1].find_elements(By.TAG_NAME, "a")

    urls_list = []
    for discipline in liste_disciplines:
        # print(discipline.find_element(By.TAG_NAME,"p").get_attribute("innerHTML"))
        # print(discipline.get_attribute("href"))
        urls_list.append(discipline.get_attribute("href"))
    return urls_list


def navigate_main_page(d):
    window = d.find_element(By.ID, 'globalTracking')
    overview_section = window.find_element(By.CLASS_NAME, 'overview')
    left_section = overview_section.find_elements(By.TAG_NAME, 'section')[0]
    right_section = overview_section.find_elements(By.TAG_NAME, 'section')[1]

    #POUR CSV
    titre = left_section.find_element(By.TAG_NAME, 'h2').text
    dates = right_section.find_elements(By.TAG_NAME, 'div')[0].get_attribute('innerHTML').split("</span>",1)[1]
    pays = right_section.find_elements(By.TAG_NAME, 'div')[1].get_attribute('innerHTML').split("</span>",1)[1]
    nb_athlètes = right_section.find_elements(By.TAG_NAME, 'div')[2].get_attribute('innerHTML').split("</span>",1)[1]
    équipes = right_section.find_elements(By.TAG_NAME, 'div')[3].get_attribute('innerHTML').split("</span>",1)[1]
    épreuves = right_section.find_elements(By.TAG_NAME, 'div')[4].get_attribute('innerHTML').split("</span>",1)[1]

    print(f"Titre des jeux: {titre}")
    print(f"Dates: {dates}")
    print(f"Pays d'accueil: {pays}")
    print(f"Nombre d'athlètes: {nb_athlètes}")
    print(f"Nombre d'équipes: {équipes}")
    print(f"Nombre d'épreuves: {épreuves}")

def navigate_disciplines(d):
    section = d.find_element(By.ID,"globalTracking").find_element(By.TAG_NAME,"section")
    discipline_section = section.find_elements(By.CLASS_NAME, "sc-e1befe53-0")

    urls_list = []
    for discipline in discipline_section:
        # print(discipline.get_attribute("innerHTML"))
        list_anchors = discipline.find_elements(By.TAG_NAME, "a")
        for anchor in list_anchors:
            urls_list.append(anchor.get_attribute("href"))

    liste_finale = []
    for item in urls_list:
        if "results" in item:
            liste_finale.append(item)
    liste_finale = list(dict.fromkeys(liste_finale))
    return liste_finale

# Départ du scrapping
def open_web(url):
    driver = webdriver.Firefox()
    driver.get(url)

    refuse_cookies(driver)

    return driver    

# driver = open_web(f"{main_url}/fr/olympic-games/athens-1896")
# navigate_main_page(driver)
# close_driver(driver)

# wait(5)

driver_results = open_web(f"{main_url}/fr/olympic-games/seo/disciplines/athens-1896")
liste_urls = get_liste_discplines_and_results_urls(driver_results)
# print(liste_urls)
close_driver(driver_results)

for url in liste_urls:
    driver_disciplines = open_web(url)
    all_results_urls = navigate_disciplines(driver_disciplines)
    close_driver(driver_disciplines)
    # print(all_results_urls)
    """
    À continuer ici
    On prend chaque url de la liste avec une boucle for et on continuer à chercher en rouvrant un driver.
    Toujours les fermer ensuite (ça commence à devenir n'importe quoi.)
    """