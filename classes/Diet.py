import os
from classes.FileAction import FileAction
from classes.HttpClient import HttpClient
from classes.Utils import Utils


class Diet:
    def getLinks(self, soup):
        print("Получение ссылок на категории...")
        allProducts = soup.select(".mzr-tc-group-item-href")
        all_categories = {}
        for item in allProducts:
            item_text = item.text
            item_href = "https://health-diet.ru" + item.get("href")
            all_categories[item_text] = item_href
        return all_categories

    @classmethod
    def categoriesToFiles(cls, categories):
        os.makedirs("pages", exist_ok=True)
        count = 1
        iterations = 10
        for category_name, category_link in categories.items():
            if count < 11:
                filename = Utils.replaceByArray(
                    category_name, [",", " ", "-", "'"]) + ".html"
                filename = f"pages/{count}_{filename}"
                http = HttpClient()
                text = http.get(category_link)
                FileAction.writeToFile(filename, text)
                category_soup = FileAction.getSoupFromFile(filename)
                cls.parseCategory(category_soup, filename)
                print("=" * 50)
                print(f"Итерация {count}. Осталось {iterations} категорий")
                print("=" * 50)
            count += 1
            iterations -= 1

    @staticmethod
    def parseCategory(soup, filename):
        table = soup.select_one(".uk-table")
        headers = []
        for th in table.select("th"):
            headers.append(th.text)
        FileAction.writeToCsv([headers], filename.replace(".html", ".csv"))
        rows = []
        health_dict = {}
        for tr in table.select("tr")[1:]:
            row = []
            td = tr.select("td")
            title = td[0].text
            calories = td[1].text
            proteins = td[2].text
            fats = td[3].text
            carbohydrates = td[4].text
            for td in tr.select("td"):
                row.append(td.text)
                health_dict[title] = {
                    "calories": calories,
                    "proteins": proteins,
                    "fats": fats,
                    "carbohydrates": carbohydrates,
                }
            rows.append(row)
        FileAction.writeToCsv(rows, filename.replace(
            ".html", ".csv"), append=True)
        FileAction.saveToJson(health_dict, filename.replace(".html", ".json"))
