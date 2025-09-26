from classes.Select import Select
from modules.duplicate_ids import duplicate_ids
from modules.empty_links import empty_links
from modules.external_links import external_links
from modules.get_seo import get_seo
from modules.get_soup_after_download import get_soup_after_download
from modules.get_url import get_url
from modules.hash_links import hash_links
from modules.have_lorem import have_lorem
from modules.images_has_alt import images_has_alt
from modules.phone_watsapp import phone_watsapp
from modules.spell_check_func import spell_check_func


def main():
    url = get_url()
    if url:
        soup = get_soup_after_download(url)
        menu(soup)


def menu(soup):
    menu_items = ["Check Images", "Check SEO",  "External Links",
                  "Hash Links",   "Empty Links", "Phone Watsapp",  "Duplicate Ids",
                  "Have Lorem",  "SpellCheck", "Exit"]
    selected = Select.select_one(menu_items)
    if selected == "Check Images":
        images_has_alt(soup)
        menu(soup)
    elif selected == "Check SEO":
        get_seo(soup)
        menu(soup)
    elif selected == "External Links":
        external_links(soup)
        menu(soup)
    elif selected == "Hash Links":
        hash_links(soup)
        menu(soup)
    elif selected == "Empty Links":
        empty_links(soup)
        menu(soup)
    elif selected == "Phone Watsapp":
        phone_watsapp(soup)
        menu(soup)
    elif selected == "Duplicate Ids":
        duplicate_ids(soup)
        menu(soup)
    elif selected == "Have Lorem":
        have_lorem(soup)
        menu(soup)
    elif selected == "SpellCheck":
        spell_check_func(soup)
        menu(soup)
    elif selected == "Exit":
        print("Exiting...")
        exit()


if __name__ == "__main__":
    main()
