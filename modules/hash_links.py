from classes.Print import Print


def hash_links(sup):
    """Check for links with hashes if have blocks with id on the page"""
    print("\nChecking for links with hashes...")
    links = sup.find_all("a", href=True)
    ids = {tag["id"] for tag in sup.find_all(attrs={"id": True})}
    # hash_links = [link for link in links if link["href"].startswith("#")]
    hash_links = []
    for link in links:
        href = link["href"]
        if href.startswith("#") and len(href) > 1:
            hash_links.append(link)
    if not hash_links:
        Print.success("No links with hashes found.")
        return
    broken_hash_links = []
    for link in hash_links:
        hash_value = link["href"][1:]  # Remove the '#' character
        if hash_value not in ids:
            broken_hash_links.append(link["href"])
    if broken_hash_links:
        print("Broken hash links found:")
        for bl in broken_hash_links:
            Print.error(f"- {bl}")
    else:
        Print.success("All hash links are valid.")
