from enum import Enum, auto
from typing import Optional
from urllib.parse import urlsplit, urlunsplit

from classes.Domain import Domain
from classes.Print import Print
from classes.Select import Select


class MenuAction(Enum):
    SELECT_SAVED = auto()
    VIEW_ALL = auto()
    REMOVE = auto()
    CLIPBOARD = auto()
    EXIT = auto()


class MainMenu:
    MENU_LABELS: dict[MenuAction, str] = {
        MenuAction.SELECT_SAVED: "Select saved urls",
        MenuAction.VIEW_ALL: "View all from file",
        MenuAction.REMOVE: "Remove from file",
        MenuAction.CLIPBOARD: "Choose url from clipboard",
        MenuAction.EXIT: "Exit",
    }

    @staticmethod
    def ask_yes_no(prompt: str, default_no: bool = True) -> bool:
        raw = input(
            f"{prompt} [{'y' if not default_no else 'Y'}/"
            f"{'N' if not default_no else 'n'}]: ").strip().lower()
        if not raw:
            return not default_no
        return raw in ("y", "yes", "да", "д")

    @classmethod
    def pick_action(cls) -> Optional[MenuAction]:
        labels = list(cls.MENU_LABELS.values())
        choice = Select.select_one(labels)
        for k, v in cls.MENU_LABELS.items():
            if v == choice:
                return k
        return None

    @classmethod
    def choose_url(cls):
        while True:
            action = cls.pick_action()
            if action is None:
                Print.error("Unknown option. Try again.")
                continue

            if action is MenuAction.EXIT:
                Print.info("Exiting.")
                return None

            if action is MenuAction.CLIPBOARD:
                dm = Domain()
                url = dm.get_from_clipboard()
                url = cls.normalize_url(url)
                return url

            if action is MenuAction.VIEW_ALL:
                dm = Domain()
                dm.view_all_from_file()

            if action is MenuAction.REMOVE:
                dm = Domain()
                dm.remove_from_file()
                dm.view_all_from_file()

            if action is MenuAction.SELECT_SAVED:
                dm = Domain()
                print(f"dm: {dm}")
                urls = dm.get_urls_from_file()
                print(f"urls: {urls}")
                if not urls:
                    Print.error("No saved URLs found.")
                    continue
                selected = Select.select_one(urls)
                print(f"selected: {selected}")
                return selected

    @classmethod
    def normalize_url(cls, raw: str) -> Optional[str]:
        s = (raw or "").strip()
        if not s:
            return None

        # если нет схемы — добавим http
        if "://" not in s:
            s = "http://" + s

        try:
            parts = urlsplit(s)
            if not parts.netloc:
                return None
            # уберём хвостовой слеш у path (кроме корня)
            path = parts.path or ""
            if len(path) > 1 and path.endswith("/"):
                path = path.rstrip("/")
            # соберём обратно
            s_norm = urlunsplit(
                (parts.scheme.lower(), parts.netloc, path, parts.query, parts.fragment))
            return s_norm
        except Exception:
            return None
