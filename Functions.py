import re
import string

def regexify(regex, data):
    """Extracts regex string from data string."""
    try:
        return re.findall(regex, data)[0]
    except:
        return

def is_english(text):
    return bool(re.match('^[a-zA-Z0-9\s!@#$%^&*(),.?":{}|<>_-]*$', text))

def combine_duplicates(dicts):
    # Create an empty dictionary to store the combined dictionaries
    combined = {}
    for dictionary in dicts:
        title = dictionary['title']
        if title in combined:
            if combined[title]['origin'] != dictionary['origin']:
                dictionary['origin'] += ', '+combined[title]['origin']
            combined[title].update(dictionary)
        else:
            combined[title] = dictionary
    return list(combined.values())