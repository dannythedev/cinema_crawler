import json
import datetime

from Cinemas.Cinema import Cinema
from Functions import is_english, regexify, is_address_in_range, find_nearest_addresses, format_date
from Movie import Movie


class HotCinema(Cinema):
    def __init__(self):
        super().__init__()
        self.url = 'https://hotcinema.co.il/'
        self.name = 'Hot Cinema'

    def get_movies(self):
        response = self.get(self.url)
        movies = json.loads(regexify(regex='app.movies = (.*])', data=response.text))
        movies_list = []
        for x in movies:
            title = regexify(regex='/movie/\d*/(.*)', data=x['PageUrl'])
            if is_english(title):
                movies_list.append(Movie(title=title.replace('-', ' ').lower(),
                          suffix=title,
                          image='',
                          trailer='',
                          genre=[],
                          origin={'Hot Cinema': x['ID']}))
        return movies_list

    def get_nearest_theatres(self):
        """Gets a list of cinema branches by id, latitude, longitude and display name.
        Then filters out branches that are outside a 20 km radius.
        Returns list of dictionaries as such:
        [{id:'', latitude:'', longitude:'', displayName:'', url:''}]"""

        url = 'https://hotcinema.co.il/'
        response = self.get(url)
        urls = self.html.get_xpath("//div[@class='modal-body']/ul/li/a/@href")
        urls = [str(url)[1:] for url in urls]
        display_names = self.html.get_xpath("//div[@class='modal-body']/ul/li/a/text()")
        theatres = []
        for x in range(len(display_names)):
            theatres.append({'displayName': display_names[x], 'url': url+urls[x]})
        # Nearest theatres will be done in next function.
        for theatre in theatres:
            response = self.get(theatre['url'])
            maps_url = str(self.html.get_xpath("//div[@class='text-wrapper']/a/@href")[1])
            theatre['latitude'], theatre['longitude'] = regexify(r'@([^,]+),([^,]+)', maps_url)
            theatre['latitude'], theatre['longitude'] = float(theatre['latitude']), float(theatre['longitude'])
            theatre['id'] = regexify(r'(?<=/)\d+', theatre['url'])

        nearest_theatres = find_nearest_addresses(theatres)
        return nearest_theatres if nearest_theatres is not None else theatres

    def get_theatre_screenings(self, theatres):
        """Gets all movie screenings from theatres list.
        Returns dictionary which values are a list of dictionaries as such:
        {theatre1:[movieid1: screenings, movieid2: screenings...], theatre2:[movieid3: screenings]}"""

        timetables = dict()
        today_date = datetime.datetime.now().strftime('%d/%m/%Y')
        for theatre in theatres:
            url = 'https://hotcinema.co.il/tickets/TheaterEvents2?movieid=undefined&date={date}&theatreid={id}&site=undefined&time=&type=undefined&lang=&kinorai=undefined&genreId=0&screentype=&subdub=&isnew=false'.format(
                date=today_date, id=theatre['id']
            )
            response = self.get(url)
            events = json.loads(response.text)['TheaterEvents']

            timetable = {event['MovieId']: [] for event in events}

            for event in events:
                timetable[event['MovieId']].extend([event_date['Hour'] for event_date in event['Dates']])
            timetables[theatre['displayName']] = timetable
        return timetables
