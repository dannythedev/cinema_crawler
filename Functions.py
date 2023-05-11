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


def convert_time(time_str):
    # Extract the number of minutes from the input string
    minutes = int(re.match(r'(\d+) min', time_str).group(1))
    hours, minutes = minutes // 60, minutes % 60
    return '{}h {}m'.format(hours, minutes)


def capitalize_sentence(sentence):
    words = sentence.split()
    return ' '.join([word.capitalize() if (word.lower() != 'of' and word.lower() != 'a') or index == 0 else word for index, word in enumerate(words)])

def exception_method(func):
    def execution(*args, **kwargs):
        try:
            return func(args, kwargs)
        except:
            pass

    return execution