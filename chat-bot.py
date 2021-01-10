import auth
import zomatopy

config = {
    "user_key": auth.api_key
}
zomato = zomatopy.initialize_app(config)

# Set up constants #
# coordinates #
LAT = -36.8483
LNG = 174.7626

# Auckland city id #
CITY_ID = 70

# category selection, default to Dine-Out #
CATEGORY = 'Dine-Out'

# default cuisine id to fast food #
CUISINE_ID = '40'

# build cuisine list for city #
# reverse key value pairing #
cuisines_raw = zomato.get_cuisines(CITY_ID)
cuisines_sorted = {}
for k, v in cuisines_raw.items():
    cuisines_sorted[v] = k

print('Loading your food finder chatbot...')

if __name__ == '__main__':

    while True:

        print('What cuisine would you like to eat?')
        statement = input()

        if statement == 0:
            continue

        if statement not in cuisines_sorted.keys():
            print(f'Sorry {statement} is not available.')
        else:
            CUISINE_ID = cuisines_sorted[statement]
            statement = input('Delivery, Takeaway or Dine-out?\n')

            if 'Delivery' in statement:
                CATEGORY = 'Delivery'
            if 'Takeaway' in statement:
                CATEGORY = 'Takeaway'

            # We have enough to suggest restaurants #
            restaurant_ids = zomato.restaurant_search(query=CATEGORY,
                                                      latitude=LAT,
                                                      longitude=LNG,
                                                      cuisines=CUISINE_ID)

            if len(restaurant_ids) == 0:
                print("Couldn't find any restaurants with those options, try again?")
                continue

            print(f'We found {len(restaurant_ids)} places for you!')

            # get first restaurant from list #
            restaurant_cnt = 0
            restaurant = zomato.get_restaurant(restaurant_ids[restaurant_cnt])
            print(f'We recommend...')
            print(f'{restaurant.get("name")} on {restaurant.get("location")}\n'
                  f'it has a user rating of {restaurant.get("user_rating")} stars')

            statement = input('Show menu or Skip?\n')
            while 'Skip' in statement:
                if len(restaurant_ids) - 1 == restaurant_cnt:
                    restaurant_cnt = 0
                else:
                    restaurant_cnt += 1
                restaurant = zomato.get_restaurant(restaurant_ids[restaurant_cnt])

                print(f'We recommend...')
                print(f'{restaurant.get("name")} on {restaurant.get("location")}\n'
                      f'it has a user rating of {restaurant.get("user_rating")} stars')

                statement = input('Show menu or Skip?\n')

            print(f'{restaurant.get("menu_url")}')

            statement = input(f'anything else we can help with?\n').lower()

            while 'restart' not in statement:
                if 'number' in statement:
                    print(f'Contact number is {restaurant.get("phone_numbers")}')
                if 'price' in statement:
                    print(f'Price is rated {restaurant.get("price_range")} out of 4')
                if 'address' in statement:
                    print(f'Address: {restaurant.get("location")}')

                statement = input(f'anything else we can help with?\n').lower()

            if 'restart' in statement:
                continue
