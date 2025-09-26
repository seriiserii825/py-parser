from classes.Print import Print


def have_lorem(soup):
    lorem_phrases = [
        "lorem ipsum",
        "dolor sit amet",
        "consectetur adipiscing elit",
        "sed do eiusmod tempor incididunt",
        "ut labore et dolore magna aliqua",
        "ut enim ad minim veniam",
        "quis nostrud exercitation ullamco laboris",
        "nisi ut aliquip ex ea commodo consequat",
        "duis aute irure dolor in reprehenderit",
        "in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
        "excepteur sint occaecat cupidatat non proident",
        "sunt in culpa qui officia deserunt mollit anim id est laborum"
    ]

    found_phrases = []

    text = soup.get_text().lower()
    for phrase in lorem_phrases:
        if phrase in text:
            found_phrases.append(phrase)

    if found_phrases:
        Print.error(f"Found {len(found_phrases)} lorem ipsum phrases:")
        for phrase in found_phrases:
            Print.info(f"- {phrase}")
    else:
        Print.success("No lorem ipsum phrases found.")
