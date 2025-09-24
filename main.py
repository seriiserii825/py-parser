from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


def main():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    link = "https://stpav.altuofianco.com/"
    response = requests.get(link, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    title = soup.title.text
    print(f'{title}: title')


if __name__ == "__main__":
    main()
