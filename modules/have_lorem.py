import re
from bs4 import BeautifulSoup, Comment
from classes.Print import Print

LOREM_PHRASES = [
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
    "sunt in culpa qui officia deserunt mollit anim id est laborum",
]

# build regexes that tolerate any whitespace/punct between words
PHRASE_REGEXES = [
    re.compile(
        r"\b" + r"\s*".join(map(re.escape, phrase.split())) + r"\b",
        re.IGNORECASE,
    )
    for phrase in LOREM_PHRASES
]


def _is_visible_text(element):
    """Filter out text in unwanted parents."""
    parent = element.parent.name if element.parent else ""
    if parent in ("script", "style", "noscript", "template", "head"):
        return False
    return True


def _shorten(s, keep=90):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= keep else s[:keep] + "…"


def have_lorem(soup: BeautifulSoup) -> None:
    # 1) remove scripts/styles/noscript/template nodes entirely
    for tag in soup.find_all(["script", "style", "noscript", "template"]):
        tag.decompose()

    # 2) remove HTML comments
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()

    # 3) iterate visible text nodes
    found = []
    for node in soup.find_all(string=True):
        if not _is_visible_text(node):
            continue
        text = node.string or ""
        if not text.strip():
            continue

        # normalize whitespace (incl. &nbsp; -> space)
        norm = text.replace("\xa0", " ")
        for rx, phrase in zip(PHRASE_REGEXES, LOREM_PHRASES):
            m = rx.search(norm)
            if m:
                ctx = _shorten(norm[max(0, m.start() - 40) : m.end() + 40])
                found.append((phrase, node.parent.name, ctx))
                break  # one phrase is enough per node

    if found:
        Print.error(f"Found {len(found)} lorem ipsum phrase(s):")
        for phrase, tag, ctx in found:
            Print.info(f"- {phrase} (in <{tag}>) :: “{ctx}”")
    else:
        Print.success("No lorem ipsum phrases found.")
