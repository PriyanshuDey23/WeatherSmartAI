import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import os
from datetime import datetime



# Load the API keys
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # https://home.openweathermap.org/api_keys

# Validate API keys
if not GOOGLE_API_KEY or not WEATHER_API_KEY:
    st.error("API keys for Google Generative AI or Weather API are not set. Please configure them.")
else:
    # Configure Google's Generative AI API key
    genai.configure(api_key=GOOGLE_API_KEY)


# Function to get weather data from OpenWeatherMap
def get_weather_data(city, weather_api_key=WEATHER_API_KEY):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric",  # Optional, for Celsius units
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch weather data: {e}")
        return None


# Function to generate a weather description using Gemini
def generate_weather_description(weather_data):
    temp = weather_data["main"]["temp"]
    condition = weather_data["weather"][0]["description"]
    humidity = weather_data["main"]["humidity"]

    prompt = (
        f"The temperature is {temp}°C, the weather condition is '{condition}', "
        f"and the humidity is {humidity}%. "
        "Describe the current weather in a detailed and engaging way. Be creative."
    )

    try:
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)

        return response.text  # Return the generated text
    except Exception as e:
        st.error(f"Failed to generate weather description: {e}")
        return None
    



# n days Forecast
def user_forecast(lat, lon, forecast_days, weather_api_key=WEATHER_API_KEY):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "cnt": forecast_days * 8,  # API returns data in 3-hour intervals; 8 entries per day
        "appid": weather_api_key,
        "units": "metric",
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch forecast data: {e}")
        return None

# Display n days forecast
def display_ndays_forecast(data):
    st.subheader("📅 Weekly Weather Forecast")
    displayed_dates = set()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("", "Day")
    with c2:
        st.metric("", "Description")
    with c3:
        st.metric("", "Min_Temp")
    with c4:
        st.metric("", "Max_Temp")

    for forecast in data["list"]:
        date = datetime.fromtimestamp(forecast["dt"]).strftime("%A, %B %d")
        if date not in displayed_dates:
            displayed_dates.add(date)
            min_temp = forecast["main"]["temp_min"]
            max_temp = forecast["main"]["temp_max"]
            description = forecast["weather"][0]["description"].capitalize()

            with c1:
                st.write(date)
            with c2:
                st.write(description)
            with c3:
                st.write(f"{min_temp}°C")
            with c4:
                st.write(f"{max_temp}°C")



# Function to load Lottie animations
def load_lottie_animation(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        st.error("Failed to load animation.")
    return None
