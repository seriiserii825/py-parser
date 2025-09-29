from urllib.parse import urlparse, urlunparse
from classes.MyTable import MyTable
from classes.Print import Print
from classes.Select import Select
from modules.get_soup_after_download import get_soup_after_download


class AllSeo:
    def __init__(self, url, soup):
        if not url:
            Print.error("URL is required.")
            exit(1)
        self.url = self.to_root_url(url)
        self.xml_sitemap_url = f"{url}sitemap_index.xml"
        self.soup = soup

    def to_root_url(self, url: str) -> str:
        """
        Transform any inner page URL to the site root URL.
        Keeps scheme (http/https) and domain, drops path/query/fragment.
        """
        parsed = urlparse(url)
        root = parsed._replace(path="/", params="", query="", fragment="")
        return urlunparse(root)

    def print_h_tag(self, tags, tag_type):
        for _, tag in enumerate(tags, start=1):
            print(f"{tag_type}: {tag}")

    def forPage(self, sup):
        title = sup.title.string if sup.title else "No title found"
        description = ""
        description_tag = sup.find("meta", attrs={"name": "description"})
        if description_tag and "content" in description_tag.attrs:
            description = description_tag["content"]
        else:
            description = ""

        if title:
            Print.success(f"Title tag found: {title}")
        else:
            Print.error("No title tag found")
        if description:
            Print.success(f"Meta description found: {description}")
        else:
            Print.error("No meta description found")

        og_image = sup.find("meta", property="og:image")
        if og_image and "content" in og_image.attrs:
            Print.success(f"OG Image: {og_image['content']}")
        else:
            Print.error("No OG Image found")

        table_columns = ["Tag", "Text"]
        table_rows = []

        for level in range(1, 6):
            tags = self.get_tags_from_soup(f"h{level}", sup)
            for text in tags:
                table_rows.append([f"H{level}", text])

        mt = MyTable()
        mt.show("Headings", table_columns, table_rows)

    def get_tags_from_soup(self, tag_name, sup) -> list[str]:
        tags = sup.find_all(tag_name)
        out: list[str] = []
        for tag in tags:
            # separator=" " turns <br> (and other inline elements) into spaces
            text = tag.get_text(separator=" ", strip=True)
            if text:
                out.append(text)
        return out

    def select_a_page(self):
        pages = self.get_sitemap_pages_url()
        if not pages:
            Print.error("No pages found in sitemap.")
            return
        selected_page = Select.select_one(pages)
        if not selected_page:
            Print.error("No page selected.")
            return
        page_soup = get_soup_after_download(selected_page)
        if not page_soup:
            Print.error(f"Failed to download or parse the page: {selected_page}")
            return
        self.forPage(page_soup)

    def get_sitemap_pages_url(self):
        root_url = self.to_root_url(self.url)
        pages_sitemap_url = f"{root_url}/page-sitemap.xml"
        pages = []
        sup = get_soup_after_download(pages_sitemap_url)
        loc_all = sup.select("loc")
        for loc in loc_all:
            url = loc.get_text()
            pages.append(url)
        return pages

    def show_all_pages(self):
        pages = {}
        sup = get_soup_after_download(self.xml_sitemap_url)
        print(f"{sup}: sup")
        loc_all = sup.select("loc")
        links = []
        for loc in loc_all:
            url = loc.get_text()
            links.append(url)
        selected_url = Select.select_one(links)
        page_soup = get_soup_after_download(selected_url)
        loc_all_page = page_soup.select("loc")
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
                self.print_h_tag(seo_data["h1_tags"], "H1")
            if seo_data["h2_text"]:
                print("---------" * 20)
                self.print_h_tag(seo_data["h2_text"], "H2")
            if seo_data["h3_text"]:
                print("---------" * 20)
                self.print_h_tag(seo_data["h3_text"], "H3")
