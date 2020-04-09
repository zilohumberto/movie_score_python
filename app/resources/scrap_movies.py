#!/usr/bin/python
# -*- coding: latin-1 -*-
# scrapping!!
# from: https://medium.com/@asishraz/scraping-data-from-imdb-top-35-movies-using-python-48d1986dc6c9
from bs4 import BeautifulSoup
from requests import get
from json import dumps, loads
from app.settings import API_MOVIE_KEY

url_movie = 'http://www.omdbapi.com/?apikey={}&t={}'
url_scrap = 'https://www.imdb.com/list/ls002981281/'

soup = BeautifulSoup(get(url_scrap).text, 'html.parser')

llist = soup.find_all("h3",{"class":"lister-item-header"})

titles = []
for x in llist:
    for y in x.find_all("a"):
        url = url_movie.format(API_MOVIE_KEY, y.text)
        r = get(url)
        movie = loads(r.text)
        if movie['Response'] == 'True':
            titles.append(dict(
                Title=movie['Title'],
                Year=movie['Year'],
                Poster=movie['Poster'],
                imdbRating=movie['imdbRating'],
                Production=movie.get('Production','')
            ))
        else:
            print("error: ", movie)
print(dumps(titles))
print("--------------")
print(titles)