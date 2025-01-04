from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
import os

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

    return [titre,dates,pays,nb_athlètes,équipes,épreuves]

    # print(f"Titre des jeux: {titre}")
    # print(f"Dates: {dates}")
    # print(f"Pays d'accueil: {pays}")
    # print(f"Nombre d'athlètes: {nb_athlètes}")
    # print(f"Nombre d'équipes: {équipes}")
    # print(f"Nombre d'épreuves: {épreuves}")

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

def get_position(tag):
    # print(tag.get_attribute("innerHTML"))
    try:
        test_data = tag.get_attribute("data-cy")
        if "medal-row" in  test_data:
            print("Position")
            # print(f"test_data={test_data}")
            position_tag = tag.find_element(By.TAG_NAME, "div")
            position = position_tag.get_attribute("title")
            if position:
                print(position)
                return position
            else:
                return "Aucune position"
    except:
        pass

def get_country(tag):
    try:
        test_data = tag.get_attribute("data-cy")
        if "flag-row" in test_data:
            print("Pays")
            country_tag = tag.find_element(By.TAG_NAME, "span")
            country = country_tag.get_attribute("innerHTML")
            print(country)
            return country
    except:
        pass

def get_athlete(tag):
    try:
        test_data = tag.get_attribute("data-cy")
        if "athlete-row" in test_data:
            print("Athlète")
            biographie = tag.find_element(By.TAG_NAME, "a").get_attribute("href")
            athlete = tag.find_element(By.TAG_NAME, "h3").get_attribute("innerHTML").title()
            print(athlete)
            return(athlete)
    except:
        pass

def get_result(tag):
    try:
        span_tag = tag.find_element(By.TAG_NAME, "span")
        if "result-row" in span_tag.get_attribute("data-cy"):
            print("Résultat")
            resultat = span_tag.find_element(By.CSS_SELECTOR, "span[data-cy='result-info-content']").get_attribute("innerHTML")
            print(resultat)
            return resultat
    except:
        pass

def get_results(d):
    all_data_rows = d.find_elements(By.CSS_SELECTOR, "div[data-cy='single-athlete-result-row']")
    # print(len(all_data_rows))
    for data in all_data_rows:
        # print(data.get_attribute("innerHTML"))
        list_divs = data.find_elements(By.TAG_NAME, "div")
        list_results = []
        for div in list_divs:
            # Médailles ou positions
            position = get_position(div)
            if position:
                list_results.append(position)
            # Pays
            country = get_country(div)
            if country:
                list_results.append(country)
            # Nom de l'athlète
            athlete = get_athlete(div)
            if athlete:
                list_results.append(athlete)
            # Résultats
            resultat = get_result(div)
            if resultat:
                list_results.append(resultat)

        print(list_results)
            # print(f"Athlète = {athlete}")
            # print(f"Position = {position}")
            # print(f"Pays = {country}")
            # print(f"Résultat = {resultat}")
# Départ du scrapping
def open_web(url):
    driver = webdriver.Firefox()
    driver.get(url)

    refuse_cookies(driver)

    return driver    

def add_to_csv(liste, type):
    this_folder = os.getcwd()
    if type == "résumé_jeux":
        """
        TODO
        Ajouter une vérification si la lgine existe déjà ou pas.
        """
        with open(f"{this_folder}\\data\\jeux_olympiques_résumé.csv", "a", encoding="utf-8", newline='') as data_file:
            wr = csv.writer(data_file)
            wr.writerow(liste)


driver = open_web(f"{main_url}/fr/olympic-games/athens-1896")
résumé_jeux = navigate_main_page(driver)
add_to_csv(résumé_jeux, "résumé_jeux")
close_driver(driver)


wait(5)

driver_results = open_web(f"{main_url}/fr/olympic-games/seo/disciplines/athens-1896")
liste_urls = get_liste_discplines_and_results_urls(driver_results)
# print(liste_urls)
close_driver(driver_results)

for url in liste_urls:
    driver_disciplines = open_web(url)
    all_results_urls = navigate_disciplines(driver_disciplines)
    close_driver(driver_disciplines)
    # print(all_results_urls)
    for results_url in all_results_urls:
        driver_disciplines = open_web(results_url)
        get_results(driver_disciplines)
        close_driver(driver_disciplines)

"""
Créer le csv
"""