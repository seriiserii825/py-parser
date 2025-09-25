from classes.Select import Select
from modules.get_seo import get_seo
from modules.get_soup_after_download import get_soup_after_download
from modules.get_url import get_url
from modules.images_has_alt import images_has_alt


def main():
    url = get_url()
    if url:
        soup = get_soup_after_download(url)
        menu(soup)


def menu(soup):
    menu_items = ["Check Images", "Check SEO", "Exit"]
    selected = Select.select_one(menu_items)
    if selected == "Check Images":
        images_has_alt(soup)
        menu(soup)
    elif selected == "Check SEO":
        get_seo(soup)
        menu(soup)
    elif selected == "Exit":
        print("Exiting...")
        exit()


if __name__ == "__main__":
    main()
