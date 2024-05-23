import streamlit as st
import requests, json
import datetime
import pandas as pd
import pytz
import timezonefinder
import sys
from IPython import get_ipython
from cryptography.fernet import Fernet


#!pip install streamlit
#!pip install requests
#!pip install json
#!pip install datetime
#!pip install pandas
#!pip install pytz
#!pip install timezonefinder
#!pip install sys
#!pip install IPython
#!pip install cryptography

def check_streamlit():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if not get_script_run_ctx():
            use_streamlit = False
        else:
            use_streamlit = True
    except ModuleNotFoundError:
        use_streamlit = False
    return use_streamlit

def get_friendly_datetime(city_name, lon, lat):
    try:
        timezone_str = get_tz_by_location(lon, lat)
        user_timezone = pytz.timezone(timezone_str)

        utc_now = datetime.datetime.utcnow()

        local_time = utc_now.astimezone(user_timezone)

        formatted_time = local_time.strftime("%A, %B %d, %Y %I:%M %p")

        return (f"Current time in {city_name}: {formatted_time}")
    except pytz.UnknownTimeZoneError:
        return (f"Error: '{timezone_str}' is not a valid timezone.")


def get_city_wheather_info(city_name,key_for_dec_api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    fernet = Fernet(key_for_dec_api_key)
    encMessage = 'gAAAAABmVI2n81eLhmqvFG-izIiw94MfubdGwK3n5INiuLyRpOtVu1rRMIt9sBKTDTRgguQI4wl8QDgtV4b-5h3teinNKGI9N02c0g6beF9vXtb9945Pk7jq5SXy7MUwg93HyamyU4zy'
    api_key = fernet.decrypt(encMessage).decode()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    if api_key:
        response = requests.get(complete_url)
        x = response.json()
        if "cod" in x:
            return x
        else:
            return None


def get_tz_by_location(lon, lat):
    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
    if timezone_str is None:
        timezone_str = tf.closest_timezone_at(lat=lat, lng=lon)
    return timezone_str

def my_print(st1,st2):
    if 'google.colab' in str(get_ipython()):
        print(f"{st1} {st2}")
    elif check_streamlit():
        st.markdown(f"{st1} {st2}")
    else:
        print(f"{st1} {st2}")

def on_change(change):
  return change['new']


if 'google.colab' in str(get_ipython()):
    print("OpenWeatherMap - Moshe Harary")
elif check_streamlit():
    st.title("OpenWeatherMap - Moshe Harary")
else:
    print("OpenWeatherMap - Moshe Harary")
df = pd.read_csv('https://raw.githubusercontent.com/mosheharary/csvfiles/main/500_cities.csv')
cities= df['City'].tolist()

if 'google.colab' in str(get_ipython()):
    key_for_dec_api_key = input("Enter Key for OpenWeatherMap key decryption (get it from mosheharary@gmail.com):")
    city_name = input("Enter city name: ")
elif check_streamlit():
    key_for_dec_api_key = st.text_input("Enter Key for OpenWeatherMap key decryption (get it from mosheharary@gmail.com):")
    city_name = st.selectbox("Choose City:", df['City'].tolist())
else:
    key_for_dec_api_key = input("Enter Key for OpenWeatherMap key decryption (get from it mosheharary@gmail.com):")
    city_name = input("Enter city name: ")

if key_for_dec_api_key:
    wheather = get_city_wheather_info(city_name,key_for_dec_api_key)
else:
    wheather = None
if wheather:
    my_print('City : ', str(wheather["name"]))
    my_print('Country : ', str(wheather["sys"]["country"]))
    if wheather["cod"] != "404":
        date_time = get_friendly_datetime(city_name, wheather['coord']['lon'], wheather['coord']['lat'])
        y = wheather["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = wheather["weather"]
        weather_description = z[0]["description"]
        my_print('date & time : ', str(date_time))
        my_print('Weather Description : ', str(weather_description))
        my_print('Temperature (in kelvin unit) : ', str(current_temperature))
        my_print('atmospheric pressure (in hPa unit) : ', str(current_pressure))
        my_print('humidity (in percentage) : ', str(current_humidiy))
    else:
        my_print(city_name," City Not Found ")