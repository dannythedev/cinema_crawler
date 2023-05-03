import re
import string


def is_english(text):
    return bool(re.match('^[a-zA-Z0-9\s!@#$%^&*(),.?":{}|<>_-]*$', text))

def combine_duplicates(dicts):
    # Create an empty dictionary to store the combined dictionaries
    combined = {}
    for dictionary in dicts:
        title = dictionary['title']
        if title in combined:
            combined[title].update(dictionary)
        else:
            combined[title] = dictionary
    return list(combined.values())