import dotenv
import streamlit as st
from user_profile import User_profile_manager
from cars import Car_manager
from send_click_event import ClickEvent

#load environment variables
dotenv.load_dotenv()

# Set page title
st.set_page_config(page_title="Car Shopping")

if 'isLoad' not in st.session_state:
    st.session_state['isLoad'] = False

if 'user_profile' not in st.session_state:
    st.session_state['user_profile'] = None

user_profiles = User_profile_manager().get_user_profile_list()
car_inventory = Car_manager().get_car_inventory()

# Define sidebar
with st.sidebar:
    st.header("User Profile")
    st.session_state.isLoad = True
    st.session_state['user_profile'] = st.selectbox(label="Select a user profile", options=[profile for profile in user_profiles])
    st.write(f"Welcome, {st.session_state['user_profile']}!")
    st.image(st.session_state['user_profile'].get_picture_url(), width=100)

# Define main content
st.title("Car Shopping")
st.header("Select a car")


# Display car inventory
col1, col2, col3 = st.columns(3)

i = 0
for _car in car_inventory:
    # # mod i by 3 to get the column
    if i%3 == 0:
        with col1.container():
            if (st.button(label=f"{_car}", key={_car.get_carid()})):
                st.empty()
                ClickEvent(st.session_state['user_profile'], _car).send()
                st.info(f"Car {_car} selected!")

            st.image(_car.picture_url, width=200)
            st.empty()
    if i%3 == 1:
        with col2.container():
            if(st.button(label=f"{_car}", key={_car.get_carid()})):
                st.empty()
                ClickEvent(st.session_state['user_profile'], _car).send()
                st.info(f"Car {_car} selected!")

            st.image(_car.picture_url, width=200)
            st.empty()
    if i%3 == 2:
        with col3.container():
            if (st.button(label=f"{_car}", key={_car.get_carid()})):
                st.empty()
                ClickEvent(st.session_state['user_profile'], _car).send()
                st.info(f"Car {_car} selected!")
            
            st.image(_car.picture_url, width=200)
            st.empty()
    
    i = i + 1
    # # st.image(car.picture_url, width=200, on_click=ClickEvent(user_profile, car).send())