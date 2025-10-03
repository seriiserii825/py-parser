from classes.ChoiceSitemapOrPage import ChoiceSitemapOrPage
from classes.MenuAction import MainMenu

from typing import Literal

TChoiceKey = Literal["page", "sitemap", "exit"]


def main_menu() -> tuple[TChoiceKey, str]:
    url = MainMenu.choose_url()
    choice = ChoiceSitemapOrPage.get_choice()
    if choice["key"] == "page":
        if url is None:
            return "exit", ""
        return "page", url
    if choice["key"] == "sitemap":
        if url is None:
            return "exit", ""
        return "sitemap", url
    if url is None:
        return "exit", ""
    return "exit", url
