from modules.get_seo import get_seo
from modules.get_soup_after_download import get_soup_after_download
from modules.get_url import get_url
from modules.images_has_alt import images_has_alt


def main():
    url = get_url()
    if url:
        soup = get_soup_after_download(url)
        images_has_alt(soup)
        get_seo(soup)


if __name__ == "__main__":
    main()
