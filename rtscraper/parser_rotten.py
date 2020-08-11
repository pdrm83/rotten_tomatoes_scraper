from bs4 import BeautifulSoup
import re
from urllib.request import urlopen

from rotten_tomatoes_client import RottenTomatoesClient


class RTParser:
    def __init__(self):
        pass

    @staticmethod
    def extract_metadata(url_movie, columns=('Rating', 'Genre', 'Box Office', 'Studio')):
        """
        Args:
            url_movie
            columns: A list of movie metadata

        Returns:
            sample: {'Rating': 'PG-13', 'Genre': 'Comedy', 'Box Office': 164454835, 'Studio': 'Universal Pictures'}
        """
        page_movie = urlopen(url_movie)
        soup = BeautifulSoup(page_movie, "lxml")

        movie_info_section = soup.find_all('div', class_='media-body')
        soup_movie_info = BeautifulSoup(str(movie_info_section[0]), "lxml")
        movie_info_length = len(soup_movie_info.find_all('li', class_='meta-row clearfix'))
        movie_metadata = {}

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

        if movie_metadata['Genre']:
            movie_genre = movie_metadata['Genre']
        else:
            movie_genre = None

        return movie_metadata, movie_genre

    def extract_movies(self, celebrity_name, section='filmography'):
        selected_section = self.__extract_section(celebrity_name, section=section)
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
        genres = dict()
        try:
            for movie_title in movie_titles:
                try:
                    print(movie_title)
                    res = RottenTomatoesClient.search(term=movie_title)
                    url_movie = 'https://www.rottentomatoes.com' + res['movies'][0]['url']
                    _, movie_genres = self.extract_metadata(url_movie=url_movie)
                except IOError:
                    movie_genres = None

                for movie_genre in movie_genres:
                    if movie_genre in genres:
                        genres[str(movie_genre)] += 1
                    else:
                        genres[str(movie_genre)] = 1

        except IOError:
            genres = None

        return genres

    @staticmethod
    def __extract_section(celebrity_name, section):
        res = RottenTomatoesClient.search(term=celebrity_name)
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

