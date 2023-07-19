"""
Importing necessary packages and modules.
"""
import logging
import requests
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def fetch_weather_data(merged_data: pd.DataFrame) -> pd.DataFrame:
    """
    Fetches weather data based on the latitude and longitude of user addresses.
    Args:
        merged_data (pd.DataFrame): The merged data containing sales and user information.
    Returns:
        pd.DataFrame: The merged data with added weather information.
    """
    api_key = "8a07d17a778413731d4440c41812b402"
    for index, row in merged_data.iterrows():
        lat = row['address']['geo']['lat']
        lon = row['address']['geo']['lng']
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]
            merged_data.at[index, 'temperature'] = temperature
            logger.debug("Added weather info to index %s: %s %s", index, temperature, description)
        except requests.exceptions.RequestException as req_exc:
            logger.warning("An error occurred while fetching weather data: %s", req_exc)
            merged_data.at[index, 'temperature'] = None
            merged_data.at[index, 'weather_description'] = 'Weather data unavailable'
    return merged_data
