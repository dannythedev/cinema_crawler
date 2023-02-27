import json
from Cinemas.Cinema import Cinema
from Parser import regexify
from Movie import Movie


class YesPlanet(Cinema):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.planetcinema.co.il/il/data-api-service/v1/feed/10100/byName/now-playing?lang=en_GB'

    def get_movies(self):
        response = super().get(self.url)
        movies = json.loads(response.text)['body']['posters']
        return [Movie(title=x['featureTitle'],
                      suffix=regexify(regex='films/(.*)/', data=x['url']),
                      image=x['mediaList'][-2]['url'],
                      trailer=x['mediaList'][-1]['url'],
                      genre=self.filter_categories_in_list(x['attributes'])) for x in movies]
