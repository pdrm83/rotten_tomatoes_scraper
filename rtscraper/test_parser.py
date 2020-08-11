
from rotten_tomatoes_client import RottenTomatoesClient
from rtscraper.parser_rotten import RTParser


def test_extract_movies_01():
    rtp = RTParser()
    movie_titles = rtp.extract_movies('jack nicholson')
    assert 'The Departed' in movie_titles


def test_extract_movies_02():
    rtp = RTParser()
    movie_titles = rtp.extract_movies('jack nicholson', section='highest')
    assert 'The Shooting' in movie_titles


def test_extract_genre_01():
    rtp = RTParser()
    movie_titles = rtp.extract_movies('meryl streep', section='highest')
    genres = rtp.extract_genre(movie_titles)
    assert 'Documentary' in genres.keys()


def test_extract_genre_02():
    rtp = RTParser()
    movie_titles = rtp.extract_movies('meryl streep', section='filmography')
    genres = rtp.extract_genre(movie_titles)
    print(genres)


test_extract_genre_02()