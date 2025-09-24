from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


def main():
    session = requests.Session()

    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    link = "http://lc-progeo.local/wp-login.php"
    data = {"log": "test", "pwd": "test"}
    response = session.post(link, data=data, headers=headers).text
    print(f"{response}: response")

    pages_link = "http://lc-progeo.local/wp-admin/edit.php?post_type=page"
    response = session.get(pages_link, headers=headers).text
    soup = BeautifulSoup()
    wp_heading_inline = 


if __name__ == "__main__":
    main()
