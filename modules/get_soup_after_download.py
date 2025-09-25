import os
from classes.FileAction import FileAction
from classes.HttpClient import HttpClient


def get_soup_after_download(url: str):
    http = HttpClient()
    html_content = http.get(url)
    file_name = "index.html"
    if not os.path.exists(file_name):
        FileAction.writeToFile(file_name, html_content)
    return FileAction.getSoupFromFile(file_name)
