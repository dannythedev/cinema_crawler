import datetime
import json
from Cinemas.Cinema import Cinema
from Functions import is_english, regexify, get_location_from_ip, find_nearest_addresses
from Movie import Movie


class YesPlanet(Cinema):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.planetcinema.co.il/il/data-api-service/v1/feed/10100/byName/now-playing?lang=en_GB'

    def get_movies(self):
        self.get_theater_ids()
        response = self.get(self.url)
        movies = json.loads(response.text)['body']['posters']
        return [Movie(title=x['featureTitle'].lower(),
                      suffix=regexify(regex='films/(.*)/', data=x['url']),
                      image=x['mediaList'][-2]['url'],
                      trailer=x['mediaList'][-1]['url'],
                      genre=self.filter_categories_in_list(x['attributes']),
                      origin='Yes Planet') for x in movies if is_english(x['featureTitle'])]

    def get_theater_ids(self):
        formatted_date = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        url = 'https://www.planetcinema.co.il/il/data-api-service/v1/quickbook/10100/cinemas/with-event/until/{date}?attr=&lang=he_IL'.format(date=formatted_date)
        response = self.get(url)
        response = json.loads(response.text)['body']['cinemas']
        theatres = [{key: d[key] for key in ['id', 'latitude', 'longitude', 'displayName']} for d in response]
        for theatre in theatres:
            theatre['url'] = 'https://www.planetcinema.co.il/il/data-api-service/v1/quickbook/10100/film-events/in-cinema/{id}/at-date/{date}?attr=&lang=he_IL'.format(date=today_date, id=theatre['id'])
        theatres = find_nearest_addresses(get_location_from_ip(), theatres, radius_km=20)

        for theatre in theatres:
            response = self.get(theatre['url'])
            response = json.loads(response.text)['body']
            events = response['events']
            timetable = {event['filmId']: [] for event in events}
            for event in events:
                event_date = datetime.datetime.strptime(event['eventDateTime'], '%Y-%m-%dT%H:%M:%S').strftime('%H:%M')
                timetable[event['filmId']].append(event_date)
            pass
        # Bookings in selected Theatres

