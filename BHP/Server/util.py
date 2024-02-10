import json
import pickle
import numpy as np
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

# Your code that may raise warnings

__data_columns = None
__locations = None
__model = None


def get_estimated_price(bath, bhk, sqft, location):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        return -1
    x = np.zeros(len(__data_columns))
    x[0] = bath
    x[1] = bhk
    x[2] = sqft
    if loc_index >= 0:
        x[loc_index] = 1

    return __model.predict([x])[0]


def get_location_names():
    return __locations


def load_artifacts():
    print("loading artifacts")
    global __data_columns
    global __locations
    global __model

    with open(r"C:\Users\navee\PycharmProjects\BHP\Model\columns.json","r") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]

    with open(r"C:\Users\navee\PycharmProjects\BHP\Model\banglore_home_prices_model.pickle", "rb") as f:
        __model = pickle.load(f)



if __name__ == "__main__":
    load_artifacts()
    print(get_location_names())
    print(get_estimated_price(2, 2, 2000, '1st phase jp nagar'))
