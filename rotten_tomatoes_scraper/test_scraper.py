from rotten_tomatoes_scraper.rtscraper import RTScraper


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
