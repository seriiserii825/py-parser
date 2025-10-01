from urllib.parse import urlparse
from classes.FileAction import FileAction
from classes.HttpClient import HttpClient


def get_soup_after_download(url: str):
    http = HttpClient()
    html_content = http.get(url)
    parsed = urlparse(url)
    path = parsed.path.strip("/")  # remove leading/trailing slashes

    if not path:  # homepage
        file_name = "index.html"
    else:
        file_name = path.replace("/", "_") + ".html"

    FileAction.writeToFile(file_name, html_content)
    return FileAction.getSoupFromFile(file_name)
