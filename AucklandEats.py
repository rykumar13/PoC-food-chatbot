import zomatopy
import auth

config = {
    "user_key": auth.api_key
}
zomato = zomatopy.initialize_app(config)


class AucklandEats:
    # Coordinates #
    lat = -36.8483
    lng = 174.7626

    # set city id #
    city_id = 70

    # category selection, default to Dine-Out #
    category = 'Dine-Out'

    # default cuisine id #
    cuisine_id = '69'

    # find default restaurants #
    restaurants = zomato.restaurant_search(latitude=lat, longitude=lng)

    # default restaurant #
    restaurant = None

    # build cuisine list for city #
    cuisines_raw = zomato.get_cuisines(city_id)
    cuisines_sorted = {}
    for k, v in cuisines_raw.items():
        cuisines_sorted[v] = k

    def find_restaurants(self):
        self.restaurants = zomato.restaurant_search(query=self.category, latitude=self.lat, longitude=self.lng,
                                                    cuisines=self.cuisine_id)

# print(raj.find_restaurants())
# print(raj.find_restaurant_details())

# def find_restaurants(self):
#     return zomato.restaurant_search(latitude=self.lat, longitude=self.lng, cuisines="69")
#
# def find_restaurant_details(self):
#     return zomato.get_restaurant(7005034)
