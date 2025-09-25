from classes.Print import Print


def external_links(sup):
    links = []
    for a in sup.find_all('a', href=True):
        href = a['href']
        if href.startswith('http://') or href.startswith('https://'):
            target_blank = a.get('target') == '_blank'
            rel_noopener = 'noopener' in (a.get('rel') or [])
            if target_blank and not rel_noopener:
                Print.error(
                    f"External link, target='_blank' missing rel='noopener': {href}")
                links.append(href)
    if not links:
        Print.success(
            "No external links with target='_blank' missing rel='noopener' found.")
