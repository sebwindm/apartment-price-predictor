import pandas as pd
from joblib import dump, load
import os
from docker import database_handler
# from sklearn.ensemble import RandomForestRegressor
# model = RandomForestRegressor()
# model.fit(X_train, Y_train)
# print("Training test score: ", str(model.score(X_train, Y_train)))
# print("Test set score: ", str(model.score(X_test, Y_test)))

# from sklearn.ensemble import GradientBoostingRegressor
# model = GradientBoostingRegressor()
# model.fit(X_train, Y_train)
# print("Training test score: ", str(model.score(X_train, Y_train)))
# print("Test set score: ", str(model.score(X_test, Y_test)))
# from sklearn.neural_network import MLPRegressor
# model = MLPRegressor(max_iter=1000, random_state=0)

# Rescale data so that mean of X = 0 and standard deviation = 1
# (makes it easier for neural network)
# mean_on_train = X_train.mean(axis=0)
# std_on_train = X_train.std(axis=0)
# X_train_scaled = (X_train - mean_on_train) / std_on_train
# X_test_scaled = (X_test - mean_on_train) / std_on_train
# model.fit(X_train_scaled, Y_train)
# print("Training test score: ",str(model.score(X_train_scaled, Y_train)))
# print("Test set score: ", str(model.score(X_test_scaled, Y_test)))




def prepare_model(verbose=False, data_dir=os.environ.get('DATA_DIR', '.')):
    from sklearn.model_selection import train_test_split

    # # Deprecated, will be removed soon:
    #dataframe = pd.read_csv(f"{data_dir}/apartments_dataframe.csv")

    sql = """ SELECT offering_id, rent, living_space, number_rooms FROM offerings """
    conn = database_handler.open_connection()
    dataframe = pd.read_sql_query(sql, conn)

    # Check for duplicates
    if dataframe[dataframe.duplicated(['offering_id'])].empty == False:
        raise ValueError("Duplicates found")


    y = dataframe['rent']
    X = dataframe[['living_space', 'number_rooms']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, random_state=0)

    if verbose is True:
        print("Shape of dataframes: ", X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)
    return X_train, X_test, Y_train, Y_test


def learn_linear_model(X_train, X_test, Y_train, Y_test, verbose=False, data_dir=os.environ.get('DATA_DIR', '.')):
    from sklearn import linear_model

    model_object = linear_model.LinearRegression().fit(X_train, Y_train)

    if verbose is True:
        print("Training set score: ", str(model_object.score(X_train, Y_train)))
        print("Test set score: ", str(model_object.score(X_test, Y_test)))
    dump(model_object, f'{data_dir}/apartment_model.joblib')
    return


def predict_apartment_price(living_space, number_of_rooms, verbose=False, data_dir=os.environ.get('DATA_DIR', '.')):
    model_object = load(f'{data_dir}/apartment_model.joblib')
    X_new = pd.DataFrame([[living_space, number_of_rooms]])
    prediction = model_object.predict(X_new)[0].round(2)
    if verbose is True:
        print("\nAn apartment with " + str(number_of_rooms) + " rooms and " + str(living_space) + " m² costs " + str(
            prediction) + " € per month.\n")


if __name__ == '__main__':
    prepare_model()