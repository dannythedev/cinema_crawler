import functools
import re
import string
import time
import datetime

import requests

IMAGE_NOT_FOUND = 'https://www.prokerala.com/movies/assets/img/no-poster-available.webp'
LOADING_REFERSH_TIME = 0.75
REGEX_YEAR = r'\d{4}'


def regexify(regex, data):
    """Extracts regex string from data string."""
    try:
        return re.findall(regex, data)[0]
    except:
        return


def is_english(s):
    """Checks if 's' is in English."""
    if not s.strip():
        return False
    return bool(regexify('^[a-zA-Z0-9\s!@#$%^&*(),.?":{}|<>_-]*$', s))


def estimate_time(start_time, current_item, total_items):
    # Calculate the estimated time left
    time_elapsed = time.time() - start_time
    items_per_second = current_item / time_elapsed
    items_left = total_items - current_item
    time_left = int(items_left / items_per_second)
    if time_left < 0:
        time_left = 0
    return '{0} seconds left.'.format(time_left) if time_left < 120 else '{0} minutes left.'.format(time_left // 60)


def convert_time(time_str):
    # Extract the number of minutes from the input string
    minutes = int(re.match(r'(\d+) min', time_str).group(1))
    hours, minutes = minutes // 60, minutes % 60
    return '{}h {}m'.format(hours, minutes)


def capitalize_sentence(sentence):
    words = sentence.split()
    return ' '.join(
        [word.capitalize() if (word.lower() != 'of' and word.lower() != 'a') or index == 0 else word for index, word in
         enumerate(words)])


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
        return []
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


def suffixify(s):
    return s.replace(' ', '-').replace(':', '').replace('&', '').replace('.', '').lower()

def compare_movie_names(movie_name1, movie_name2):
    # Remove non-alphanumeric characters and convert to lowercase
    movie_name1_cleaned = ''.join(e for e in movie_name1 if e.isalnum()).lower()
    movie_name2_cleaned = ''.join(e for e in movie_name2 if e.isalnum()).lower()

    # Check if the cleaned names are equal
    if movie_name1_cleaned == movie_name2_cleaned:
        return True

    # Define variations of words that may appear in movie titles
    word_variations = {
        "volume": ["vol.", "volumes", "vols"],
        "part": ["pt.", "parts", "pts"],
        "chapter": ["ch.", "chapters", "chs"],
        "edition": ["ed.", "eds", "editions"],
        "episode": ["ep.", "eps", "episodes"],
        "season": ["seas.", "seasons"],
        "special": ["spec.", "specials"],
        "director's cut": ["dc", "director's"],
        "extended": ["ext.", "extended version"],
        "ultimate": ["ult.", "ultimate edition"],
        "anniversary": ["anniv.", "anniversary edition"],
        # Add more variations as needed
    }

    # Check for specific variations in the names
    for word, variations in word_variations.items():
        if any(variation in movie_name1_cleaned for variation in variations) and \
                any(variation in movie_name2_cleaned for variation in variations):
            # Extract the word from both names
            word_extract1 = [var for var in variations if var in movie_name1_cleaned][0]
            word_extract2 = [var for var in variations if var in movie_name2_cleaned][0]

            # Remove the word from the cleaned names
            movie_name1_cleaned = movie_name1_cleaned.replace(word_extract1, "")
            movie_name2_cleaned = movie_name2_cleaned.replace(word_extract2, "")

            # Compare the cleaned names
            if movie_name1_cleaned == movie_name2_cleaned:
                return True

    return False


import re

def filter_hour_format(strings):
    pattern = r'^\d{2}:\d{2}$'  # Regex pattern for 'hh:mm' format
    # Use list comprehension to filter strings
    return [s.strip() for s in strings if regexify(pattern, s.strip())]

def sort_and_remove_duplicate_hours(hours):
    # Remove duplicates using set()
    unique_hours = list(set(hours))
    # Sort the hours using custom key function
    sorted_hours = sorted(unique_hours, key=lambda x: (int(x.split(':')[0]), int(x.split(':')[1])))
    return sorted_hours

def is_image_url(url):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    return any(url.lower().endswith(ext) for ext in image_extensions)
