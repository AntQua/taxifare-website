import streamlit as st
import requests
import datetime
import pydeck as pdk
#from PIL import Image

# image for reference (if needed)
# image = Image.open("path for image file")
# st.image(image)

# URL for the API
url = 'https://taxifare.lewagon.ai/predict'

# Set page configuration
st.set_page_config(layout="wide")

# Title
#st.title("NY Taxi Fare Prediction")
# Centered Title
st.markdown("<h1 style='text-align: center;'>🚕 NY Taxi Fare Prediction 🚕</h1>", unsafe_allow_html=True)

# Layout setup
col1, col2 = st.columns([1, 2])


# Input controllers in the first column
with col1:
    st.subheader("Enter ride details")

    # Date and time input
    date = st.date_input("Select date", datetime.date.today())
    time = st.time_input("Select time", datetime.datetime.now().time())
    date_time = datetime.datetime.combine(date, time)

    # Pickup and dropoff coordinates
    pickup_longitude = st.number_input("Pickup longitude", value=-73.985428)
    pickup_latitude = st.number_input("Pickup latitude", value=40.748817)
    dropoff_longitude = st.number_input("Dropoff longitude", value=-73.985428)
    dropoff_latitude = st.number_input("Dropoff latitude", value=40.748817)

    # Passenger count
    passenger_count = st.number_input("Passenger count", min_value=1, max_value=8, value=1)

# Prepare the dictionary with the parameters for the API
params = {
    "pickup_datetime": date_time.strftime("%Y-%m-%d %H:%M:%S"),
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

# Get fare button and API call
with col2:
    # st.write("##")
    # st.write("##")
    if st.button("Get fare"):
        response = requests.get(url, params=params)
        prediction = response.json()
        fare = prediction["fare"]
        st.subheader(f"Estimated Fare: ${fare:.2f}")

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11',
        initial_view_state=pdk.ViewState(
            latitude=(pickup_latitude + dropoff_latitude) / 2,
            longitude=(pickup_longitude + dropoff_longitude) / 2,
            zoom=10,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=[
                    {"coordinates": [pickup_longitude, pickup_latitude]},
                    {"coordinates": [dropoff_longitude, dropoff_latitude]}
                ],
                get_position='coordinates',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

    # Display a summary
    st.markdown(f"""
    **Ride details:**
    - Pickup: ({pickup_latitude}, {pickup_longitude})
    - Dropoff: ({dropoff_latitude}, {dropoff_longitude})
    - Passenger count: {passenger_count}
    - Date and time: {date_time}
    """)
