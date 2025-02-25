import streamlit as st
from WeatherSmartAI.helper import *
import pytz  # Import the pytz module
from streamlit_lottie import st_lottie  # For animations
import sys

# Streamlit app setup
import streamlit as st
import pytz
from datetime import datetime
from streamlit_lottie import st_lottie

# Set page config
st.set_page_config(layout="wide", page_title="Weather Forecast App")

st.title("🌤️ Weather Forecast App")

# Lottie animation
animation_url = "https://assets5.lottiefiles.com/packages/lf20_g1t3slfh.json"
lottie_animation = load_lottie_animation(animation_url)
if lottie_animation:
    st_lottie(lottie_animation, height=200)

# User Input Section
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        city = st.text_input("🏙️ Enter City Name", placeholder="E.g., London")
    with col2:
        forecast_days = st.slider("📅 Forecast Days (1-5)", min_value=1, max_value=5)

# Get Weather Button
if st.button("Get Weather Update"):
    if not city.strip():
        st.error("❌ Please enter a valid city name.")
    else:
        with st.spinner("⏳ Fetching weather data..."):
            weather_data = get_weather_data(city=city)
            
            if weather_data:
                st.subheader(f"🌟 Weather Update for **{city.capitalize()}**")
                
                # Use tabs to reduce scrolling
                tab1, tab2, tab3 = st.tabs(["📋 Overview", "🌡️ Statistics", "🌅 Sun & Forecast"])

                with tab1:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("🌍 Location", f"{weather_data['name']}, {weather_data['sys']['country']}")
                    col2.metric("📍 Coordinates", f"{weather_data['coord']['lat']}, {weather_data['coord']['lon']}")
                    timezone_offset = weather_data["timezone"] // 3600
                    col3.metric("⏰ Time Zone", f"UTC {'+' if timezone_offset >= 0 else ''}{timezone_offset}")

                    st.subheader("🌦️ Current Conditions")
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"🌥️ **Description**: {weather_data['weather'][0]['description'].capitalize()}")
                    with col2:
                        st.image(
                            f"http://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png",
                            width=100,
                        )

                with tab2:
                    st.subheader("🌡️ Weather Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("🌡️ Temp", f"{weather_data['main']['temp']}°C")
                    col2.metric("🤔 Feels Like", f"{weather_data['main']['feels_like']}°C")
                    col3.metric("💧 Humidity", f"{weather_data['main']['humidity']}%")
                    col4.metric("🌬️ Pressure", f"{weather_data['main']['pressure']} hPa")

                    st.subheader("🍃 Wind & ☁️ Clouds")
                    col1, col2 = st.columns(2)
                    col1.write(f"🌪️ **Wind Speed**: {weather_data['wind']['speed']} m/s")
                    col1.write(f"🧭 **Direction**: {weather_data['wind']['deg']}°")
                    col2.write(f"☁️ **Cloud Coverage**: {weather_data['clouds']['all']}%")

                with tab3:
                    sys = weather_data["sys"]
                    utc_timezone = pytz.timezone("UTC")
                    sunrise = datetime.fromtimestamp(sys["sunrise"], tz=utc_timezone).strftime("%H:%M:%S UTC")
                    sunset = datetime.fromtimestamp(sys["sunset"], tz=utc_timezone).strftime("%H:%M:%S UTC")

                    col1, col2 = st.columns(2)
                    col1.write(f"🌄 **Sunrise**: {sunrise}")
                    col2.write(f"🌇 **Sunset**: {sunset}")

                    st.write("---")
                    with st.expander("📅 View Forecast Details"):
                        forecast_data = user_forecast(
                            lat=weather_data["coord"]["lat"],
                            lon=weather_data["coord"]["lon"],
                            forecast_days=forecast_days,
                        )
                        if forecast_data:
                            display_ndays_forecast(forecast_data)

                # Generated Weather Description
                description = generate_weather_description(weather_data)
                if description:
                    st.subheader("🌤️ **Generated Weather Description**")
                    st.write(description)
