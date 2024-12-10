import streamlit as st
from WeatherSmartAI.helper import *
import pytz  # Import the pytz module
from streamlit_lottie import st_lottie  # For animations
import sys

# Streamlit app setup
st.set_page_config(layout="wide", page_title="Weather Forecast App")
st.title("🌤️ Weather Forecast App")


# Add a Lottie animation header
animation_url = "https://assets5.lottiefiles.com/packages/lf20_g1t3slfh.json"
lottie_animation = load_lottie_animation(animation_url)
if lottie_animation:
    st_lottie(lottie_animation, height=200)

# User input for city
city = st.text_input("🏙️ Enter the City Name", placeholder="E.g., London")
forecast_days = st.slider("📅 Select Forecast Days (1-5)", min_value=1, max_value=5)


if st.button("Get Weather Update"):
    if not city.strip():
        st.error("❌ Please enter a valid city name.")
    else:
        st.title(f"🌟 Weather Update for **{city.capitalize()}**")
        with st.spinner("⏳ Fetching weather data..."):
            weather_data = get_weather_data(city=city)
            if weather_data:
                # Add animation for weather
                animation_url = "https://assets5.lottiefiles.com/packages/lf20_g1t3slfh.json"
                lottie_animation = load_lottie_animation(animation_url)
                if lottie_animation:
                    st_lottie(lottie_animation, height=200)

                # Display top-level details with icons
                st.header("📋 Key Weather Details")
                # Divide top-level details into three columns
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🌍 Location", f"{weather_data['name']}, {weather_data['sys']['country']}")
                with col2:
                    st.metric("📍 Coordinates", f"{weather_data['coord']['lat']}, {weather_data['coord']['lon']}")
                with col3:
                    timezone_offset = weather_data["timezone"] // 3600  # Convert seconds to hours
                    st.metric("⏰ Time Zone", f"UTC {'+' if timezone_offset >= 0 else ''}{timezone_offset}")

                # Extract and display current weather conditions with an icon
                st.write("---")  # Add a divider for clarity
                st.subheader("🌦️ Current Conditions")
                current_weather_col1, current_weather_col2 = st.columns([2, 1])
                weather = weather_data["weather"][0]
                with current_weather_col1:
                    st.write(f"🌥️ **Description**: {weather['description'].capitalize()}")
                with current_weather_col2:
                    st.image(
                        f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png",
                        width=100,
                    )

                # Display Main Weather Stats
                st.write("---")
                st.subheader("🌡️ Weather Statistics")
                main = weather_data["main"]
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                with stat_col1:
                    st.metric("🌡️ Temperature", f"{main['temp']}°C")
                with stat_col2:
                    st.metric("🤔 Feels Like", f"{main['feels_like']}°C")
                with stat_col3:
                    st.metric("💧 Humidity", f"{main['humidity']}%")
                with stat_col4:
                    st.metric("🌬️ Pressure", f"{main['pressure']} hPa")

                # Wind and Cloud Conditions
                st.write("---")
                st.subheader("🍃 Wind and ☁️ Clouds")
                wind_col1, wind_col2 = st.columns(2)
                wind = weather_data["wind"]
                clouds = weather_data["clouds"]
                with wind_col1:
                    st.write(f"🌪️ **Wind Speed**: {wind['speed']} m/s")
                    st.write(f"🧭 **Direction**: {wind['deg']}°")
                with wind_col2:
                    st.write(f"☁️ **Cloud Coverage**: {clouds['all']}%")

                # Sunrise and Sunset Times
                st.write("---")
                st.subheader("🌅 Sun Times")
                sun_col1, sun_col2 = st.columns(2)
                
                sys = weather_data["sys"]  # Ensure this variable is defined and contains the required data

                # Convert sunrise and sunset timestamps to UTC with the correct timezone
                utc_timezone = pytz.timezone("UTC")
                sunrise = datetime.fromtimestamp(sys["sunrise"], tz=utc_timezone).strftime("%H:%M:%S UTC")
                sunset = datetime.fromtimestamp(sys["sunset"], tz=utc_timezone).strftime("%H:%M:%S UTC")

                # Display sunrise and sunset in the respective columns
                with sun_col1:
                    st.write(f"🌄 **Sunrise**: {sunrise}")
                with sun_col2:
                    st.write(f"🌇 **Sunset**: {sunset}")

                # Fetch and display forecast
                forecast_data = user_forecast(
                    lat=weather_data["coord"]["lat"],
                    lon=weather_data["coord"]["lon"],
                    forecast_days=forecast_days,
                )
                if forecast_data:
                    display_ndays_forecast(forecast_data)

                # Generate a detailed weather description
                description = generate_weather_description(weather_data)
                if description:
                    st.subheader("🌤️ **Generated Weather Description**")
                    st.write(description)


