from classes.MyTable import MyTable
from classes.Print import Print


def get_seo(sup):
    title = sup.title.string if sup.title else "No title found"
    description = ""
    description_tag = sup.find("meta", attrs={"name": "description"})
    if description_tag and "content" in description_tag.attrs:
        description = description_tag["content"]
    else:
        description = ""

    og_image = sup.find("meta", property="og:image")
    if og_image and "content" in og_image.attrs:
        Print.success(f"OG Image: {og_image['content']}")
    else:
        Print.error("No OG Image found")

    table_columns = ["Tag", "Text"]
    table_rows = []

    for level in range(1, 6):
        tags = get_tags(f"h{level}", sup)
        for text in tags:
            table_rows.append([f"H{level}", text])

    mt = MyTable()
    mt.show("Headings", table_columns, table_rows)

    if title:
        Print.success(f"Title tag found: {title}")
    else:
        Print.error("No title tag found")
    if description:
        Print.success(f"Meta description found: {description}")
    else:
        Print.error("No meta description found")


def get_tags(tag_name, sup) -> list[str]:
    tags = sup.find_all(tag_name)
    out: list[str] = []
    for tag in tags:
        # separator=" " turns <br> (and other inline elements) into spaces
        text = tag.get_text(separator=" ", strip=True)
        if text:
            out.append(text)
    return out
