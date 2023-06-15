import datetime
import json
from Cinemas.Cinema import Cinema
from Functions import is_english, regexify, get_location_from_ip, find_nearest_addresses, MY_LOCATION, format_date
from Movie import Movie


class YesPlanet(Cinema):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.planetcinema.co.il/il'
        self.api_url = '{home_url}/data-api-service/v1'.format(home_url=self.home_url)
        self.url = '{api_url}/feed/10100/byName/now-playing?lang=en_GB'.format(api_url=self.api_url)
        self.name = 'Yes Planet'

    def get_movies(self):
        response = self.get(self.url)
        movies = json.loads(response.text)['body']['posters']
        return [Movie(title=x['featureTitle'].lower(),
                      suffix=regexify(regex='films/(.*)/', data=x['url']),
                      image=x['mediaList'][-2]['url'],
                      trailer=x['mediaList'][-1]['url'],
                      genre=self.filter_categories_in_list(x['attributes']),
                      origin={'Yes Planet': x['code']}) for x in movies if is_english(x['featureTitle'])]

    def get_nearest_theatres(self):
        """Gets a list of cinema branches by id, latitude, longitude and display name.
        Then filters out branches that are outside a 20 km radius.
        Returns list of dictionaries as such:
        [{id:'', latitude:'', longitude:'', displayName:'', url:''}]"""

        formatted_date = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        url = '{api_url}/quickbook/10100/cinemas/with-event/until/{date}?attr=&lang=he_IL'.format(
            date=formatted_date, api_url=self.api_url)
        response = self.get(url)
        response = json.loads(response.text)['body']['cinemas']
        theatres = [{key: d[key] for key in ['id', 'latitude', 'longitude', 'displayName']} for d in response]

        for theatre in theatres:
            theatre['url'] = '{api_url}/quickbook/10100/film-events/in-cinema/{id}/at-date/{date}?attr=&lang=he_IL'\
                .format(date=today_date, id=theatre['id'], api_url=self.api_url)
        nearest_theatres = find_nearest_addresses(theatres)
        return theatres if not nearest_theatres else nearest_theatres

    def get_theatre_screenings(self, theatres, movies=None):
        """Gets all movie screenings from theatres list.
        Returns dictionary which values are a list of dictionaries as such:
        {theatre1:[movieid1: screenings, movieid2: screenings...], theatre2:[movieid3: screenings]}"""

        timetables = dict()
        for theatre in theatres:
            response = self.get(theatre['url'])
            response = json.loads(response.text)['body']
            events = response['events']
            timetable = {event['filmId']: [] for event in events}

            for event in events:
                event_date = format_date(date=event['eventDateTime'], from_format='%Y-%m-%dT%H:%M:%S', to_format='%H:%M')
                timetable[event['filmId']].append(event_date)
            timetables[theatre['displayName']] = timetable
        return timetables



