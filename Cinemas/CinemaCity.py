import datetime
import json

import bs4
from Cinemas.Cinema import Cinema
from Functions import is_english, regexify, find_nearest_addresses, IMAGE_NOT_FOUND, suffixify
from Movie import Movie
from lxml import etree

class CinemaCity(Cinema):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.cinema-city.co.il/'
        self.url = '{home_url}home/MoviesGrid'.format(home_url=self.home_url)
        self.api_url = '{home_url}tickets/Events'.format(home_url=self.home_url)
        self.name = 'Cinema City'
        self.params = {'cat': 'now', 'page': 1, 'TheaterId': 0, 'catId': 0}
        self.theatres = {}
        self.total_progress = 0


    def get_amount_of_movies(self):
        response = self.get('{api_url}?VenueTypeId=1&Date=0'.format(api_url=self.api_url))
        response = json.loads(response.text)
        return len(response)

    def get_movies(self):
        response = self.get(self.url)
        movies = self.html.get_xpath("//div[@class='col-lg-3 col-md-4 col-sm-4 col-6 movie-thumb']")
        limit = self.get_amount_of_movies()//len(movies) + 1

        for _ in range(0, limit):
            self.params['page'] += 1
            response = self.get(self.url)
            page_movies = self.html.get_xpath("//div[@class='col-lg-3 col-md-4 col-sm-4 col-6 movie-thumb']")
            if page_movies:
                movies.extend(page_movies)
            else:
                break

        movies = [etree.tostring(x, pretty_print=True) for x in movies]
        movies_list = []
        for response_text in movies:
            dom = etree.HTML(str(bs4.BeautifulSoup(str(response_text), "html.parser")))
            title = dom.xpath("//div[@class='flip-1']/p[@class='sub-title']/text()") + dom.xpath("//div[@class='flip-1']/p[@class='title']/text()")
            movie_id = regexify(r'(?<=/)\d+', str(dom.xpath("/html/body/div/@data-linkmobile")[0]))
            if title:
                title = str(title[0])
                if is_english(title):
                    movies_list.append(Movie(title=title.lower(),
                                             suffix=suffixify(title),
                                             trailer='',
                                             genre=[],
                                             image=IMAGE_NOT_FOUND,
                                             origin={'Cinema City': movie_id})
                                             )
        return movies_list


    def get_nearest_theatres(self):
        """Gets a list of cinema branches by id, latitude, longitude and display name.
        Then filters out branches that are outside a 20 km radius.
        Returns list of dictionaries as such:
        [{id:'', latitude:'', longitude:'', displayName:'', url:''}]"""
        response = self.get(self.home_url)

        # Generates id:displayName dictionary.
        theatre_id_dictionary = regexify(r'self\.ticketsVM\.theatersAll\((.*)\)', response.text)
        theatre_id_dictionary = json.loads(theatre_id_dictionary)

        for theatre in theatre_id_dictionary:
            if theatre['TixTheatreId'] not in self.theatres:
                self.theatres.update({theatre['TixTheatreId']: theatre['Name']})

        urls = self.html.get_xpath("//div[@class='theatre-a']/a/@href")
        urls = [str(url)[1:] for url in urls]
        display_names = self.html.get_xpath("//div[@class='theatre-a']/a[@href]//div[@class='theatre-name']/text()")
        theatres = []
        for x in range(len(display_names)):
            theatres.append({'displayName': display_names[x].strip("\n ").strip(), 'url': self.home_url+urls[x]})

        # Nearest theatres will be done in next function.
        for theatre in theatres:
            response = self.get(theatre['url'])
            maps_url = str(self.html.get_xpath("//div[@class='theater-loc']/iframe/@src")[0])
            theatre['latitude'], theatre['longitude'] = regexify(r"!2d(\d+\.\d+)!3d(\d+\.\d+)", maps_url)
            theatre['latitude'], theatre['longitude'] = float(theatre['latitude']), float(theatre['longitude'])
            theatre['id'] = regexify(r'(?<=/)\d+', theatre['url'])

        # nearest_theatres = find_nearest_addresses(theatres)
        nearest_theatres = None
        return theatres if not nearest_theatres else nearest_theatres

    def get_theatre_screenings(self, theatres, movies=None):
        """Gets all movie screenings from theatres list.
        Returns dictionary which values are a list of dictionaries as such:
        {theatre1:{movieid1: screenings, movieid2: screenings...}, theatre2:{movieid3: screenings}}"""
        today_date = datetime.datetime.now().strftime('%d/%m/%Y')
        timetables = dict()
        self.total_progress = len(movies)
        for movie in movies:
            movie_id = movie.origin[self.name]
            response = self.get('{api_url}?VenueTypeId=1&MovieId={movie_id}&Date=0'.format(movie_id=movie_id,
                                                                                           api_url=self.api_url))
            events = json.loads(response.text)
            events = [[date for date in event['Dates'] if today_date in date['Date']] for event in events]
            movie_dates = []
            for event in events[0]:
                if event['TheaterId'] not in timetables.keys():
                    timetables[event['TheaterId']] = {}
                movie_dates.append(event['Hour'])
                timetables[event['TheaterId']].update({movie_id : movie_dates})
            self.progress += 1

        timetables = {self.theatres[timetable]: timetables[timetable] for timetable in timetables}
        return timetables




