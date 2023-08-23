import json

from lxml import etree

from Functions import suffixify, regexify, IMAGE_NOT_FOUND, exception_method, is_image_url
from Reviewers.Reviewer import Reviewer


class Letterboxd(Reviewer):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://letterboxd.com/'
        self.search_url = '{home_url}search/'.format(home_url=self.home_url)
        self.headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 ('
                                     'KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'}
        self.validate_year_first = True
        self.xpaths.update({
                            'year': ["//span[@class='film-title-wrapper']//small/a/text()"],
                            'rating': ["//span[@class='average-rating']//a/text()"],
                            'movies': ["//div[@class='film-detail-content']"],
                            'title': ["//span[@class='film-title-wrapper']/a/text()"],
                            'id': ["//span[@class='film-title-wrapper']/a/@href"]})
        self.name = 'Letterboxd'


    def get_attributes(self, movie, url=''):
        response = self.get(self.search_url + movie.title)
        movies = self.html.get_xpath_elements(self.xpaths['movies'])
        movies = [etree.tostring(x, pretty_print=True) for x in movies]
        for results in movies:
            self.html.set(results)
            if suffixify(movie.title) == suffixify(self.html.get_xpath_element_by_index(self.xpaths['title'])):
                validation = super().get_attributes(movie, url=self.home_url[:-1] + self.html.get_xpath_element_by_index(self.xpaths['id']))
                if validation:
                    continue
                data_json = regexify(r'\* <!\[CDATA\[ \*\/\n(.*?)\n\/\* \]\]> \*', self.html.response.text)
                data_json = json.loads(data_json)

                if not movie.genre:
                    movie.genre = ', '.join(data_json['genre'])

                if movie.image == IMAGE_NOT_FOUND:
                    if is_image_url(data_json['image']):
                        movie.image = data_json['image']

                rating = data_json['aggregateRating']['ratingValue']
                movie.rating.update({'Letterboxd Audience Score': int(float(rating)*20)})
                break