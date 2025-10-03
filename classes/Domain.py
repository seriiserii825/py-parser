from urllib.parse import urlparse
from classes.Clipboard import Clipboard
from classes.MyTable import MyTable
from classes.PathHelper import PathHelper
from classes.Print import Print
from classes.Select import Select


class Domain:
    def __init__(self):
        ph = PathHelper()
        script_dir = ph.script_dir.parent  # ✅ works
        url_file = script_dir / "urls.txt"
        self.url_path = str(url_file)
        if not url_file.exists():
            Print.error(f"No urls.txt file found at {url_file}")

    def view_all_from_file(self):
        columns = ["Index", "URL"]
        rows = [[str(i + 1), url]
                for i, url in enumerate(self.get_urls_from_file())]
        my = MyTable()
        my.show("Saved URLs", columns, rows)

    def remove_from_file(self):
        urls = self.get_urls_from_file()
        if not urls:
            Print.error("urls.txt is empty.")
            return
        multiple_selected = Select.select_term_menu(urls)
        if not multiple_selected:
            return
        urls = [u for u in urls if u not in multiple_selected]
        with open(self.url_path, "w") as f:
            for url in urls:
                f.write(url + "\n")
        Print.success(f"Removed URL: {', '.join(multiple_selected)}")

    def get_from_clipboard(self) -> str:
        clipboard = (Clipboard.paste() or "").strip()
        print(f"clipboard: {clipboard}")

        if not self._is_http_url(clipboard):
            Print.error("Clipboard does not contain a valid URL.")
            return ""
        url = clipboard
        print("Do you want to save this URL? (y/n): ", end="")
        if input().lower() == "y":
            with open(self.url_path, "a") as f:
                f.write(url + "\n")
            Print.success(f"URL saved to {self.url_path}")
        return url

    def get_urls_from_file(self) -> list[str]:
        with open(self.url_path, "r") as f:
            return [line.strip() for line in f if line.strip()]

    def _is_http_url(self, s: str) -> bool:
        s = (s or "").strip()
        try:
            u = urlparse(s)
            return u.scheme in ("http", "https") and bool(u.netloc)
        except ValueError:
            return False
