"""
GBIF Link Adder for Plant Entities - Thuringia Digital Edition
==============================================================
This script adds GBIF links to plant entities in the HTML document.
It reads the German->Latin mappings from a CSV file (plant_mappings.csv).

Modelled after the animal GBIF link adder script.

Usage in Google Colab:
1. Mount Google Drive:
   from google.colab import drive
   drive.mount('/content/drive')

2. Upload plant_mappings.csv to /content/ (or adjust MAPPING_CSV_PATH)

3. Adjust INPUT_PATH and OUTPUT_PATH below

4. Run this script
"""

# ============================================
# CELL 1: Install dependencies
# ============================================
# !pip install beautifulsoup4 requests

# ============================================
# CELL 2: Imports and Configuration
# ============================================
import requests
import time
import csv
from bs4 import BeautifulSoup
from typing import Optional, Dict, List, Tuple

# File paths (ADJUST THESE)
INPUT_PATH = "/content/drive/MyDrive/Thuringia_digital_edition_output/digital_edition_reussjl_LATEST.html"
OUTPUT_PATH = "/content/digital_edition_reussjl_plants_linked.html"
MAPPING_CSV_PATH = "/content/plant_mappings.csv"  # Upload this file to Colab

# Categories that should get GBIF links (not skipped)
LINKABLE_CATEGORIES = {
    'SPECIES', 'SPECIES_LATIN', 'FAMILY', 'ORDER', 'GENUS', 'CLASS',
    'SUBCLASS', 'SUBFAMILY', 'SUPERFAMILY', 'SUBSPECIES', 'SUBPHYLUM',
    'SUPERCLASS', 'SUBORDER', 'CLADE', 'PHYLUM', 'KINGDOM'
}

# ============================================
# CELL 3: Load Mappings from CSV
# ============================================

def load_mappings_from_csv(csv_path: str) -> Dict[str, Tuple[Optional[str], str]]:
    """
    Load plant mappings from CSV file.

    Returns:
        Dictionary: german_name -> (latin_name, category)
    """
    mappings = {}

    print(f"Loading mappings from: {csv_path}")

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            german_name = row['german_name'].strip()
            latin_name = row['latin_name'].strip() if row['latin_name'].strip() else None
            category = row['category'].strip()
            mappings[german_name] = (latin_name, category)

    print(f"Loaded {len(mappings)} mappings")

    # Print category summary
    categories = {}
    for _, (_, cat) in mappings.items():
        categories[cat] = categories.get(cat, 0) + 1

    print("\nCategory breakdown:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        skip_marker = " (will skip)" if 'SKIP' in cat or cat == 'UNCLEAR' else ""
        print(f"  {cat}: {count}{skip_marker}")

    return mappings

# ============================================
# CELL 4: GBIF API Functions
# ============================================

# Cache for API results
GBIF_CACHE: Dict[str, Optional[int]] = {}

def search_gbif(latin_name: str) -> Optional[int]:
    """
    Search GBIF for a species and return the usageKey.
    Uses caching to avoid duplicate API calls.
    """
    if latin_name in GBIF_CACHE:
        return GBIF_CACHE[latin_name]

    url = "https://api.gbif.org/v1/species/match"
    params = {"name": latin_name, "verbose": True}

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("usageKey") and data.get("matchType") != "NONE":
                usage_key = data["usageKey"]
                GBIF_CACHE[latin_name] = usage_key
                return usage_key
    except requests.RequestException as e:
        print(f"  API error for '{latin_name}': {e}")

    GBIF_CACHE[latin_name] = None
    return None

def get_gbif_url(usage_key: int) -> str:
    """Generate GBIF species page URL."""
    return f"https://www.gbif.org/species/{usage_key}"

# ============================================
# CELL 5: HTML Processing Functions
# ============================================

def create_gbif_link_html(url: str) -> str:
    """
    Create the HTML for a GBIF link.
    Matches the existing format used for plant GBIF links in the edition
    (with data-title-de and data-title-en attributes).
    """
    return (
        f'<a class="gbif-link" '
        f'data-title-de="Auf GBIF anzeigen" '
        f'data-title-en="View on GBIF" '
        f'href="{url}" '
        f'style="margin-left: 4px; font-size: 0.85em; text-decoration: none; '
        f'color: #4a7c59; vertical-align: super;" '
        f'target="_blank" '
        f'title="Auf GBIF anzeigen">'
        f'\U0001f517</a>'
    )

def has_gbif_link(mark_tag) -> bool:
    """Check if a mark tag already has a GBIF link."""
    next_sib = mark_tag.next_sibling
    if next_sib and hasattr(next_sib, 'name') and next_sib.name == 'a':
        return 'gbif-link' in next_sib.get('class', [])
    return False

def should_get_link(category: str) -> bool:
    """Determine if a category should receive a GBIF link."""
    return category in LINKABLE_CATEGORIES

# ============================================
# CELL 6: Main Processing Function
# ============================================

def process_html():
    """Main function to process the HTML and add GBIF links to plant entities."""

    print("=" * 70)
    print("GBIF LINK ADDER FOR PLANT ENTITIES")
    print("Thuringia Digital Edition")
    print("=" * 70)

    # Load mappings from CSV
    print()
    mappings = load_mappings_from_csv(MAPPING_CSV_PATH)

    # Statistics
    stats = {
        'total_plants': 0,
        'already_linked': 0,
        'links_added': 0,
        'skipped_generic': 0,
        'skipped_compound': 0,
        'skipped_named_tree': 0,
        'skipped_epithet': 0,
        'skipped_unclear': 0,
        'skipped_other': 0,
        'not_in_mapping': 0,
        'gbif_not_found': 0,
    }

    # Track which species were processed
    processed_species = {}
    not_found_in_gbif = []
    not_in_mapping_list = []

    print(f"\nReading HTML: {INPUT_PATH}")
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all plant entity marks
    plant_marks = soup.find_all('mark', class_='entity', attrs={'data-type': 'Plant'})
    stats['total_plants'] = len(plant_marks)
    print(f"Found {stats['total_plants']} plant annotations\n")

    print("Processing plants...")
    print("-" * 70)

    for mark in plant_marks:
        german_name = mark.get_text().strip()

        # Skip if already has GBIF link
        if has_gbif_link(mark):
            stats['already_linked'] += 1
            continue

        # Check if in mapping
        if german_name not in mappings:
            stats['not_in_mapping'] += 1
            if german_name not in not_in_mapping_list:
                not_in_mapping_list.append(german_name)
                print(f"  \u26a0\ufe0f  NOT IN MAPPING: {german_name}")
            continue

        latin_name, category = mappings[german_name]

        # Skip based on category
        if 'SKIP' in category:
            if 'GENERIC' in category:
                stats['skipped_generic'] += 1
            elif 'COMPOUND' in category:
                stats['skipped_compound'] += 1
            elif 'NAMED_TREE' in category:
                stats['skipped_named_tree'] += 1
            elif 'EPITHET' in category:
                stats['skipped_epithet'] += 1
            else:
                stats['skipped_other'] += 1
            continue

        if category == 'UNCLEAR':
            stats['skipped_unclear'] += 1
            continue

        # Should get a link - query GBIF
        if latin_name:
            usage_key = search_gbif(latin_name)

            if usage_key:
                gbif_url = get_gbif_url(usage_key)
                link_html = create_gbif_link_html(gbif_url)
                link_tag = BeautifulSoup(link_html, 'html.parser')
                mark.insert_after(link_tag)
                stats['links_added'] += 1

                if german_name not in processed_species:
                    processed_species[german_name] = (latin_name, usage_key)
                    print(f"  \u2713 {german_name} \u2192 {latin_name} (GBIF: {usage_key})")
            else:
                stats['gbif_not_found'] += 1
                if latin_name not in [x[1] for x in not_found_in_gbif]:
                    not_found_in_gbif.append((german_name, latin_name))
                    print(f"  \u2717 {german_name} \u2192 {latin_name} (NOT FOUND IN GBIF)")

        # Be nice to the API
        time.sleep(0.1)

    # Save the modified HTML
    print(f"\n{'-' * 70}")
    print(f"Saving to: {OUTPUT_PATH}")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total plant annotations:      {stats['total_plants']}")
    print(f"Already had GBIF links:       {stats['already_linked']}")
    print(f"GBIF links added:             {stats['links_added']}")
    print(f"Skipped (generic terms):      {stats['skipped_generic']}")
    print(f"Skipped (compound terms):     {stats['skipped_compound']}")
    print(f"Skipped (named trees):        {stats['skipped_named_tree']}")
    print(f"Skipped (bare epithets):      {stats['skipped_epithet']}")
    print(f"Skipped (other):              {stats['skipped_other']}")
    print(f"Skipped (unclear):            {stats['skipped_unclear']}")
    print(f"Not in mapping CSV:           {stats['not_in_mapping']}")
    print(f"Not found in GBIF:            {stats['gbif_not_found']}")

    if not_in_mapping_list:
        print("\n" + "=" * 70)
        print("PLANTS NOT IN MAPPING CSV (add to CSV file)")
        print("=" * 70)
        for name in not_in_mapping_list:
            print(f"  - {name}")

    if not_found_in_gbif:
        print("\n" + "=" * 70)
        print("SPECIES NOT FOUND IN GBIF (may need name correction)")
        print("=" * 70)
        for german, latin in not_found_in_gbif:
            print(f"  {german} \u2192 {latin}")

    print(f"\n\u2705 Done! Output saved to: {OUTPUT_PATH}")

    return stats

# ============================================
# CELL 7: Run the script
# ============================================

if __name__ == "__main__":
    process_html()
