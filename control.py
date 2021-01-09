import requests
import auth
import constants

base_url = "https://developers.zomato.com/api/v2.1/"


# Find city id for Auckland #
city_name = 'Auckland'
headers = {'Accept': 'application/json', 'user-key': auth.api_key}
response = requests.get(base_url + "cities?q=" + city_name, headers=headers).content.decode("utf-8")


# Get all cuisines in Auckland #
response = requests.get(base_url + "cuisines?city_id=" + str(constants.CITY_ID), headers=headers).content.decode("utf-8")
print(response)
