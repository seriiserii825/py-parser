from urllib.parse import urlparse, urlunparse
from classes.Print import Print
from classes.Select import Select
from modules.get_soup_after_download import get_soup_after_download


def all_seo(url):
    if not url:
        Print.error("URL is required.")
        exit(1)
    url = to_root_url(url)
    xml_sitemap_url = f"{url}sitemap_index.xml"
    agree = input("Do you want to check the sitemap.xml? (y/n): ").strip().lower()
    if agree == "y":
        pages = {}
        sup = get_soup_after_download(xml_sitemap_url)
        print(f"{sup}: sup")
        loc_all = sup.select("loc")
        links = []
        for loc in loc_all:
            url = loc.get_text()
            links.append(url)
        selected_url = Select.select_one(links)
        page_soup = get_soup_after_download(selected_url)
        loc_all_page = page_soup.select("loc")
        missing_data = []
        for loc in loc_all_page:
            page_url = loc.get_text()
            print(f"Checking SEO for: {page_url}")
            page_soup = get_soup_after_download(page_url)
            title = page_soup.title.string if page_soup.title else "No title"
            description_tag = page_soup.select('meta[name="description"]')
            if description_tag:
                description_text = description_tag[0]["content"]
            else:
                description_text = "No description"
            og_image = page_soup.select_one('meta[property="og:image"]')
            h1_tags = page_soup.find_all("h1")
            h1_text = [h1.get_text(strip=True) for h1 in h1_tags]
            h2_tags = page_soup.find_all("h2")
            h2_text = [h2.get_text(strip=True) for h2 in h2_tags]
            h3_tags = page_soup.find_all("h3")
            h3_text = [h3.get_text(strip=True) for h3 in h3_tags]
            pages[page_url] = {
                "title": title,
                "description": description_text,
                "og_image": og_image["content"] if og_image else "No OG image",
                "h1_tags": h1_text,
                "h2_text": h2_text,
                "h3_text": h3_text,
            }
        for page, seo_data in pages.items():
            Print.info(f"\nPage URL: {page}")
            print(f"Title: {seo_data['title']}")
            print(f"Description: {seo_data['description']}")
            print(f"OG Image: {seo_data['og_image']}")
            if seo_data["h1_tags"]:
                print("---------" * 20)
                print_h_tag(seo_data["h1_tags"], "H1")
            if seo_data["h2_text"]:
                print("---------" * 20)
                print_h_tag(seo_data["h2_text"], "H2")
            if seo_data["h3_text"]:
                print("---------" * 20)
                print_h_tag(seo_data["h3_text"], "H3")
    else:
        print("Skipping sitemap.xml check.")


def print_h_tag(tags, tag_type):
    for _, tag in enumerate(tags, start=1):
        print(f"{tag_type}: {tag}")


def to_root_url(url: str) -> str:
    """
    Transform any inner page URL to the site root URL.
    Keeps scheme (http/https) and domain, drops path/query/fragment.
    """
    parsed = urlparse(url)
    root = parsed._replace(path="/", params="", query="", fragment="")
    return urlunparse(root)

def get_missing_seo_data(pages):
    missing_data = []
    for page_url, seo_data in pages.items():
        missing_fields = []
        if seo_data["title"] == "No title":
            missing_fields.append("title")
        if seo_data["description"] == "No description":
            missing_fields.append("description")
        if seo_data["og_image"] == "No OG image":
            missing_fields.append("og_image")
        if not seo_data["h1_tags"]:
            missing_fields.append("h1_tags")
        if not seo_data["h2_text"]:
            missing_fields.append("h2_text")
        if not seo_data["h3_text"]:
            missing_fields.append("h3_text")
        if missing_fields:
            missing_data.append((page_url, missing_fields))
    return missing_data
