import functools
import re
import string
import time
import datetime

import requests



def regexify(regex, data):
    """Extracts regex string from data string."""
    try:
        return re.findall(regex, data)[0]
    except:
        return

def is_english(text):
    return bool(re.match('^[a-zA-Z0-9\s!@#$%^&*(),.?":{}|<>_-]*$', text))

def estimate_time(start_time, current_item, total_items):
    # Calculate the estimated time left
    time_elapsed = time.time() - start_time
    items_per_second = current_item / time_elapsed
    items_left = total_items - current_item
    time_left = int(items_left / items_per_second)
    return '{0} seconds left.'.format(time_left) if time_left < 120 else '{0} minutes left.'.format(time_left//60)


def convert_time(time_str):
    # Extract the number of minutes from the input string
    minutes = int(re.match(r'(\d+) min', time_str).group(1))
    hours, minutes = minutes // 60, minutes % 60
    return '{}h {}m'.format(hours, minutes)


def capitalize_sentence(sentence):
    words = sentence.split()
    return ' '.join([word.capitalize() if (word.lower() != 'of' and word.lower() != 'a') or index == 0 else word for index, word in enumerate(words)])


def exception_method(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper


import math

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert coordinates to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers

    return distance


def find_nearest_addresses(addresses):
    if MY_LOCATION is None:
        return None
    my_lat, my_lon = MY_LOCATION

    # Filter addresses within the radius of 20 km
    nearest_addresses = []
    for address in addresses:
        address_lat, address_lon = address['latitude'], address['longitude']
        distance = calculate_distance(my_lat, my_lon, address_lat, address_lon)
        if distance <= RADIUS_KM:
            nearest_addresses.append(address)

    return nearest_addresses

def is_address_in_range(address):
    if MY_LOCATION is None:
        return None
    my_lat, my_lon = MY_LOCATION
    address_lat, address_lon = address['latitude'], address['longitude']
    distance = calculate_distance(my_lat, my_lon, address_lat, address_lon)
    return distance <= RADIUS_KM

def get_location_from_ip():
    response = requests.get('https://ipapi.co/json/')
    if response.status_code == 200:
        data = response.json()
        latitude = data['latitude']
        longitude = data['longitude']
        return latitude, longitude
    print('Failed to retrieve location information.')

MY_LOCATION = get_location_from_ip()
RADIUS_KM = 20

def format_date(date, from_format, to_format):
    return datetime.datetime.strptime(date, from_format).strftime(to_format)