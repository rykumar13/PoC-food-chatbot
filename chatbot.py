import AucklandEats
import auth
import zomatopy

config = {
    "user_key": auth.api_key
}
zomato = zomatopy.initialize_app(config)

print('Loading your food finder chatbot...')
aucklandEats = AucklandEats

if __name__ == '__main__':

    while True:

        print('What cuisine would you like to eat?')
        statement = input()

        if statement == 0:
            continue

        if statement not in aucklandEats.AucklandEats.cuisines_sorted.keys():
            print(f'Sorry {statement} is not available.')
        else:
            aucklandEats.AucklandEats.cuisine_id = aucklandEats.AucklandEats.cuisines_sorted[statement]
            statement = input('Delivery, Takeaway or Dine-out?\n')

            if 'Delivery' in statement:
                aucklandEats.AucklandEats.category = 'Delivery'
            elif 'Takeaway' in statement:
                aucklandEats.AucklandEats.category = 'Takeaway'

            # We have enough to suggest restaurants #
            restaurant_ids = zomato.restaurant_search(query=aucklandEats.AucklandEats.category,
                                                      latitude=aucklandEats.AucklandEats.lat,
                                                      longitude=aucklandEats.AucklandEats.lng,
                                                      cuisines=aucklandEats.AucklandEats.cuisine_id)

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
                if len(restaurant_ids)-1 == restaurant_cnt:
                    restaurant_cnt = 0
                else:
                    restaurant_cnt += 1
                restaurant = zomato.get_restaurant(restaurant_ids[restaurant_cnt])
                aucklandEats.AucklandEats.restaurant = restaurant

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
                    print(f'Price is {restaurant.get("price_range")} out of 4')
                if 'address' in statement:
                    print(f'Address: {restaurant.get("location")}')

                statement = input(f'anything else we can help with?\n').lower()

            if 'restart' in statement:
                continue
