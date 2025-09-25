import os
import csv
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
    print("Парсинг категорий...")
    os.makedirs("pages", exist_ok=True)
    count = 1
    iterations = 10
    for category_name, category_link in categories.items():
        if count < 11:
            filename = replaceByArray(category_name, [",", " ", "-", "'"]) + ".html"
            filename = f"pages/{count}_{filename}"
            text = getHtmlFromSite(category_link)
            writeToFile(filename, text)
            category_soup = getCategoryFromFile(filename)
            parseCategory(category_soup, filename)
            print("=" * 50)
            print(f"Итерация {count}. Осталось {iterations} категорий")
            print("=" * 50)
        count += 1
        iterations -= 1


def parseCategory(soup, filename):
    table = soup.select_one(".uk-table")
    headers = []
    for th in table.select("th"):
        headers.append(th.text)
    writeToCsv([headers], filename.replace(".html", ".csv"))
    rows = []
    for tr in table.select("tr")[1:]:
        row = []
        for td in tr.select("td"):
            row.append(td.text)
        rows.append(row)
    writeToCsv(rows, filename.replace(".html", ".csv"), append=True)


def writeToCsv(data, filename, append=False):
    mode = "a" if append else "w"
    with open(filename, mode, encoding="utf-8") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)


def getCategoryFromFile(filename):
    print(f"Получение категории из файла {filename}...")
    return getSoupFromFile(filename)


def replaceByArray(text, arr):
    for item in arr:
        text = text.replace(item, "_")
    return text


def getDataFromJson(filename):
    print(f"Получение данных из файла {filename}...")
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def saveToJson(data, filename):
    print(f"Сохранение данных в файл {filename}...")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def getLinks(soup):
    print("Получение ссылок на категории...")
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
    print("Скачивание главной страницы...")
    text = getHtmlFromSite(
        "https://health-diet.ru/table_calorie/"
        "?utm_source=leftMenu&utm_medium=table_calorie"
    )

    writeToFile("index.html", text)


def getHtmlFromSite(url):
    print(f"Скачивание страницы {url}...")
    headers = {"user-agent": UserAgent().chrome, "accept": "*/*"}
    req = requests.get(url, headers=headers)
    return req.text


def writeToFile(filename, text):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
