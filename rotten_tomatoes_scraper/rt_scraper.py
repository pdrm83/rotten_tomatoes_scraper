from bs4 import BeautifulSoup
import difflib
import re
import requests
from urllib.request import urlopen


class RTScraper:
    BASE_URL = "https://www.rottentomatoes.com/api/private/v2.0"
    SEARCH_URL = "{base_url}/search".format(base_url=BASE_URL)

    def __init__(self):
        self.metadata = dict()
        self.url = None

    def extract_url(self):
        pass

    def extract_metadata(self, **kwargs):
        pass

    def _extract_section(self, section):
        pass

    @staticmethod
    def search(term, limit=10):
        r = requests.get(url=RTScraper.SEARCH_URL, params={"q": term, "limit": limit})
        r.raise_for_status()
        return r.json()


class MovieScraper(RTScraper):
    def __init__(self, **kwargs):
        RTScraper.__init__(self)
        self.movie_genre = None
        if 'movie_title' in kwargs.keys():
            self.movie_title = kwargs['movie_title']
            self.extract_url()
        if 'movie_url' in kwargs.keys():
            self.url = kwargs['movie_url']

    def extract_url(self):
        search_result = self.search(term=self.movie_title)

        movie_titles = []
        for movie in search_result['movies']:
            movie_titles.append(movie['name'])

        closest = self.closest(self.movie_title, movie_titles)
        for movie in search_result['movies']:
            if movie['name'] == closest[0]:
                url_movie = 'https://www.rottentomatoes.com' + movie['url']

        self.url = url_movie

    def extract_metadata(self, columns=('Rating', 'Genre', 'Box Office', 'Studio')):
        movie_metadata = dict()
        page_movie = urlopen(self.url)
        soup = BeautifulSoup(page_movie, "lxml")

        # Score
        score = soup.find('score-board')
        movie_metadata['Score_Rotten'] = score.attrs['tomatometerscore']
        movie_metadata['Score_Audience'] = score.attrs['audiencescore']

        # Movie Info
        movie_info_section = soup.find_all('div', class_='media-body')
        soup_movie_info = BeautifulSoup(str(movie_info_section[0]), "lxml")
        movie_info_length = len(soup_movie_info.find_all('li', class_='meta-row clearfix'))

        for i in range(movie_info_length):
            x = soup_movie_info.find_all('li', class_='meta-row clearfix')[i]
            soup = BeautifulSoup(str(x), "lxml")
            label = soup.find('div', class_='meta-label subtle').text.strip().replace(':', '')
            value = soup.find('div', class_='meta-value').text.strip()
            if label in columns:
                if label == 'Box Office':
                    value = int(value.replace('$', '').replace(',', ''))
                if label == 'Rating':
                    value = re.sub(r'\s\([^)]*\)', '', value)
                if label == 'Genre':
                    value = value.replace(' ', '').replace('\n', '').split(',')
                movie_metadata[label] = value

        self.metadata = movie_metadata
        self.movie_genre = self.extract_genre(self.metadata)

    @staticmethod
    def closest(keyword, words):
        closest_match = difflib.get_close_matches(keyword, words, cutoff=0.6)
        return closest_match

    @staticmethod
    def extract_genre(metadata):
        try:
            if 'Genre' in metadata:
                movie_genre = metadata['Genre']
            else:
                movie_genre = ['None']

        except IOError:
            movie_genre = ['None']

        return movie_genre


class CelebrityScraper(RTScraper):
    def __init__(self, **kwargs):
        RTScraper.__init__(self)
        if 'celebrity_name' in kwargs.keys():
            self.celebrity_name = kwargs['celebrity_name']
            self.extract_url()
        if 'celebrity_url' in kwargs.keys():
            self.url = kwargs['celebrity_url']

    def extract_url(self):
        search_result = self.search(term=self.celebrity_name)
        url_celebrity = 'https://www.rottentomatoes.com' + search_result['actors'][0]['url']
        self.url = url_celebrity

    def _extract_section(self, section):
        page_celebrity = urlopen(self.url)
        soup = BeautifulSoup(page_celebrity, "lxml")
        selected_section = []
        try:
            if section == 'highest':
                selected_section = soup.find_all('div', class_='posters-container')[0].text.split('\n')
            elif section == 'filmography':
                selected_section = soup.find_all('tbody', class_='celebrity-filmography__tbody')[0]
        except IOError:
            print('The parsing process returns an error.')

        return selected_section

    def extract_metadata(self, section):
        selected_section = self._extract_section(section=section)
        movie_titles = []
        if section == 'highest':
            for i in range(len(selected_section)):
                if selected_section[i].strip():
                    movie_titles.append(selected_section[i].strip())
        elif section == 'filmography':
            soup_filmography = BeautifulSoup(str(selected_section), 'lxml')
            for h in soup_filmography.find_all('a'):
                try:
                    movie_titles.append(h.text.strip())
                except IOError:
                    pass
        self.metadata['movie_titles'] = movie_titles
