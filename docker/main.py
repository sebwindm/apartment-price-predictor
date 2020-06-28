"""
This package scrapes data from an apartment-finding website and uses the gathered information on living area, number 
of rooms and price to train a machine learning model. The model can then be used to predict the price of an apartment
by giving a number of rooms and the living space.
"""
import webscraper, price_predictor


def ask_user():
    user_input = input('Type... '
                  '\n 1 to get new apartment data'
                  '\n 2 to train the model'
                  '\n 3 to predict'
                  '\n 4 to exit \n'
                  )
    return user_input


if __name__ == '__main__':
    user_input = ask_user()

    if user_input == "1":
        dataframe = webscraper.scrape_data_from_immoscout(verbose=True)

    elif user_input == "2":
        X_train, X_test, Y_train, Y_test = price_predictor.prepare_model(verbose=True)
        model = price_predictor.learn_linear_model(X_train, X_test, Y_train, Y_test, verbose=True)

    elif user_input == "3":
        rooms = input('How many rooms should the apartment have?\n')
        area = input('How large (in m²) should the apartment be?\n')
        price_predictor.predict_apartment_price(area, rooms, verbose=True)

    elif user_input == "4":
        exit()