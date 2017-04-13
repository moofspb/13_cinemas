import requests
from bs4 import BeautifulSoup


def fetch_afisha_page(url='https://www.afisha.ru/spb/schedule_cinema/'):
    return requests.get(url).text


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'lxml')
    films = soup.find_all('div', class_='s-votes-hover-area')
    films_data = []
    for film in films:
        title = film.find('h3', class_='usetags').text.strip()
        cinemas_amount = len(film.find('table').find_all('td', class_='b-td-item'))
        films_data.append({'title': title, 'cinemas_amount': cinemas_amount})
    return films_data


    #for film in films:
     #   res.append((film_title, cinemas_amount))
    #print(res)

def fetch_movie_info(movie_title):
    pass


def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
    html = fetch_afisha_page()
    parse_afisha_list(html)
