from urllib.parse import urlparse, urlunparse
from classes.AllSeo import AllSeo
from classes.Print import Print
from classes.Select import Select
from modules.get_soup_after_download import get_soup_after_download


def all_seo(url, soup):
    als = AllSeo(url, soup)
    menu_options = ["Show current Page", "Select a page", "Missing meta", "Exit"]
    selected_option = Select.select_one(menu_options)
    if selected_option == "Exit":
        Print.error("Exiting the program.")
        exit(0)
    elif selected_option == "Show current Page":
        als.forPage(soup)
    elif selected_option == "Select a page":
        als.select_a_page()
    elif selected_option == "Missing meta":
        als.missing_meta(soup)
    else:
        Print.error("Invalid option selected.")
        exit(1)
