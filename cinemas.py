import requests
from bs4 import BeautifulSoup
from random import choice


USERAGENTS = 'user-agents.txt'
PROXIES = 'proxies.txt'


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
    movie_info = filter(lambda movie: movie['title'] == movie_title and
                        movie['year'] == year, movies_data['result'])
    return list(movie_info)[0]['id']


def get_movie_page(movie_id, url='https://www.kinopoisk.ru/film/'):
    useragents = open(USERAGENTS).read().split('\n')
    proxies = open(PROXIES).read().split('\n')
    useragent = {'User-Agent': choice(useragents)}
    proxy = {'http': 'http://' + choice(proxies)}
    return requests.get(url + movie_id, headers=useragent, proxies=proxy).text


def fetch_movie_info(movie_page):
    soup = BeautifulSoup(movie_page, 'lxml')
    movie_title = soup.find('h1', class_='moviename-big').text.strip()
    rating = soup.find('span', class_='rating_ball').text.strip()
    votes = soup.find('span', class_='ratingCount').text.strip()
    return {'title': movie_title,
            'rating': rating,
            'votes': votes}


def get_movies_data():



def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
    #html = fetch_afisha_page()
    #movies_list = parse_afisha_list(html)
    #film_id = get_movie_id('Время первых')
    #fetch_movie_info(film_id)
    page = get_movie_page('53523')
    fetch_movie_info(page)
