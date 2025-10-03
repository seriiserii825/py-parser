from typing import TypedDict, Literal


class TChoice(TypedDict):
    key: Literal["page", "sitemap"]
    value: str
