from urllib.parse import urlparse
from classes.Clipboard import Clipboard
from classes.MyTable import MyTable
from classes.PathHelper import PathHelper
from classes.Print import Print
from classes.Select import Select


def _as_str(choice):
    """Helper: normalize Select.select_one result to a string."""
    if isinstance(choice, list):
        return choice[0] if choice else ""
    return choice or ""


def get_url():
    ph = PathHelper()
    script_dir = ph.script_dir.parent  # ✅ works
    url_file = script_dir / "urls.txt"
    url_path = str(url_file)
    if not url_file.exists():
        Print.error(f"No urls.txt file found at {url_file}")

    options = [
        "Select saved urls",
        "View all from file",
        "Remove from file",
        "Choose url from clipboard",
        "Exit",
    ]

    while True:
        choice = _as_str(Select.select_one(options))

        if choice == "Choose url from clipboard":
            # clipboard path does not require urls.txt to exist
            url = _get_from_clipboard(url_file)
            if url:
                return url

        elif choice == "View all from file":
            view_all_from_file(url_path)

        elif choice == "Remove from file":
            remove_from_file(url_path)
            view_all_from_file(url_path)

        elif choice == "Select saved urls":
            urls = get_urls_from_file(url_path)
            if not urls:
                Print.error("urls.txt is empty.")
                continue
            picked = _as_str(Select.select_one(urls))
            if picked:
                return picked
            else:
                Print.error("No URL selected.")
                # back to menu
        elif choice == "Exit":
            Print.error("Exiting.")
            return ""
        else:
            Print.error("Unknown option. Try again.")


def view_all_from_file(url_file: str):
    columns = ["Index", "URL"]
    rows = [[str(i + 1), url] for i, url in enumerate(get_urls_from_file(url_file))]
    my = MyTable()
    my.show("Saved URLs", columns, rows)


def remove_from_file(url_file: str):
    urls = get_urls_from_file(url_file)
    if not urls:
        Print.error("urls.txt is empty.")
        return
    multiple_selected = Select.select_term_menu(urls)
    if not multiple_selected:
        return
    urls = [u for u in urls if u not in multiple_selected]
    with open(url_file, "w") as f:
        for url in urls:
            f.write(url + "\n")
    Print.success(f"Removed URL: {', '.join(multiple_selected)}")


def _get_from_clipboard(url_file) -> str:
    clipboard = (Clipboard.paste() or "").strip()
    print(f"clipboard: {clipboard}")

    if not is_http_url(clipboard):
        Print.error("Clipboard does not contain a valid URL.")
        return ""
    url = clipboard
    print("Do you want to save this URL? (y/n): ", end="")
    if input().lower() == "y":
        with open(url_file, "a") as f:
            f.write(url + "\n")
        Print.success(f"URL saved to {url_file}")
    return url


def get_urls_from_file(url_file: str) -> list[str]:
    with open(url_file, "r") as f:
        return [line.strip() for line in f if line.strip()]


def is_http_url(s: str) -> bool:
    s = (s or "").strip()
    try:
        u = urlparse(s)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except ValueError:
        return False
