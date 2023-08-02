import dotenv
import random
from user_profile import User_profile_manager
from cars import Car_manager
from send_click_event import ClickEvent

#load environment variables
dotenv.load_dotenv()

user_profiles = User_profile_manager().get_user_profile_list()
car_inventory = Car_manager().get_car_inventory()

NUM_EVENTS = 1000

def main():
    for i in range(NUM_EVENTS):
        # get random user profile from user_profiles
        # get random carfrom car_inventory
        # send ClickEvent(user_profile, car)

        random_user = user_profiles[random.randint(0, len(user_profiles)-1)]
        random_car = car_inventory[random.randint(0, len(car_inventory)-1)]

        ClickEvent(user_profile=random_user,car=random_car).send()
        print(f"ClickEvent sent for {random_user} and {random_car}")

if __name__ == "__main__":
    main()