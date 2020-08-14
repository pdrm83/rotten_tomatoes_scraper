from bs4 import BeautifulSoup
import re
from urllib.request import urlopen

from rotten_tomatoes_scraper.rt_scraper import RTScraper


def test_extract_movies_01():
    rts = RTScraper()
    movie_titles = rts.extract_movies('jack nicholson', section='filmography')
    assert 'The Departed' in movie_titles


def test_extract_movies_02():
    rts = RTScraper()
    movie_titles = rts.extract_movies('jack nicholson', section='highest')
    assert 'The Shooting' in movie_titles


def test_extract_genre_01():
    rts = RTScraper()
    movie_titles = rts.extract_movies('meryl streep', section='highest')
    movie_genres = rts.extract_genre(movie_titles)
    print(movie_genres)
    assert 'Documentary' in movie_genres.keys()


def test_extract_genre_02():
    rts = RTScraper()
    movie_titles = rts.extract_movies('meryl streep', section='filmography')
    movie_genres = rts.extract_genre(movie_titles)
    print(movie_genres)


class WikiParser:
    def __init__(self):
        pass

    @staticmethod
    def extract_actresses_names():
        url_actresses = 'https://en.wikipedia.org/wiki/Category:American_film_actresses'
        page_actresses = urlopen(url_actresses)
        soup = BeautifulSoup(page_actresses, "lxml")
        data = soup.find_all('div', class_='mw-category-group')
        actresses = data[8].text.split('\n')
        actresses = [re.sub(r'\s\([^)]*\)', '', actress) for actress in actresses[1:]]
        return actresses

    @staticmethod
    def extract_actors_names():
        url_actors = 'https://en.wikipedia.org/wiki/Category:American_male_film_actors'
        page_actors = urlopen(url_actors)
        soup = BeautifulSoup(page_actors, "lxml")
        data = soup.find_all('div', class_='mw-category-group')
        actors = data[1].text.split('\n')
        actors = [re.sub(r'\s\([^)]*\)', '', actor) for actor in actors[1:]]
        return actors
