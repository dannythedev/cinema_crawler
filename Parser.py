import re
import bs4
import requests
from lxml import etree


class Parser:
    """Html class for response."""

    def __init__(self):
        self.soup = None
        self.dom = None
        self.response = None

    def set(self, response):
        if isinstance(response, requests.Response):
            self.response = response
            response = response.text
        self.soup = bs4.BeautifulSoup(response, "html.parser")
        self.dom = etree.HTML(str(self.soup))

    def get_xpath(self, xpath):
        return self.dom.xpath(xpath)

    def find(self, string):
        return self.soup.find(string)



