import requests
from requests.adapters import Retry
from requests.sessions import HTTPAdapter


class HttpClient():
    def __init__(self, timeout: float = 15.0, retries: int = 3, backoff: float = 0.5):
        self.session = requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.timeout = timeout
        # Avoid fake_useragent flakiness; a stable UA is fine
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0 Safari/537.36",
            "Accept": "*/*",
        }

    def get(self, url: str) -> str:
        resp = self.session.get(
            url, headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.text
