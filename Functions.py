import re
import string
import time


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