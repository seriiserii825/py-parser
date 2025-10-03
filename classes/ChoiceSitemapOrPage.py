from classes.Select import Select
from my_types.TChoice import TChoice


class ChoiceSitemapOrPage:
    @staticmethod
    def get_choice() -> TChoice:
        questions: list[TChoice] = [
            {"key": "page", "value": "Check a single page"},
            {"key": "sitemap", "value": "Check a sitemap (multiple pages)"}
        ]

        keys = [q["key"] for q in questions]
        selected_key = Select.select_one(keys)  # "page" or "sitemap"
        choice: TChoice = next(
            q for q in questions if q["key"] == selected_key)
        return choice
