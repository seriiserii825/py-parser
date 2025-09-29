import os
import re
import unicodedata
from classes.PathHelper import PathHelper
import hunspell
from classes.Print import Print
from classes.Select import Select


class SpellCheck:
    def __init__(self):
        self.WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ’'\-]+", re.UNICODE)
        self.SOFT_HYPHENS = ("\u00ad",)  # &shy;
        ph = PathHelper()
        script_dir = ph.script_directory.parent
        self.EXCLUDED_FILE_PATH = script_dir / "excluded_words.txt"
        if not self.EXCLUDED_FILE_PATH.exists():
            os.system(f"touch {self.EXCLUDED_FILE_PATH}")

        self.h_it = hunspell.HunSpell(
            "/usr/share/hunspell/it_IT.dic", "/usr/share/hunspell/it_IT.aff"
        )
        self.h_en = hunspell.HunSpell(
            "/usr/share/hunspell/en_US.dic", "/usr/share/hunspell/en_US.aff"
        )

    def normalize_text(self, s: str) -> str:
        # Normalize unicode, remove soft hyphens,
        # replace NBSP with space, strip zero-width chars
        s = unicodedata.normalize("NFKC", s)
        for ch in self.SOFT_HYPHENS:
            s = s.replace(ch, "")
        s = s.replace("\u00a0", " ")  # NBSP
        s = s.replace("\u200b", "")  # zero-width space
        return s

    def extract_visible_text(self, soup):
        for t in soup(["script", "style", "noscript"]):
            t.decompose()
        # Ensure words aren’t glued together across tags
        text = soup.get_text(" ", strip=True)
        return self.normalize_text(text)

    def spell_check(self, soup):
        Print.info("Starting spell check...")
        excluded_words = self.get_excluded_words_from_file()

        try:
            Print.info("Select language for spell check:")
            lang = Select.select_one(["English", "Italian", "Auto (EN+IT)"])
            h = {"English": self.h_en, "Italian": self.h_it}.get(lang, None)
            text = self.extract_visible_text(
                soup) + " " + self.extract_attrs_text(soup)

            misspelled = self.get_misspelled_words(
                text, excluded_words, h)
            misspelled = self.filter_uppercase_words(misspelled)
            self.show_misspelled(misspelled)
            self.add_to_excluded(misspelled.keys())

        except Exception as e:
            Print.error(
                f"Hunspell dictionaries not found or hunspell not installed. {e}")
            Print.info("sudo pacman -S hunspell hunspell-en_us hunspell-it")

    def filter_uppercase_words(self, misspelled):
        # Filter out words that are all uppercase (likely acronyms)
        return {word: sugg for word, sugg in misspelled.items() if not word.isupper()}

    def add_to_excluded(self, excluded_words):
        Print.info(
            "You can save some of the excluded words to excluded_words.txt")
        agree = input("Save words to a file now?, y/n: ")
        if agree.lower() == "y":
            selected_words = Select.select_with_fzf(excluded_words)
            self.excludeToFile(selected_words, self.EXCLUDED_FILE_PATH)

    def get_misspelled_words(self, text, excluded_words, h):
        misspelled = {}  # original_token -> suggestions
        for match in self.WORD_RE.finditer(text):
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
                ok_it = check_with(self.h_it)
                ok_en = check_with(self.h_en)
                if not (ok_it or ok_en):
                    # merge suggestions
                    sugg = list(dict.fromkeys(
                        self.h_it.suggest(token) + self.h_en.suggest(token)))
                    misspelled[original] = sugg
        return misspelled

    def show_misspelled(self, misspelled):
        if misspelled:
            Print.error(f"Found {len(misspelled)} misspelled tokens")
            for word, suggestions in misspelled.items():
                self.print_word(word, suggestions)
        else:
            Print.success("No spelling issues found in visible text.")

    def get_excluded_words_from_file(self):
        with open(self.EXCLUDED_FILE_PATH, "r") as f:
            excluded_words = {line.strip().lower()
                              for line in f if line.strip()}
        return excluded_words

    def extract_attrs_text(self, soup, attrs=("alt", "title",
                                              "placeholder", "aria-label")):
        chunks = []
        for attr in attrs:
            for el in soup.find_all(attrs={attr: True}):
                chunks.append(el.get(attr, ""))
        return self.normalize_text(" ".join(chunks))

    def excludeToFile(self, words, EXCLUDED_FILE_PATH):
        with open(EXCLUDED_FILE_PATH, "a") as f:
            for word in words:
                f.write(f"{word}\n")
        Print.info("Excluded words saved to excluded_words.txt")

    def print_word(self, word, suggestions):
        print(
            f"- {word}: "
            f"{', '.join(suggestions[:8]) if suggestions else 'No suggestions'}"
        )
