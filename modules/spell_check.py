import os
import re
import unicodedata
from classes.PathHelper import PathHelper
import hunspell
from classes.Print import Print
from classes.Select import Select

# keep apostrophes and hyphens
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ’'\-]+", re.UNICODE)
SOFT_HYPHENS = ("\u00ad",)  # &shy;


def normalize_text(s: str) -> str:
    # Normalize unicode, remove soft hyphens, replace NBSP with space, strip zero-width chars
    s = unicodedata.normalize("NFKC", s)
    for ch in SOFT_HYPHENS:
        s = s.replace(ch, "")
    s = s.replace("\u00a0", " ")  # NBSP
    s = s.replace("\u200b", "")  # zero-width space
    return s


def extract_visible_text(soup):
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    # Ensure words aren’t glued together across tags
    text = soup.get_text(" ", strip=True)
    return normalize_text(text)


def spell_check(soup):
    ph = PathHelper()
    script_dir = ph.script_directory.parent
    EXCLUDED_FILE_PATH = script_dir / "excluded_words.txt"
    if not EXCLUDED_FILE_PATH.exists():
        os.system(f"touch {EXCLUDED_FILE_PATH}")

    Print.info("Starting spell check...")
    with open(EXCLUDED_FILE_PATH, "r") as f:
        excluded_words = {line.strip().lower() for line in f if line.strip()}

    try:
        h_it = hunspell.HunSpell(
            "/usr/share/hunspell/it_IT.dic", "/usr/share/hunspell/it_IT.aff"
        )
        h_en = hunspell.HunSpell(
            "/usr/share/hunspell/en_US.dic", "/usr/share/hunspell/en_US.aff"
        )

        Print.info("Select language for spell check:")
        lang = Select.select_one(["English", "Italian", "Auto (EN+IT)"])
        h = {"English": h_en, "Italian": h_it}.get(lang, None)

        text = extract_visible_text(soup) + " " + extract_attrs_text(soup)

        misspelled = {}  # original_token -> suggestions

        for match in WORD_RE.finditer(text):
            original = match.group(0)
            token = original

            # Normalize apostrophes to straight ASCII for better matches
            token = token.replace("’", "'")

            # Optionally check hyphenated tokens by parts if whole fails
            def check_with(hun):
                if hun.spell(token):
                    return True
                if "-" in token:
                    parts = [p for p in token.split("-") if p]
                    if parts and all(hun.spell(p) for p in parts):
                        return True
                return False

            # Skip excluded words
            if original.lower() in excluded_words:
                continue

            if h:  # single-language mode
                ok = check_with(h)
                if not ok:
                    suggestions = h.suggest(token)
                    misspelled[original] = suggestions
            else:
                # Auto mode: accept if IT or EN is OK
                ok_it = check_with(h_it)
                ok_en = check_with(h_en)
                if not (ok_it or ok_en):
                    # merge suggestions
                    sugg = list(dict.fromkeys(h_it.suggest(token) + h_en.suggest(token)))
                    misspelled[original] = sugg

        to_exclude = []

        if misspelled:
            Print.error(f"Found {len(misspelled)} misspelled tokens")
            for word, suggestions in misspelled.items():
                print(
                    f"- {word}: "
                    f"{', '.join(suggestions[:8]) if suggestions else 'No suggestions'}"
                )
                to_exclude.append(word)
        else:
            Print.success("No spelling issues found in visible text.")

        if to_exclude:
            Print.info("You can save some of the excluded words to excluded_words.txt")
            agree = input("Save words to a file now?, y/n: ")
            if agree.lower() == "y":
                excludeToFile(to_exclude, EXCLUDED_FILE_PATH)
    except Exception as e:
        Print.error(f"Hunspell dictionaries not found or hunspell not installed. {e}")
        Print.info("sudo pacman -S hunspell hunspell-en_us hunspell-it")



def excludeToFile(words, EXCLUDED_FILE_PATH):
    words_to_exclude = Select.select_term_menu(words)
    with open(EXCLUDED_FILE_PATH, "a") as f:
        for word in words_to_exclude:
            f.write(f"{word}\n")
    Print.info("Excluded words saved to excluded_words.txt")


def extract_attrs_text(soup, attrs=("alt", "title", "placeholder", "aria-label")):
    chunks = []
    for attr in attrs:
        for el in soup.find_all(attrs={attr: True}):
            chunks.append(el.get(attr, ""))
    return normalize_text(" ".join(chunks))
