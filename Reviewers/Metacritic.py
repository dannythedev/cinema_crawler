from Reviewers.Reviewer import Reviewer


class Metacritic(Reviewer):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.metacritic.com/movie/'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    def get_rating(self, movie):
        self.get(url=self.url + movie.suffix)
        critic_score = self.html.get_xpath("//span[contains(@class, 'metascore_w larger movie')]/text()")[0]
        audience_score = self.html.get_xpath("//span[contains(@class, 'metascore_w user')]/text()")[0]
        movie.rating.update({'Metacritic Audience Score': int(critic_score),
                             'Metacritic Critic Score': int(float(audience_score) * 10)})
