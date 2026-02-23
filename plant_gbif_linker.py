"""
GBIF Link Adder for Plant Entities - Thuringia Digital Edition
==============================================================
This script adds GBIF links to plant entities in the HTML document.
It reads the German->Latin mappings from a CSV file (plant_mappings.csv).

IMPORTANT: Uses regex-based insertion (NOT BeautifulSoup) to avoid
corrupting JavaScript, inline JSON, and CSS in the HTML file.

Usage in Google Colab:
1. Clone the repo:
   !git clone --branch claude/match-plants-gbif-b1sNr https://github.com/Maelkolb/Thuringia-digital-edition.git

2. Run:
   %run /content/Thuringia-digital-edition/plant_gbif_linker.py
"""

# ============================================
# CELL 1: Install dependencies
# ============================================
# !pip install requests

# ============================================
# CELL 2: Imports and Configuration
# ============================================
import requests
import time
import csv
import re
import html
from typing import Optional, Dict, Tuple

# File paths (ADJUST THESE)
INPUT_PATH = "/content/drive/MyDrive/Thuringia_digital_edition_output/digital_edition_reussjl_LATEST.html"
OUTPUT_PATH = "/content/digital_edition_reussjl_plants_linked.html"
MAPPING_CSV_PATH = "/content/plant_mappings.csv"

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
# CELL 5: HTML Processing Functions (Regex-based)
# ============================================

def create_gbif_link_html(url: str) -> str:
    """
    Create the HTML for a GBIF link.
    Matches the existing format used for plant/animal GBIF links in the edition.
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

# Regex pattern to match Plant entity <mark> tags
# Captures the full mark tag and the text content inside it
PLANT_MARK_PATTERN = re.compile(
    r'(<mark\s+class="entity"\s+data-type="Plant"[^>]*>)(.*?)(</mark>)'
    r'(\s*<a\s+class="gbif-link"[^>]*>[^<]*</a>)?',
    re.DOTALL
)

def extract_text_from_html(html_fragment: str) -> str:
    """Extract plain text from a small HTML fragment (strip tags)."""
    return re.sub(r'<[^>]+>', '', html_fragment).strip()

# ============================================
# CELL 6: Main Processing Function
# ============================================

def process_html():
    """
    Main function to process the HTML and add GBIF links to plant entities.
    Uses regex-based replacement to preserve all JS/CSS/JSON in the HTML intact.
    """

    print("=" * 70)
    print("GBIF LINK ADDER FOR PLANT ENTITIES")
    print("Thuringia Digital Edition")
    print("(Regex-based - preserves JS/CSS/JSON)")
    print("=" * 70)

    # Load mappings from CSV
    print()
    mappings = load_mappings_from_csv(MAPPING_CSV_PATH)

    # Pre-query GBIF for all linkable species to build a lookup table
    # This avoids querying inside the regex callback
    print("\nQuerying GBIF API for all linkable species...")
    print("-" * 70)

    gbif_lookup = {}  # german_name -> gbif_link_html or None
    processed_species = {}
    not_found_in_gbif = []

    for german_name, (latin_name, category) in mappings.items():
        if 'SKIP' in category or category == 'UNCLEAR':
            continue
        if category not in LINKABLE_CATEGORIES:
            continue
        if not latin_name:
            continue

        usage_key = search_gbif(latin_name)
        if usage_key:
            gbif_url = get_gbif_url(usage_key)
            gbif_lookup[german_name] = create_gbif_link_html(gbif_url)
            processed_species[german_name] = (latin_name, usage_key)
            print(f"  \u2713 {german_name} \u2192 {latin_name} (GBIF: {usage_key})")
        else:
            not_found_in_gbif.append((german_name, latin_name))
            print(f"  \u2717 {german_name} \u2192 {latin_name} (NOT FOUND IN GBIF)")

        time.sleep(0.1)

    print(f"\nGBIF lookup ready: {len(gbif_lookup)} species with links")

    # Statistics
    stats = {
        'total_plants': 0,
        'already_linked': 0,
        'links_added': 0,
        'skipped_category': 0,
        'not_in_mapping': 0,
        'gbif_not_found': 0,
    }
    not_in_mapping_list = []

    # Read the HTML as a raw string
    print(f"\nReading HTML: {INPUT_PATH}")
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        html_content = f.read()

    print(f"File size: {len(html_content):,} bytes")

    # Count total plant marks
    stats['total_plants'] = len(re.findall(
        r'<mark\s+class="entity"\s+data-type="Plant"', html_content
    ))
    print(f"Found {stats['total_plants']} plant annotations\n")

    print("Inserting GBIF links via regex replacement...")
    print("-" * 70)

    def replace_plant_mark(match):
        """Callback for regex substitution."""
        mark_open = match.group(1)   # <mark class="entity" data-type="Plant" ...>
        mark_inner = match.group(2)  # text content
        mark_close = match.group(3)  # </mark>
        existing_link = match.group(4)  # existing <a class="gbif-link"...> or None

        german_name = extract_text_from_html(mark_inner).strip()

        # Already has a GBIF link - keep as-is
        if existing_link:
            stats['already_linked'] += 1
            return match.group(0)

        # Not in mapping
        if german_name not in mappings:
            stats['not_in_mapping'] += 1
            if german_name not in not_in_mapping_list:
                not_in_mapping_list.append(german_name)
            return match.group(0)

        _, category = mappings[german_name]

        # Skip based on category
        if 'SKIP' in category or category == 'UNCLEAR' or category not in LINKABLE_CATEGORIES:
            stats['skipped_category'] += 1
            return match.group(0)

        # Has a GBIF link to add?
        if german_name in gbif_lookup:
            stats['links_added'] += 1
            return mark_open + mark_inner + mark_close + gbif_lookup[german_name]
        else:
            stats['gbif_not_found'] += 1
            return match.group(0)

    # Apply regex replacement
    html_output = PLANT_MARK_PATTERN.sub(replace_plant_mark, html_content)

    # Save the modified HTML
    print(f"\nSaving to: {OUTPUT_PATH}")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_output)

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total plant annotations:      {stats['total_plants']}")
    print(f"Already had GBIF links:       {stats['already_linked']}")
    print(f"GBIF links added:             {stats['links_added']}")
    print(f"Skipped (category):           {stats['skipped_category']}")
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
