import streamlit as st
import requests
import datetime
import pandas as pd
import numpy as np

'''
# TaxiFareModel Site
## Estimate your taxi cost!
'''

st.markdown('''
We need some information to estiamte the cost of your ride:
''')

image_path = 'images/taxi_ny.jpg'
st.image(image_path, width=500)  

passanger = st.slider('How many passangers?', 1, 8, 1)

d = st.date_input(
    "Which day is your pickup?",
    datetime.date(2014, 7, 6))

t = st.time_input('What about the pick-up time?', datetime.time(8, 45))
pickup_datetime = datetime.datetime.combine(d, t)

columns = st.columns(2)


lat_pickup  = columns[0].number_input('Pick-up latitude',   value=40.7128, step=0.01, format="%.4f")
long_pickup = columns[0].number_input('Pick-up longitude',  value=-74.0060, step=0.01, format="%.4f")
lat_dropoff  = columns[1].number_input('Drop-off latitude',  value=40.7580, step=0.01, format="%.4f")
long_dropoff = columns[1].number_input('Drop-off longitude', value=-73.9855, step=0.01, format="%.4f")


def get_map_data(center_lat, center_lon):
    return pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [center_lat, center_lon],
        columns=['lat', 'lon']
    )

points = pd.DataFrame({
    'lat': [lat_pickup, lat_dropoff],
    'lon': [long_pickup, long_dropoff]
})
st.map(points)

input_dict = dict(
        pickup_datetime=[pd.Timestamp(pickup_datetime, tz='US/Eastern')],
        pickup_longitude=[long_pickup],
        pickup_latitude=[lat_pickup],
        dropoff_longitude=[long_dropoff],
        dropoff_latitude=[lat_dropoff],
        passenger_count=[passanger],
        )

'''
### The price of your run will be around 
'''

url_gcd = st.secrets['gcp_api']['key']

response = requests.get(url_gcd, params = input_dict)
data = response.json()
price = np.round(data['fare'],2)

# Clean metric display
st.metric(label="Estimated Fare", value=f"${price}")

