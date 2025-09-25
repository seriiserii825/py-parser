from classes.Diet import Diet
from classes.FileAction import FileAction
from classes.HttpClient import HttpClient


def diet():
    http = HttpClient()
    response = http.get(
        "https://health-diet.ru/table_calorie/"
        "?utm_source=leftMenu&utm_medium=table_calorie"
    )
    FileAction.writeToFile("index.html", response)
    soup = FileAction.getSoupFromFile("index.html")
    diet_cls = Diet()
    links = diet_cls.getLinks(soup)
    FileAction.saveToJson(links, "all_categories.json")
    all_categories = FileAction.getJson("all_categories.json")
    Diet.categoriesToFiles(all_categories)
