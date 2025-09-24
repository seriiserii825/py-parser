from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


def diet():
    # htmlToFile()
    soup = getSoupFromFile("index.html")
    print(f"soup: {soup}")


def getSoupFromFile(filename):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()
    return BeautifulSoup(text, "lxml")


def htmlToFile():
    text = getHtmlFromSite(
        "https://health-diet.ru/table_calorie/"
        "?utm_source=leftMenu&utm_medium=table_calorie"
    )

    writeToFile("index.html", text)


def getHtmlFromSite(url):
    headers = {"user-agent": UserAgent().chrome, "accept": "*/*"}
    req = requests.get(url, headers=headers)
    return req.text


def writeToFile(filename, text):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
