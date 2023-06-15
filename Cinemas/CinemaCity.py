import bs4
from Cinemas.Cinema import Cinema
from Functions import is_english, regexify
from Movie import Movie
from lxml import etree

class CinemaCity(Cinema):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.cinema-city.co.il/home/MoviesGrid'
        self.name = 'Cinema City'
        self.params = {'cat': 'now', 'page': 0, 'TheaterId': 0, 'catId': 0}


    def get_movies(self):
        movies = []
        for _ in range(0, 20):
            self.params['page'] += 1
            response = self.get(self.url)
            page_movies = self.html.get_xpath("//div[@class='col-lg-3 col-md-4 col-sm-4 col-6 movie-thumb']")
            if page_movies:
                movies += page_movies
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
                                             suffix=title.replace(' ','-').lower(),
                                             trailer='',
                                             genre=[],
                                             image=dom.xpath("//img[@class='img-responsive flip-thumb']/@src"),
                                             origin={'Cinema City': movie_id})
                                             )
        return movies_list
