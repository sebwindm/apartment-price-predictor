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


# Optional check for duplicates
if all_offers_dataframe[all_offers_dataframe.duplicated(['offer_id'])].empty == False:
    print("Duplicates found")
else:
    print("No duplicates found")


# TODO:
#  save files to csv
# make duplicate check remove duplicates
# fix mlp regressor
# add k-fold cross validation
# increase accuracy
# modularize web scraping and the prediction model
# .


from sklearn.model_selection import train_test_split


y = all_offers_dataframe['rent']
X = all_offers_dataframe[['living_space', 'number_rooms']]
X_train, X_test, Y_train, Y_test = train_test_split(X, y, random_state=0)
print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

from sklearn import linear_model


model = linear_model.LinearRegression().fit(X_train, Y_train)
print("Training test score: ", str(model.score(X_train, Y_train)))
print("Test set score: ", str(model.score(X_test, Y_test)))

# Enter the values for the new apartment:
living_space = 45  # Living space in m²
number_of_rooms = 2  # Number of rooms

X_new = pd.DataFrame([[living_space, number_of_rooms]])

print("An apartment with " + str(number_of_rooms) + " rooms and " + str(living_space) + " m² costs " + str(
    model.predict(X_new)[0].round(2)) + " € per month.")
