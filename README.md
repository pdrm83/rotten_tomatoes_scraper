[![license](https://img.shields.io/badge/license-MIT-success)](https://github.com/pdrm83/Rotten_Tomatoes_Scraper/blob/master/LICENSE)

# Rotten Tomatoes Scraper 
You can extract information about **movies** and **actors** that are listed on the Rotten Tomatoes website using this 
module. Each movie has different metadata such as *Rating*, *Genre*, *Box Office*, *Studio*, and *Scores*. The 
*Genre* has 20+ subcategories that also gives you more granular information on a movie. These metadata can be helpful 
for many data science projects. For actors you can extract movies listed in **highest-rated** or **filmography** 
sections depending on your need. This module uses the BeautifulSoup package to parse HTML documents. 

## Install
The module requires the following libraries:

* bs4
* requests
* lxml

Then, it can be installed using pip:
```python
pip3 install rotten_tomatoes_scraper
```

## Usage
This module contains two classes: **MovieScraper** and **CelebrityScraper**.

You can use *CelebrityScraper* to extract the complete list of movies that a celebrity participated by calling 
`extract_metadata` method and using `section='filmography'`. Plus, you can also extract the list of top ranked movies 
by using the same method and `section='highest'`. 

```python
from rotten_tomatoes_scraper.rt_scraper import CelebrityScraper

celebrity_scraper = CelebrityScraper(celebrity_name='jack nicholson')
celebrity_scraper.extract_metadata(section='highest')
movie_titles = celebrity_scraper.metadata['movie_titles']

print(movie_titles)
['On a Clear Day You Can See Forever', 'The Shooting', 'Chinatown', 'Broadcast News']
```

You can also use *MovieScraper* to extract metadata of movies. If you want to find out what movie genres an actor has 
participated, you can, first, extract the list of movies that he or she participated using `CelebrityScraper`. Then, you 
must instantiate the `MovieScraper` and feed the `movie_title` to the `extract_metada` method. You can feed `movie_url` 
or `movie_title` to extract the movie metadata. You can see the code below. 

```python
from rotten_tomatoes_scraper.rt_scraper import MovieScraper

movie_scraper = MovieScraper(movie_title='VICKY CRISTINA BARCELONA')
movie_scraper.extract_metadata()

print(movie_scraper.metadata)
{'Score_Rotten': '81', 'Score_Audience': '74', 'Genre': ['comedy', 'drama', 'romance']}
```

```python
from rotten_tomatoes_scraper.rt_scraper import MovieScraper

movie_url = 'https://www.rottentomatoes.com/m/marriage_story_2019'
movie_scraper = MovieScraper(movie_url=movie_url)
movie_scraper.extract_metadata()

print(movie_scraper.metadata)
{'Score_Rotten': '94', 'Score_Audience': '85', 'Genre': ['comedy', 'drama']}
```

This module doesn't give you a full access to all the metadata that you may find in Rotten Tomatoes website. However,
you can easily use it to extract the most important ones.

And, that's pretty much it!
