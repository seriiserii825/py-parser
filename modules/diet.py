import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import json


def diet():
    # htmlToFile()
    soup = getSoupFromFile("index.html")
    links = getLinks(soup)
    saveToJson(links, "all_categories.json")
    all_categories = getDataFromJson("all_categories.json")
    categoriesToFiles(all_categories)


def categoriesToFiles(categories):
    os.makedirs('pages', exist_ok=True)
    count = 1
    for category_name, category_link in categories.items():
        if count < 3:
            filename = replaceByArray(
                category_name, [",", " ", "-", "'"]) + ".html"
            filename = f"pages/{count}_{filename}"
            text = getHtmlFromSite(category_link)
            writeToFile(filename, text)
        count += 1


def replaceByArray(text, arr):
    for item in arr:
        text = text.replace(item, "_")
    return text


def getDataFromJson(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def saveToJson(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def getLinks(soup):
    allProducts = soup.select(".mzr-tc-group-item-href")
    all_categories = {}
    for item in allProducts:
        item_text = item.text
        item_href = "https://health-diet.ru" + item.get("href")
        all_categories[item_text] = item_href
    return all_categories


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
