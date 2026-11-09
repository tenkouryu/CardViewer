#!/usr/bin/env python3
"""Search MTG cards through the Scryfall API."""

import json
import re
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen


API_URL = "https://api.scryfall.com/cards/search"
COLLECTION_URL = "https://api.scryfall.com/cards/collection"
USER_AGENT = "MTGCardViewer/1.0 (Python urllib)"
COLLECTION_INTERVAL = 0.5
REQUEST_INTERVAL = 0.1  # 100ms between requests to respect Scryfall rate limits

_collection_lock = threading.Lock()
_last_collection_request = 0.0
_last_api_request = 0.0
_request_lock = threading.Lock()


def image_url(card: dict, preferred_name: str | None = None) -> str | None:
    """Extract the image URL from a card object.
    
    For double-faced cards, prefers the face matching preferred_name.
    """
    # For single-faced cards
    images = card.get("image_uris")
    if images:
        return images.get("normal")

    # For double-faced cards, try to find matching face
    faces = card.get("card_faces", [])
    
    # If preferred_name is provided, try to find matching face first
    if preferred_name and faces:
        preferred_name_lower = preferred_name.lower()
        for face in faces:
            if face.get("name", "").lower() == preferred_name_lower:
                images = face.get("image_uris")
                if images and images.get("normal"):
                    return images["normal"]
    
    # Fall back to first face with image
    for face in faces:
        images = face.get("image_uris")
        if images and images.get("normal"):
            return images["normal"]
    
    return None


def summarize_card(card: dict, search_name: str | None = None) -> dict:
    """Convert a Scryfall card object to a summary dictionary.
    
    Args:
        card: Scryfall card object
        search_name: The name that was searched for (used for double-faced cards)
    """
    # For double-faced cards, prefer the matching face
    card_name = card.get("name", "")
    preferred_name = None
    
    # If searching for a specific name and it's a double-faced card
    if search_name and "//" in card_name:
        # Try to use the searched name as preferred name
        preferred_name = search_name
    
    result = {
        "name": card.get("name"),
        "printed_name": card.get("printed_name"),  # Japanese name if available
        "type": card.get("type_line"),
        "rules_text": card.get("oracle_text"),
        "set": card.get("set_name"),
        "set_code": card.get("set"),
        "collector_number": card.get("collector_number"),
        "image_url": image_url(card, preferred_name),
        "scryfall_url": card.get("scryfall_uri"),
        "mana_cost": card.get("mana_cost"),
        "power": card.get("power"),
        "toughness": card.get("toughness"),
        "loyalty": card.get("loyalty"),
        "cmc": card.get("cmc"),
        "colors": card.get("colors", []),
    }
    if card.get("card_faces"):
        result["faces"] = [summarize_face(face) for face in card["card_faces"]]
    return result


def summarize_face(face: dict) -> dict:
    """Convert a Scryfall card face to a summary dictionary."""
    images = face.get("image_uris") or {}
    return {
        "name": face.get("name"),
        "type": face.get("type_line"),
        "rules_text": face.get("oracle_text"),
        "image_url": images.get("normal"),
        "mana_cost": face.get("mana_cost"),
        "power": face.get("power"),
        "toughness": face.get("toughness"),
    }


def fetch_page(url: str) -> dict:
    """Fetch and parse a JSON response from the Scryfall API."""
    global _last_api_request
    
    # Rate limiting: enforce minimum interval between requests
    with _request_lock:
        now = time.time()
        elapsed = now - _last_api_request
        if elapsed < REQUEST_INTERVAL:
            delay = REQUEST_INTERVAL - elapsed
            print(f"[DEBUG] Rate limit: waiting {delay:.3f}s")
            time.sleep(delay)
        _last_api_request = time.time()
    
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        print(f"[DEBUG] API request: {url}")
        with urlopen(request, timeout=30) as response:
            data = json.load(response)
            print(f"[DEBUG] API response: {response.status} OK")
            return data
    except HTTPError as error:
        try:
            detail = json.load(error).get("details", str(error))
        except (json.JSONDecodeError, AttributeError):
            detail = str(error)
        print(f"[DEBUG] API error: HTTP {error.code}: {detail}")
        raise RuntimeError(f"Scryfall API returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        print(f"[DEBUG] Connection error: {error.reason}")
        raise RuntimeError(f"Could not connect to the Scryfall API: {error.reason}") from error
    except json.JSONDecodeError as error:
        print(f"[DEBUG] JSON decode error: {error}")
        raise RuntimeError("Scryfall returned invalid JSON.") from error


def is_japanese(text: str) -> bool:
    """Check if text contains Japanese characters."""
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', text))


def fetch_card_by_japanese_name(ja_name: str) -> dict | None:
    """Fetch card information using Japanese card name.
    
    Searches for the Japanese version of the card using lang:ja filter,
    then filters by exact printed_name match.
    """
    try:
        # Search for Japanese cards using lang:ja filter
        query = urlencode({"q": f'"{ja_name}" lang:ja', "unique": "prints"})
        url = f"{API_URL}?{query}"
        print(f"[DEBUG] Searching: {url}")
        response = fetch_page(url)
        
        total = response.get("total_cards", 0)
        print(f"[DEBUG] Total cards found: {total}")
        
        # Find exact match by printed_name
        for i, card in enumerate(response.get("data", [])):
            printed_name = card.get("printed_name", "").strip()
            print(f"[DEBUG] Card {i}: {card.get('name')} / {repr(printed_name)}")
            
            if printed_name == ja_name.strip():
                print(f"[DEBUG] MATCH! Found exact Japanese: {card.get('name')} / {printed_name}")
                return summarize_card(card, search_name=ja_name)
        
        print(f"[DEBUG] No exact match found for: {repr(ja_name.strip())}")
        return None
            
    except RuntimeError as e:
        print(f"[DEBUG] fetch_card_by_japanese_name error: {e}")
        return None


def fetch_card_by_name(name: str) -> dict | None:
    """Fetch a single card by its name.
    
    Supports both English and Japanese card names.
    - For Japanese names: attempts fuzzy matching, then falls back to English search
    - For English names: searches normally
    """
    try:
        # Check if input is Japanese
        if is_japanese(name):
            # Try Japanese-specific lookup first
            card = fetch_card_by_japanese_name(name)
            if card:
                return card
            # If not found, it means the card may not exist or isn't registered
            # Return None so the UI can show "not found"
            return None
        
        # For English names, use /cards/named?exact= for exact match
        # This avoids both-faced cards like "Emeritus of Conflict // Lightning Bolt"
        try:
            url = f"https://api.scryfall.com/cards/named?exact={quote(name)}"
            request = Request(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": USER_AGENT,
                },
            )
            with urlopen(request, timeout=30) as response:
                card = json.load(response)
                return summarize_card(card, search_name=name)
        except HTTPError as e:
            if e.code != 404:
                raise RuntimeError(f"Scryfall API error: {e.code}") from e
        
        # If exact match fails, try fuzzy match
        try:
            url = f"https://api.scryfall.com/cards/named?fuzzy={quote(name)}"
            request = Request(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": USER_AGENT,
                },
            )
            with urlopen(request, timeout=30) as response:
                card = json.load(response)
                return summarize_card(card, search_name=name)
        except HTTPError as e:
            if e.code == 404:
                return None
            raise RuntimeError(f"Scryfall API error: {e.code}") from e
        
    except RuntimeError:
        raise


def fetch_card_by_set_number(set_code: str, collector_number: str) -> dict | None:
    """Fetch a single card by its set code and collector number."""
    try:
        url = f"https://api.scryfall.com/cards/{set_code.lower()}/{collector_number.lower()}"
        card = fetch_page(url)
        return summarize_card(card)
    except RuntimeError as e:
        if "404" in str(e):
            return None
        raise


def search_cards_by_name(name: str, limit: int = 25) -> list[dict]:
    """Search for cards by name pattern.
    
    Supports both English and Japanese names.
    - For Japanese names: exact matches first (sorted by release date), then partial matches, returns top 5
    - For English names: uses full search
    """
    try:
        # Check if input is Japanese
        if is_japanese(name):
            # Search for Japanese cards using lang:ja filter
            query = urlencode({"q": f'"{name}" lang:ja', "unique": "prints"})
            url = f"{API_URL}?{query}"
            response = fetch_page(url)
            
            exact_matches = []
            partial_matches = []
            name_lower = name.strip().lower()
            
            # Separate exact and partial matches
            for card in response.get("data", [])[:100]:  # Check up to 100 results
                printed_name = card.get("printed_name", "").strip()
                printed_name_lower = printed_name.lower()
                
                if printed_name_lower == name_lower:
                    exact_matches.append(card)
                elif name_lower in printed_name_lower:
                    partial_matches.append(card)
            
            # Sort exact matches by release date (newest first)
            exact_matches.sort(
                key=lambda c: c.get("released_at", ""),
                reverse=True
            )
            
            # Sort partial matches by release date (newest first)
            partial_matches.sort(
                key=lambda c: c.get("released_at", ""),
                reverse=True
            )
            
            # Combine: exact matches first, then partial matches
            all_matches = exact_matches + partial_matches
            
            # Summarize cards and limit to 100 results for suggestions
            cards = []
            for card in all_matches[:100]:
                cards.append(summarize_card(card, search_name=name))
            
            print(f"[DEBUG] Japanese search found {len(exact_matches)} exact + {len(partial_matches)} partial matches for: {name} (showing up to 100)")
            return cards
        else:
            # Search for English names using search endpoint
            query = urlencode({"q": name, "unique": "prints"})
            url = f"{API_URL}?{query}"
            response = fetch_page(url)
            
            cards = []
            for card in response.get("data", [])[:limit]:
                cards.append(summarize_card(card, search_name=name))
            return cards
    except RuntimeError:
        raise
