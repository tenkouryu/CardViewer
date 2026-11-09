"""MTG Card Viewer - Individual card search and display application."""

__version__ = "1.0.0"
__author__ = "MTG Card Viewer"

from .mtg_card_search import (
    fetch_card_by_name,
    fetch_card_by_set_number,
    search_cards_by_name,
    summarize_card,
)

__all__ = [
    "fetch_card_by_name",
    "fetch_card_by_set_number",
    "search_cards_by_name",
    "summarize_card",
]
