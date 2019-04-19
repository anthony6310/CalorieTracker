# Anthony Pumar, Daniel Corona, Daniel Correa
# Necessary imports to request, search, and run JSON files

import json
import requests
import objectpath


# function to save JSON files
def save_to_file(data, file_name):
    with open(file_name, 'w') as write_file:
        json.dump(data, write_file, indent=4)
        print("The file {0} was successfully created.".format(file_name))


# function to read JSON files
def read_from_file(file_name):
    with open(file_name, 'r') as read_file:
        file = json.load(read_file)
        print("You successfully read from {0}.".format(file_name))
        return file


# function to perform search
def search_api():
    # read API key file
    my_calorie_api_key = read_from_file("api_key.json")

    # save API key to this variable
    my_api_key = my_calorie_api_key["calorie_api_key"]

    # url for nutrition API
    url = "https://chompthis.com/api/product-search.php?token="

    # url concat to key
    url_calorie = url + my_api_key

    # search param
    search_parameter = input("What would you Like to search?")

    search_parameter.lower()

    # full search request
    search_request = url_calorie + "&name=" + search_parameter

    # ***COMMENT OUT THE REQUESTS WHEN NOT NEEDED***

    #calorie = requests.get(search_request).json()

    #save_to_file(calorie, "calories_" + search_parameter + ".json")

    # name of JSON file to use
    calorie_json_file_name = "calories_" + search_parameter + ".json"

    # read from selected JSON file
    calorie_index = read_from_file(calorie_json_file_name)

    # tree path from JSON file
    tree_obj = objectpath.Tree(calorie_index)

    # returns the names of the products
    names = tuple(tree_obj.execute('$..details.name'))

    # returns calories per 100g
    calories = tuple(tree_obj.execute('$..calories.per_100g'))

    results = {}

    str(names)

    search_range = None

    if len(calories) > len(names):
        search_range = names
    else:
        search_range = calories

    for i in range(len(search_range)):
        results.update({names[i]: calories[i]})

    print(results.keys())

    search_key = input("Which " + search_parameter +
                       " product would you like to see calories for?")

    sentinel_value = False

    while sentinel_value == False:
        if search_key in results:
            print(results[search_key])
            sentinel_value = True
        else:
            search_key = input("Sorry, please make sure the "
                               "search matches the key.")


search_api()
