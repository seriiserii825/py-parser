from pathlib import Path
from urllib.parse import urlparse
from classes.FileAction import FileAction
from classes.HttpClient import HttpClient


class Sitemap:
    def __init__(self, domain: str):
        self.url = 'sitemap_index.xml'

    def get_soup_after_download(self, url: str):
        http = HttpClient()
        html_content = http.get(url)
        parsed = urlparse(url)
        path = parsed.path.strip("/")  # remove leading/trailing slashes
        # filename create domain folder + each segment of path a subfolder
        domain = parsed.netloc.replace("www.", "")
        domain_path = Path(domain)
        if not domain_path.exists():
            domain_path.mkdir(parents=True, exist_ok=True)

        if not path:  # homepage
            file_name = domain_path / "index.html"
        else:
            # create subfolders for each segment in the path and a file from last segment + .html
            segments = path.split("/")
            *folders, last_segment = segments
            folder_path = domain_path.joinpath(*folders)
            if not folder_path.exists():
                folder_path.mkdir(parents=True, exist_ok=True)
            file_name = folder_path / f"{last_segment}.html"

        FileAction.writeToFile(file_name, html_content)
        return FileAction.getSoupFromFile(file_name)
