import re
import bs4
from lxml import etree


class Parser:
    """Html class for response."""

    def __init__(self):
        self.soup = None
        self.dom = None
        self.response = None

    def set(self, response):
        self.response = response
        self.soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        self.dom = etree.HTML(str(self.soup))

    def get_xpath(self, xpath):
        return self.dom.xpath(xpath)

    def find(self, string):
        return self.soup.find(string)


def regexify(regex, data):
    """Extracts regex string from data string."""
    try:
        return re.findall(regex, data)[0]
    except:
        return
