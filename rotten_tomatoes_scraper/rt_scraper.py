from bs4 import BeautifulSoup
import re
import requests
from urllib.request import urlopen


class RTScraper:

    BASE_URL = "https://www.rottentomatoes.com/api/private/v2.0"
    SEARCH_URL = "{base_url}/search".format(base_url=BASE_URL)

    def __init__(self):
        pass

    def extract_movies(self, celebrity_name, section='filmography'):
        selected_section = self.extract_section(celebrity_name, section=section)
        movie_titles = []
        if section == 'highest':
            for i in range(len(selected_section)):
                movie_titles.append(selected_section[i].text.split('\n')[2].strip())
        elif section == 'filmography':
            soup_filmography = BeautifulSoup(str(selected_section), 'lxml')
            for h in soup_filmography.find_all('a'):
                try:
                    movie_titles.append(h.text.strip())
                except IOError:
                    pass
        return movie_titles

    def extract_genre(self, movie_titles):
        output = dict()
        try:
            for movie_title in movie_titles:
                res = self.search(term=movie_title)
                url_movie = 'https://www.rottentomatoes.com' + res['movies'][0]['url']
                _, movie_genres = self.extract_metadata(url_movie=url_movie)
                for movie_genre in movie_genres:
                    if movie_genre in output:
                        output[str(movie_genre)] += 1
                    else:
                        output[str(movie_genre)] = 1

        except IOError:
            output = dict()

        return output

    def extract_section(self, celebrity_name, section):
        res = self.search(term=celebrity_name)
        selected_section = []
        try:
            if section == 'highest':
                url_celebrity = 'https://www.rottentomatoes.com' + res['actors'][0]['url']
                page_celebrity = urlopen(url_celebrity)
                soup = BeautifulSoup(page_celebrity, "lxml")
                highest_section = soup.find_all('p', class_='celebrity-highest__info')
                selected_section = highest_section
            elif section == 'filmography':
                url_celebrity = 'https://www.rottentomatoes.com' + res['actors'][0]['url']
                page_celebrity = urlopen(url_celebrity)
                soup_celebrity = BeautifulSoup(page_celebrity, "lxml")
                filmography_section = soup_celebrity.find_all('tbody', class_='celebrity-filmography__tbody')[0]
                selected_section = filmography_section
        except IOError:
            print('I could not parse correctly!')

        return selected_section

    def extract_metadata(self, url_movie, columns=('Rating', 'Genre', 'Box Office', 'Studio')):
        page_movie = urlopen(url_movie)
        soup = BeautifulSoup(page_movie, "lxml")

        movie_info_section = soup.find_all('div', class_='media-body')
        soup_movie_info = BeautifulSoup(str(movie_info_section[0]), "lxml")
        movie_info_length = len(soup_movie_info.find_all('li', class_='meta-row clearfix'))
        movie_metadata = dict()

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

        if 'Genre' in movie_metadata:
            movie_genre = movie_metadata['Genre']
        else:
            movie_genre = []

        return movie_metadata, movie_genre

    @staticmethod
    def search(term, limit=10):
        r = requests.get(url=RTScraper.SEARCH_URL, params={"q": term, "limit": limit})
        r.raise_for_status()
        return r.json()
