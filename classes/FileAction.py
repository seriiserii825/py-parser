import csv
import json


class FileAction():
    @staticmethod
    def writeToFile(filename, text, append=False):
        mode = "a" if append else "w"
        with open(filename, mode=mode, encoding="utf-8") as file:
            file.write(text)

    @staticmethod
    def getSoupFromFile(filename):
        from bs4 import BeautifulSoup
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
        return BeautifulSoup(text, "lxml")

    @staticmethod
    def saveToJson(data, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def getJson(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def writeToCsv(data, filename, append=False):
        mode = "a" if append else "w"
        with open(filename, mode, encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
