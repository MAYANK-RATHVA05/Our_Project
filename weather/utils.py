import os
import requests
import logging
from django.conf import settings
from decimal import Decimal

# Set up logging
logger = logging.getLogger(__name__)

def get_weather_data(location=None, lat=None, lon=None):
    """
    Fetch weather data from OpenWeatherMap API
    Args:
        location (str, optional): Location name (city, address)
        lat (float, optional): Latitude
        lon (float, optional): Longitude
    
    Returns:
        dict: Weather data including temperature, humidity, wind speed, etc.
              or error information
    """
    api_key = settings.WEATHER_API_KEY
    
    if not api_key:
        logger.error("No API key configured for OpenWeatherMap")
        return {
            'error': True,
            'message': 'Weather API key is not configured.',
        }
    
    # Base URL for OpenWeatherMap API
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    # Parameters for the API request
    params = {
        'appid': api_key,
        'units': 'metric',  # Use metric units (Celsius, meters/sec)
    }
    
    # Add location parameter or coordinates
    if location:
        params['q'] = location
    elif lat is not None and lon is not None:
        params['lat'] = lat
        params['lon'] = lon
    else:
        return {
            'error': True,
            'message': 'Location or coordinates are required.',
        }
    
    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract required weather information
            weather_data = {
                'error': False,
                'location_name': data.get('name', 'Unknown') + ', ' + data.get('sys', {}).get('country', ''),
                'temperature': round(data.get('main', {}).get('temp', 0)),
                'condition': data.get('weather', [{}])[0].get('main', 'Unknown'),
                'description': data.get('weather', [{}])[0].get('description', ''),
                'humidity': data.get('main', {}).get('humidity', 0),
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'icon': data.get('weather', [{}])[0].get('icon', ''),
                'latitude': Decimal(str(data.get('coord', {}).get('lat', 0))),
                'longitude': Decimal(str(data.get('coord', {}).get('lon', 0))),
            }
            
            return weather_data
            
        elif response.status_code == 404:
            return {
                'error': True,
                'message': 'Location not found. Please try a different location.',
            }
        elif response.status_code == 401:
            logger.error("API key invalid or exceeded rate limit")
            return {
                'error': True,
                'message': 'Unable to authenticate with the weather service.',
            }
        else:
            logger.error(f"API error: {response.status_code}, {response.text}")
            return {
                'error': True,
                'message': 'Unable to fetch weather data. Please try again later.',
            }
            
    except requests.exceptions.ConnectionError:
        logger.error("Connection error when making API request")
        return {
            'error': True,
            'message': 'Network error. Please check your internet connection.',
        }
    except requests.exceptions.Timeout:
        logger.error("Timeout when making API request")
        return {
            'error': True,
            'message': 'Request timed out. Please try again later.',
        }
    except Exception as e:
        logger.error(f"Unexpected error fetching weather data: {str(e)}")
        return {
            'error': True,
            'message': 'An unexpected error occurred. Please try again later.',
        }

