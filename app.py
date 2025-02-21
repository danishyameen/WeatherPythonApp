# Import necessary libraries
import streamlit as st
import requests
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title=" GIAIC Weather Wise",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# API configuration
API_KEY = "abb54687f0029b17322ac8ed183fbe14"  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Define utility functions
def get_weather_data(city, units="metric"):
    """Fetch weather data from OpenWeatherMap API"""
    params = {
        "q": city,
        "units": units,
        "appid": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def get_weather_icon(condition):
    """Map weather conditions to emoji icons"""
    icon_map = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌁",
        "Drizzle": "🌦️"
    }
    return icon_map.get(condition, "🌤️")

# Build the UI components
def main():
    # Page header
    st.title("🌦️ GIAIC Weather Wise")
    st.title("Real-Time Live Dashboard")
    
    # User inputs in sidebar
    with st.sidebar:
        st.header("🌦️ GIAIC Weather App ")
        st.header("Search Your City Weather")
        city = st.text_input("Enter City Name", "Karachi")
        unit_system = st.selectbox("Select Unit System", ["metric", "imperial"])
        show_details = st.checkbox("Show Extended Details", True)
    
    # Fetch weather data
    if city:
        weather_data = get_weather_data(city, unit_system)
        
        if weather_data and weather_data.get("cod") == 200:
            # Parse data from API response
            main_data = weather_data["main"]
            weather_info = weather_data["weather"][0]
            wind_data = weather_data["wind"]
            sys_data = weather_data["sys"]
            
            # Display basic weather info
            temp_unit = "°C" if unit_system == "metric" else "°F"
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Temperature", 
                         f"{main_data['temp']}{temp_unit}",
                         f"Feels like {main_data['feels_like']}{temp_unit}")
            
            with col2:
                st.metric("Humidity", f"{main_data['humidity']}%")
            
            with col3:
                st.metric("Wind Speed", 
                         f"{wind_data['speed']} {'m/s' if unit_system == 'metric' else 'mph'}",
                         f"Gusts: {wind_data.get('gust', 0)}")
            
            # Weather condition display
            
            st.subheader(f"{get_weather_icon(weather_info['main'])} Current City: {city.capitalize()}")
            st.write(f"**{weather_info['main']}** ({weather_info['description']})")
            
            # Extended details section
            if show_details:
                st.subheader("Detailed Weather Analysis")
                
                col4, col5, col6 = st.columns(3)
                with col4:
                    st.write("🌡️ Temperature Ranges")
                    st.write(f"Min: {main_data['temp_min']}{temp_unit}")
                    st.write(f"Max: {main_data['temp_max']}{temp_unit}")
                
                with col5:
                    st.write("🌬️ Wind Information")
                    st.write(f"Speed: {wind_data['speed']}")
                    st.write(f"Direction: {wind_data['deg']}°")
                
                with col6:
                    st.write("🌄 Sunrise/Sunset")
                    sunrise = datetime.fromtimestamp(sys_data['sunrise'])
                    sunset = datetime.fromtimestamp(sys_data['sunset'])
                    st.write(f"🌅 Sunrise: {sunrise.strftime('%H:%M')}")
                    st.write(f"🌇 Sunset: {sunset.strftime('%H:%M')}")
            
            # Map visualization
            st.subheader("Location Map")
            st.map({
                "latitude": [weather_data["coord"]["lat"]],
                "longitude": [weather_data["coord"]["lon"]]
            }, zoom=10)
            
        elif weather_data and weather_data.get("cod") != 200:
            st.error(f"Error: {weather_data.get('message', 'Unknown error')}")

if __name__ == "__main__":
    main()