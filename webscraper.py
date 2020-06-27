# https://realpython.com/beautiful-soup-web-scraper-python/

import time, requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

base_URL = 'https://www.immobilienscout24.de/Suche/de/baden-wuerttemberg/stuttgart/west/wohnung-mit-einbaukueche-mieten?haspromotion=false&sorting=2&pagenumber='
base_URL = 'https://www.immobilienscout24.de/Suche/de/baden-wuerttemberg/stuttgart/wohnung-mit-einbaukueche-mieten?haspromotion=false&sorting=2&pagenumber='

page = requests.get(str(base_URL) + str(1))
soup = BeautifulSoup(page.content, 'html.parser')
number_of_results_pages = len(soup.find('select', class_="select").find_all('option'))
time.sleep(1)

list_of_all_offer_data = []

for results_page in range(number_of_results_pages):

    new_URL = str(base_URL) + str(results_page + 1)
    page = requests.get(new_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results_list_container = soup.find('ul', id="resultListItems")
    all_offers = results_list_container.find_all('li', class_="result-list__listing")

    for offer in all_offers:
        offer_id = offer['data-id']
        access_date = datetime.today().strftime('%Y-%m-%d')
        link_prefix = 'https://www.immobilienscout24.de'
        offer_link = link_prefix + offer.find('a')['href']

        offer_details = offer.find_all('div', class_="grid grid-flex gutter-horizontal-l gutter-vertical-s")
        offer_details = offer.find_all('dd', class_="font-nowrap font-highlight font-tabular")

        offer_rent = offer_details[0].text.replace("€", "").replace(".", "").replace(",", ".")
        offer_living_space = offer_details[1].text.replace("m²", "").replace(",", ".")
        offer_number_of_rooms = offer_details[2].find('span', class_="onlyLarge").text.replace(",", ".")

        offer_data = {
            "offer_id": offer_id,
            "access_date": access_date,
            "link": offer_link,
            "rent": offer_rent,
            "living_space": offer_living_space,
            "number_rooms": offer_number_of_rooms
        }

        list_of_all_offer_data.append(offer_data)
    if results_page % 10 == 0:
        print("finished page " + str(results_page + 1) + " of " + str(number_of_results_pages))
    time.sleep(0.1)

all_offers_dataframe = pd.DataFrame(list_of_all_offer_data)

print("Apartment offerings stored: ", str(all_offers_dataframe.shape[0]))