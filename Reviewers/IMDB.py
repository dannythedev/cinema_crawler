from Functions import exception_method, IMAGE_NOT_FOUND
from Reviewers.Reviewer import Reviewer


class IMDB(Reviewer):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.imdb.com/'
        self.search_url = 'https://www.imdb.com/find/?q='
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    @exception_method
    def get_image(self, movie):
        if movie.image == IMAGE_NOT_FOUND:
            xpath = str(self.html.get_xpath("//div[@class='sc-61c73608-1 jLwVZW']//@src")[0])
            if 'poster-default' not in xpath:
                movie.image = xpath

    @exception_method
    def get_duration(self, movie):
        if not movie.duration:
            movie.duration = str(self.html.get_xpath("//html/body/div[2]/main//li[3]/text()")[0])

    @exception_method
    def get_genre(self, movie):
        if not movie.genre:
            movie.genre = str(', '.join(self.html.get_xpath("//div[@class='ipc-chip-list__scroller']/a//text()")))

    def get_attributes(self, movie, url=''):
        """Searches for movie in IMDB. Then gets rating."""
        self.get(self.search_url + movie.title)
        url = self.html.get_xpath("//a[@class='ipc-metadata-list-summary-item__t']/@href")[0]
        title = self.html.get_xpath("//a[@class='ipc-metadata-list-summary-item__t']/text()")[0]
        if title.lower().replace(' ', '-').replace(':', '').replace('&', '') == movie.suffix:
            super().get_attributes(movie, url=self.url + url)
        else:
            return
        rating = self.html.get_xpath("//span[@class='sc-bde20123-1 iZlgcd']/text()")[0]
        movie.rating.update({'IMDB Score': int(float(rating) * 10)})
