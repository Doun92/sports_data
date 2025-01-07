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
    position_tag = tag.find_element(By.TAG_NAME, "div")
    position = position_tag.get_attribute("title")
    if position:
        return position
    else:
        return "Aucune position"

def get_country(tag):
    country_tag = tag.find_element(By.TAG_NAME, "span")
    country = country_tag.get_attribute("innerHTML")
    return country

def get_athlete(tag):
    try:
        biographie = tag.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        pass
    athlete = tag.find_element(By.CSS_SELECTOR, "h3[data-cy='athlete-name']").get_attribute("innerHTML").title()
    return(athlete)


def get_result(tag):
    try:
        span_tag = tag.find_element(By.TAG_NAME, "span")
        if "result-row" in span_tag.get_attribute("data-cy"):
            # print("Résultat")
            resultat = span_tag.find_element(By.CSS_SELECTOR, "span[data-cy='result-info-content']").get_attribute("innerHTML")
            return resultat
    except:
        pass

def get_results(d, sport, discipline):
    all_data_rows = d.find_elements(By.CSS_SELECTOR, "div[data-cy='single-athlete-result-row']")
    # print(len(all_data_rows))
    for data in all_data_rows:
        # print(data.get_attribute("innerHTML"))
        list_divs = data.find_elements(By.TAG_NAME, "div")
        dic_results = {}
        dic_results["sport"] = sport
        dic_results["discipline"] = discipline
        for div in list_divs:
            data_cy_attribute = div.get_attribute("data-cy")
            if data_cy_attribute:
                # Médailles ou positions
                if "medal-row" in data_cy_attribute:
                    position = get_position(div)
                    if position:
                        dic_results["position"] = position

                # Pays
                if "flag-row" in data_cy_attribute:
                    country = get_country(div)
                    if country:
                        dic_results["pays"] = country

                # Nom de l'athlète
                if  "athlete-row"in data_cy_attribute:
                    athlete = get_athlete(div)
                    if athlete:
                        dic_results["athlète"] = athlete
                        
            # Résultats
            resultat = get_result(div)
            if resultat:
                dic_results["résultat"] = resultat

        if "résultat" not in dic_results:
            dic_results["résultat"] = "Aucune donnée"


        print(dic_results)

        add_to_csv(list(dic_results.values()),"résultats")

# Départ du scrapping
def open_web(url):
    driver = webdriver.Firefox()
    driver.get(url)

    refuse_cookies(driver)

    return driver    

def add_to_csv(data, type):
    this_folder = os.getcwd()
    if type == "résumé_jeux":
        with open(f"{this_folder}\\data\\jeux_olympiques_résumé.csv", "a", encoding="utf-8", newline='') as data_file:
            wr = csv.writer(data_file)
            wr.writerow(data)
    elif type == "résultats":
        with open(f"{this_folder}\\data\\résultats.csv", "a", encoding="utf-8", newline='') as data_file:
            wr = csv.writer(data_file)
            wr.writerow(data)

# driver = open_web(f"{main_url}/fr/olympic-games/athens-1896")
# résumé_jeux = navigate_main_page(driver)
# add_to_csv(résumé_jeux, "résumé_jeux")
# close_driver(driver)


wait(5)

driver_results = open_web(f"{main_url}/fr/olympic-games/seo/disciplines/athens-1896")
liste_urls = get_liste_discplines_and_results_urls(driver_results)
close_driver(driver_results)

for i, url in enumerate(liste_urls):
    driver_disciplines = open_web(url)
    all_results_urls = navigate_disciplines(driver_disciplines)
    close_driver(driver_disciplines)
    for j, results_url in enumerate(all_results_urls):
            sport = url.split("/")[-1]
            discipline = results_url.split("/")[-1]
            driver_disciplines = open_web(results_url)
            get_results(driver_disciplines, sport, discipline)
            close_driver(driver_disciplines)