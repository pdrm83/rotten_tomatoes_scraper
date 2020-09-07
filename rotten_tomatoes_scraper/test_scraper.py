from bs4 import BeautifulSoup
import re
from urllib.request import urlopen

from rotten_tomatoes_scraper.rt_scraper import CelebrityScraper, MovieScraper


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


def test_celebrity_scraper_01():
    celebrity_scraper = CelebrityScraper(celebrity_name='jack nicholson')
    celebrity_scraper.extract_metadata(section='filmography')
    movie_titles = celebrity_scraper.metadata['movie_titles']
    assert 'The Departed' in movie_titles


def test_celebrity_scraper_02():
    celebrity_scraper = CelebrityScraper(celebrity_name='meryl streep')
    celebrity_scraper.extract_metadata(section='highest')
    movie_titles = celebrity_scraper.metadata['movie_titles']
    assert 'Manhattan' in movie_titles


def test_celebrity_scraper_03():
    wiki_parser = WikiParser()
    actresses = wiki_parser.extract_actresses_names()
    celebrity_scraper = CelebrityScraper(celebrity_name=actresses[2])
    celebrity_scraper.extract_metadata(section='highest')
    movie_titles = celebrity_scraper.metadata['movie_titles']
    assert 'Manhattan' in movie_titles


def test_movie_scraper_01():
    movie_scraper = MovieScraper(movie_title='Manhattan')
    movie_scraper.extract_metadata()
    movie_genres = movie_scraper.movie_genre
    assert 'Comedy' in movie_genres


def test_movie_scraper_02():
    movie_scraper = MovieScraper(movie_title='Manhattan')
    movie_scraper.extract_metadata()
    movie_genres = movie_scraper.movie_genre
    assert 'Kids&Family' in movie_genres


def test_movie_scraper_03():
    movie_url = 'https://www.rottentomatoes.com/m/manhattan'
    movie_scraper = MovieScraper(movie_url=movie_url)
    movie_scraper.extract_metadata()
    movie_genres = movie_scraper.movie_genre
    assert 'Kids&Family' not in movie_genres


def test_movie_scraper_04():
    movie_url = 'https://www.rottentomatoes.com/m/marriage_story_2019'
    movie_scraper = MovieScraper(movie_url=movie_url)
    movie_scraper.extract_metadata()
    print(movie_scraper.metadata)


def test_movie_scraper_05():
    movie_scraper = MovieScraper(movie_title='VICKY CRISTINA BARCELONA')
    movie_scraper.extract_metadata()
    print(movie_scraper.metadata)

test_movie_scraper_05()
