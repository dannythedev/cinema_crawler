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
