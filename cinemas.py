import requests
from bs4 import BeautifulSoup
from random import choice
import argparse


USERAGENTS = 'proxies & user-agents/user-agents.txt'
PROXIES = 'proxies & user-agents/proxies.txt'


def get_script_parameters():
    parser = argparse.ArgumentParser(
        description='The script shows rating of best movies in cinemas right now.')
    parser.add_argument('-ma', '--movies amount', nargs='?', type=int, default=10,
                        help='Movies amount that will be shown in rating')
    return parser.parse_args()


def fetch_afisha_page(url='https://www.afisha.ru/spb/schedule_cinema/'):
    return requests.get(url).text


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'lxml')
    movies = soup.find_all('div', class_='s-votes-hover-area')
    movies_data = []
    for movie in movies:
        title = movie.find('h3', class_='usetags').text.strip()
        cinemas_amount = len(movie.find('table').find_all('td', class_='b-td-item'))
        movies_data.append({'title': title, 'cinemas_amount': cinemas_amount})
    return movies_data


def get_movie_id(movie_title, year='2017', url='http://kparser.pp.ua/json/search/'):
    movies_page = requests.get(url+movie_title)
    movies_data = movies_page.json()
    movie_info = list(filter(lambda movie: movie['year'] == year, movies_data['result']))
    movie_id = movie_info[0]['id']
    return movie_id


def get_movie_page(movie_id, url='https://www.kinopoisk.ru/film/'):
    useragents = open(USERAGENTS).read().split('\n')
    proxies = open(PROXIES).read().split('\n')
    useragent = {'User-Agent': choice(useragents)}
    proxy = {'http': 'http://' + choice(proxies)}
    return requests.get(url + movie_id, headers=useragent, proxies=proxy, timeout=10).text


def fetch_movie_data(movie_page):
    soup = BeautifulSoup(movie_page, 'lxml')
    movie_title = soup.find('h1', class_='moviename-big').text.strip()
    rating = soup.find('span', class_='rating_ball').text.strip()
    votes = soup.find('span', class_='ratingCount').text.strip()
    return {'title': movie_title,
            'rating': float(rating),
            'votes': int(votes.replace('\xa0', ''))}


def collect_movies_data():
    afisha_movies_list = parse_afisha_list(fetch_afisha_page())
    movies = []
    for movie in afisha_movies_list:
        movie_id = get_movie_id(movie['title'])
        movie_data = fetch_movie_data(get_movie_page(movie_id))
        movie_data_with_cinemas = {**movie_data, **movie}
        movies.append(movie_data_with_cinemas)
    return movies


def sort_movies(movies):
    return sorted(movies,
                  key=lambda movie: movie['rating'] and movie['cinemas_amount'],
                  reverse=True)


def output_movies_to_console(movies, movies_amount):
    sorted_movies = sort_movies(movies)[:movies_amount]
    print('{} best movies in cinemas right now:'.format(movies_amount))
    print('---------------')
    for movie in enumerate(sorted_movies, start=1):
        print('{}. {} - rating is {} ({} votes).'
              .format(movie[0], movie[1]['title'], movie[1]['rating'], movie[1]['votes']))


if __name__ == '__main__':
    top_movies_amount = get_script_parameters()
    movies = collect_movies_data()
    output_movies_to_console(movies, top_movies_amount)
