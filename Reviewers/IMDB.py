from Reviewers.Reviewer import Reviewer


class IMDB(Reviewer):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.imdb.com/'
        self.search_url = 'https://www.imdb.com/find/?q='
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    def get_rating(self, movie):
        """Searches for movie in IMDB. Then gets rating."""
        self.get(self.search_url + movie.title)
        url = self.html.get_xpath("//a[@class='ipc-metadata-list-summary-item__t']/@href")[0]
        title = self.html.get_xpath("//a[@class='ipc-metadata-list-summary-item__t']/text()")[0]
        if title.lower().replace(' ', '-').replace(':', '').replace('&', '') == movie.suffix:
            self.get(self.url + url)
        else:
            return
        rating = self.html.get_xpath("//span[@class='sc-bde20123-1 iZlgcd']/text()")[0]
        movie.rating.update({'IMDB Score': int(float(rating) * 10)})
