from classes.Print import Print


def empty_links(soup):
    empty_links_list = []
    for link in soup.find_all('a', href=True):
        if link['href'].strip() == '' or link['href'].strip() == '#':
            empty_links_list.append(link)

    if empty_links_list:
        Print.error(f"Found {len(empty_links_list)} empty links:")
        for link in empty_links_list:
            Print.info(link)
    else:
        Print.success("No empty links found.")
