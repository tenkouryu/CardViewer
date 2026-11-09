#!/usr/bin/env python3
"""Test Japanese MTG card search with Scryfall API"""

import requests
import json

def test_search(query, description, include_multilingual=False):
    print(f"\n{description}")
    print("=" * 60)
    print(f"Query: {query}")
    try:
        params = {
            'q': query,
            'unique': 'prints'
        }
        if include_multilingual:
            params['include_multilingual'] = 'true'
            
        response = requests.get('https://api.scryfall.com/cards/search',
                              params=params,
                              timeout=10)
        
        if response.status_code == 404:
            print("No results found (404)")
            return False
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('total_cards', 0) > 0:
            card = result['data'][0]
            print(f"[OK] Found {result['total_cards']} result(s)")
            print(f"  English name: {card.get('name')}")
            print(f"  Printed name: {card.get('printed_name', 'N/A')}")
            print(f"  Language: {card.get('lang')}")
            print(f"  Set: {card.get('set_name')}")
            return True
        else:
            print(f"[NO] No results found")
            return False
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return False

if __name__ == '__main__':
    print("MTG Card Viewer - Japanese Search Test")
    print("=" * 60)
    
    # Test 1: Basic English search without multilingual
    test_search('Lightning Bolt', "Test 1: English search (no multilingual)")
    
    # Test 2: English search WITH multilingual
    test_search('Lightning Bolt', "Test 2: English search (WITH multilingual)", include_multilingual=True)
    
    # Test 3: Japanese name with multilingual
    test_search('ライトニング・ボルト', "Test 3: Japanese name (WITH multilingual)", include_multilingual=True)
    
    # Test 4: Search for Japanese version specifically
    test_search('Lightning Bolt lang:ja', "Test 4: English name + lang:ja (WITH multilingual)", include_multilingual=True)
    
    # Test 5: Just check what happens with single card
    print(f"\n\nTest 5: Direct single card lookup")
    print("=" * 60)
    try:
        # Try to get a specific card directly
        response = requests.get('https://api.scryfall.com/cards/named',
                              params={'exact': 'Lightning Bolt'},
                              timeout=10)
        response.raise_for_status()
        card = response.json()
        print(f"[OK] Found card: {card.get('name')}")
        print(f"  Printed: {card.get('printed_name', 'N/A')}")
        print(f"  Lang: {card.get('lang')}")
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
