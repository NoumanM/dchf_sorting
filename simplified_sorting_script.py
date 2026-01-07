"""
Simplified DCHF Data Sorting Script
Sorts provider data according to specified priority:
1. Source (custom order)
2. Specialty (alphabetical)
3. County (custom order)
4. Group Name (alphabetical)
5. Last Name (alphabetical)

After sorting, translates the Specialty column to Spanish.
"""

import csv
import chardet
from datetime import date
from pathlib import Path
from spanish_utils import Spanish_Utils
try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    print("Warning: deep_translator not installed. Spanish translation will be skipped.")

# Import existing Spanish translations
try:
    spanish_translations = Spanish_Utils.add_spanish.copy()
    print(f"Loaded {len(spanish_translations)} existing Spanish translations")
except ImportError:
    spanish_translations = {}
    print("Warning: spanish_utils.py not found. Starting with empty translation dictionary.")

def add_spanish_to_csv(text):
    for i in range(3):
        try:
            if text.strip() in spanish_translations.keys():
                return spanish_translations[text.strip()]
            if '-' not in text and '/' not in text:
                translated = GoogleTranslator(source='en', target='es').translate(text.strip())
                new_text = translated
            else:
                all_chunks = text.split('-')
                new_text = ''
                for chunk in all_chunks:
                    translated = GoogleTranslator(source='en', target='es').translate(chunk.strip())
                    new_text += f"{translated} - "

            if new_text.endswith('- '):
                new_text = new_text[:-2].strip()
            print(f"'{text}': '{new_text}'")
            spanish_translations[text.strip()] = f"{text} / {new_text}"
            return f"{text} / {new_text}"
        except Exception as ex:
            print(f"'{text}': '{ex}'")

    return 'NULL'

def detect_encoding(file_path):
    """Detect the encoding of a file."""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']


def get_source_priority(source):
    """Return priority value for Source column (lower = higher priority)."""
    source_order = {
        'PCP': 1,
        'Specialist': 2,
        'BehavioralHealthSpecialist': 3,
        'Dental': 4,
        'Vision': 5,
        'Facility': 6,
        'Pharmacy': 7,
    }
    # Return priority, or 999 for unknown sources (they sort last)
    return source_order.get(source, 999)


def get_county_priority(county):
    """Return priority value for County column (lower = higher priority)."""
    county_order = {
        'District of Columbia': 1,
        'Montgomery': 2,
        'Prince Georges': 3,
        'Arlington': 4,
        'Fairfax': 5,
        'Fairfax City': 6,
        'Manassas City': 7,
        'Prince William': 8,
    }

    # Handle Ward entries - they should be grouped with District of Columbia
    if county and 'Ward' in county:
        return 1

    # Return priority, or 999 for unknown counties (they sort last)
    return county_order.get(county, 999)


def capitalize_address_directions(address):
    """Capitalize directional abbreviations in address (Ne -> NE, etc.)."""
    if not address:
        return address

    import re
    replacement_dict = {"Ne": "NE", "Se": "SE", "Nw": "NW", "Sw": "SW"}
    return re.sub(
        r'\b(Ne|Se|Nw|Sw)\b',
        lambda x: replacement_dict.get(x.group(0), x.group(0)),
        address
    )


def create_sort_key(row_dict):
    """Create a tuple for sorting based on the priority rules."""
    return (
        get_source_priority(row_dict.get('Source', '')),           # 1. Source (custom)
        row_dict.get('Specialty', '').lower(),                     # 2. Specialty (alphabetical)
        get_county_priority(row_dict.get('County', '')),           # 3. County (custom)
        row_dict.get('GroupName', '').lower(),                     # 4. Group Name (alphabetical)
        row_dict.get('LastName', '').lower()                       # 5. Last Name (alphabetical)
    )


def process_csv_file(input_file, output_file):
    """Read, sort, and write CSV data according to specifications."""

    print(f"Reading input file: {input_file}")

    # Detect encoding
    encoding = detect_encoding(input_file)
    print(f"Detected encoding: {encoding}")

    # Read all data
    data_rows = []
    with open(input_file, 'r', encoding=encoding, errors='ignore') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames

        for row in reader:
            # Capitalize address directions
            if 'AddressLine1' in row:
                row['AddressLine1'] = capitalize_address_directions(row['AddressLine1'])
            data_rows.append(row)

    print(f"Read {len(data_rows)} rows")

    # Sort the data
    print("Sorting data...")
    data_rows.sort(key=create_sort_key)
    # Assign spanish translation
    new_data_rows = []
    for row in data_rows:
        specialty = row.get('Specialty', 'Unknown')
        translated_specialty = add_spanish_to_csv(specialty)
        row['Specialty'] = translated_specialty
        if row['County'] and 'ward' in row['County'].lower():
            row['County'] = 'District of Columbia'
        if row['ProviderSuffix'] and row['ProviderSuffix'] == 'NULL':
            row['ProviderSuffix'] = ''
        new_data_rows.append(row)
    # Write sorted data
    print(f"Writing output file: {output_file}")
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(new_data_rows)

    print(f"Successfully wrote {len(new_data_rows)} rows to {output_file}")

    # Print summary statistics
    print("\n--- Summary Statistics ---")

    # Count by Source
    source_counts = {}
    for row in new_data_rows:
        source = row.get('Source', 'Unknown')
        source_counts[source] = source_counts.get(source, 0) + 1

    print("\nRecords by Source:")
    for source in sorted(source_counts.keys(), key=lambda x: get_source_priority(x)):
        print(f"  {source}: {source_counts[source]}")

    # Count by Specialty (top 10)
    specialty_counts = {}
    for row in new_data_rows:
        specialty = row.get('Specialty', 'Unknown')
        specialty_counts[specialty] = specialty_counts.get(specialty, 0) + 1

    print("\nTop 10 Specialties:")
    sorted_specialties = sorted(specialty_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for specialty, count in sorted_specialties:
        print(f"  {specialty}: {count}")

    # Count by County
    county_counts = {}
    for row in new_data_rows:
        county = row.get('County', 'Unknown')
        county_counts[county] = county_counts.get(county, 0) + 1

    print("\nRecords by County:")
    for county in sorted(county_counts.keys(), key=lambda x: get_county_priority(x)):
        print(f"  {county}: {county_counts[county]}")


def main():
    """Main function to execute the sorting process."""
    base_dir = Path(__file__).resolve().parent

    # Find CSV input files (exclude output files)
    csv_files = [f for f in base_dir.glob('*.csv')
                 if 'output' not in f.name.lower() and 'spanish' not in f.name.lower()]

    if not csv_files:
        print("Error: No input CSV files found!")
        return

    if len(csv_files) > 1:
        print(f"Found {len(csv_files)} CSV files:")
        for i, f in enumerate(csv_files, 1):
            print(f"  {i}. {f.name}")
        print(f"\nProcessing the first file: {csv_files[0].name}")

    input_file = csv_files[0]
    output_file = base_dir / f'DCHF-output-{date.today()}.csv'

    print("=" * 60)
    print("DCHF Provider Data Sorting Script")
    print("=" * 60)

    try:
        process_csv_file(input_file, output_file)
        print("\n" + "=" * 60)
        print("Processing completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\nError during processing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
