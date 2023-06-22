import re
import bs4
import requests
from lxml import etree

from Functions import regexify


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

    def stringify(self, xpath, elements):
        if xpath.endswith('/text()') or regexify(r'(@\w+)$', xpath):
            if isinstance(elements, list):
                return [str(element).strip() for element in elements]
            else:
                return str(elements).strip()
        return elements

    def get_xpath_elements(self, xpaths):
        for xpath in xpaths:
            elements = self.stringify(xpath, self.dom.xpath(xpath))
            if elements:
                return elements
        return

    def get_xpath_element_by_index(self, xpaths, index=0):
        for xpath in xpaths:
            try:
                element = self.stringify(xpath, self.dom.xpath(xpath)[index])
                if element:
                    return element
            except IndexError:
                pass
        return

    def find(self, string):
        return self.soup.find(string)



