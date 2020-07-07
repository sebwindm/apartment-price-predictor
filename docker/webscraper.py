# https://realpython.com/beautiful-soup-web-scraper-python/

import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import os
from tqdm import tqdm
from docker import database_handler


def scrape_data_from_immoscout(verbose=False, data_dir=os.environ.get('DATA_DIR', '.')):
    """
    Collect data on apartments from immobilienscout24.de and return the collected data as a Pandas dataframe
    :param verbose: boolean, set True to display console output
    :return: Pandas dataframe containing apartment data as seen in offer_data
    """
    base_URL = 'https://www.immobilienscout24.de/Suche/de/baden-wuerttemberg/stuttgart/west/wohnung-mit-einbaukueche-mieten?haspromotion=false&sorting=2&pagenumber='
    base_URL = 'https://www.immobilienscout24.de/Suche/de/baden-wuerttemberg/stuttgart/wohnung-mit-einbaukueche-mieten?haspromotion=false&sorting=2&pagenumber='

    page = requests.get(str(base_URL) + str(1))
    soup = BeautifulSoup(page.content, 'html.parser')
    number_of_results_pages = len(soup.find('select', class_="select").find_all('option'))
    time.sleep(1)

    list_of_all_offer_data = []

    if verbose == True:
        results_pages = tqdm(range(number_of_results_pages))
    else: 
        results_pages = range(number_of_results_pages)

    for results_page in results_pages:

        new_URL = str(base_URL) + str(results_page + 1)
        page = requests.get(new_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results_list_container = soup.find('ul', id="resultListItems")
        all_offerings = results_list_container.find_all('li', class_="result-list__listing")

        for offering in all_offerings:
            offering_id = offering['data-id']
            access_date = datetime.now().date()
            link_prefix = 'https://www.immobilienscout24.de'
            offer_link = link_prefix + offering.find('a')['href']

            offer_details = offering.find_all('div', class_="grid grid-flex gutter-horizontal-l gutter-vertical-s")
            offer_details = offering.find_all('dd', class_="font-nowrap font-highlight font-tabular")

            offer_rent = offer_details[0].text.replace("€", "").replace(".", "").replace(",", ".")
            offer_living_space = offer_details[1].text.replace("m²", "").replace(",", ".")
            offer_number_of_rooms = offer_details[2].find('span', class_="onlyLarge").text.replace(",", ".")

            offering_data = {
                "offering_id": offering_id,
                "access_date": access_date,
                "link": offer_link,
                "rent": offer_rent,
                "living_space": offer_living_space,
                "number_rooms": offer_number_of_rooms
            }

            list_of_all_offer_data.append(offering_data)
        time.sleep(0.1)

    # Insert all new offers into the database and get any error messages
    insertion_error = database_handler.insert_offerings(list_of_all_offer_data)
    if insertion_error != None:
        raise ValueError("PostgreSQL error in database_handler.insert_offerings(): ", insertion_error)

    # Delete duplicate rows from the database
    old_duplicates, new_duplicates, duplicate_deletion_error = database_handler.remove_duplicates()
    if new_duplicates > 0:
        raise ValueError("Duplicate deletion in database_handler.remove_duplicates() didn't delete all duplicates")
    elif duplicate_deletion_error != None:
        raise ValueError("PostgreSQL error: ", duplicate_deletion_error)
    elif verbose is True:
        print("Removed ", old_duplicates/2, " duplicate entries")

    # Deprecated, will be removed soon:
    all_offers_dataframe = pd.DataFrame(list_of_all_offer_data)
    if verbose is True:
        print("Apartment offerings stored: ", str(all_offers_dataframe.shape[0]))

    # Deprecated, will be removed soon:
    # Save dataframe to disk
    # all_offers_dataframe.to_csv(f"{data_dir}/apartments_dataframe.csv")
    return

if __name__ == '__main__':
    scrape_data_from_immoscout(verbose=True)
