import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'
source = requests.get(url)
source.raise_for_status()

soup = BeautifulSoup(source.text, 'html.parser')

movie_name = []
year = []
time = []
rating = []
metascore = []
votes = []
gross = []
description = []
Director = []
Stars = []

movie_data = soup.find_all('div', class_='lister-item')

for store in movie_data:
    name = store.h3.a.text
    movie_name.append(name)

    year_of_release = store.h3.find('span', class_='lister-item-year').text.strip('()')
    year.append(year_of_release)

    runtime = store.find('span', class_='runtime').text.replace(' min', '') if store.find('span', class_='runtime') else None
    time.append(runtime)

    rate = store.find('div', class_='inline-block ratings-imdb-rating').strong.text
    rating.append(rate)

    meta = store.find('span', class_='metascore').text.strip() if store.find('span', class_='metascore') else None
    metascore.append(meta)

    value = store.find_all('span', attrs={'name': 'nv'})

    vote = value[0]['data-value']
    votes.append(vote)

    grosses = value[2]['data-value'] if len(value) > 2 else None
    gross.append(grosses)

    describe = store.find('p', class_='text-muted').find_next('p').text.strip() if store.find('p', class_='text-muted').find_next('p') else None
    description.append(describe)

    cast = store.find("p", class_='')
    cast = cast.text.strip().split('|')
    cast = [x.strip() for x in cast]
    cast = [cast[i].replace(j, "") for i, j in enumerate(["Director:", "Stars:"])]
    Director.append(cast[0])
    Stars.append([x.strip() for x in cast[1].split(",")])

movie_DF = pd.DataFrame({'Name of movie': movie_name, 'Year of relase': year, 'Watchtime': time, 'Movie Rating': rating, 'Metascore': metascore, 'Votes': votes, 'Gross collection': gross, 'Description': description, "Director": Director, 'Star': Stars})
#Saving data in Excel file:

movie_DF.to_excel("Top_100_IMDB_Movies.xlsx")
movie_DF.head(7)
