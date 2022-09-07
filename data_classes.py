from dataclasses import dataclass
from dataclasses import field
from typing import List

@dataclass
class CardArticle:
    condition: str
    language: str
    price: float
    amount: int

@dataclass
class Card:
    name: str
    language_id: str
    expansion_id: str
    rarity: str
    article_list: List[CardArticle]

