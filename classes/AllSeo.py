from urllib.parse import urlparse, urlunparse
from classes.Print import Print
from classes.Select import Select
from modules.get_soup_after_download import get_soup_after_download


class AllSeo:
    def __init__(self, url):
        if not url:
            Print.error("URL is required.")
            exit(1)
        self.url = self.to_root_url(url)
        self.xml_sitemap_url = f"{url}sitemap_index.xml"

    def to_root_url(self, url: str) -> str:
        """
        Transform any inner page URL to the site root URL.
        Keeps scheme (http/https) and domain, drops path/query/fragment.
        """
        parsed = urlparse(url)
        root = parsed._replace(path="/", params="", query="", fragment="")
        return urlunparse(root)
