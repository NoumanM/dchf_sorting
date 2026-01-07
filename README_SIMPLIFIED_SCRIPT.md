# DCHF Provider Data Sorting Script - Documentation

## Overview
This simplified script replaces the complex nested dictionary sorting approach with a straightforward, reliable sorting mechanism using Python's built-in `sorted()` function.

## Script: `simplified_sorting_script.py`

### What It Does
Reads provider data from a CSV file and sorts it according to the specified priority order:

1. **Source (Column AG)** - Custom order:
   - PCP
   - Specialist
   - BehavioralHealthSpecialist
   - Dental
   - Vision
   - Facility
   - Pharmacy
   - (Any other values sort last)

2. **Specialty (Column G)** - Alphabetical A-Z

3. **County (Column N)** - Custom order:
   - District of Columbia (includes all Ward # entries)
   - Montgomery
   - Prince Georges
   - Arlington
   - Fairfax
   - Fairfax City
   - Manassas City
   - Prince William
   - (Any other values sort last)

4. **Group Name (Column H)** - Alphabetical A-Z

5. **Last Name (Column A)** - Alphabetical A-Z (final tiebreaker)

### Key Improvements Over Original Script

1. **Simplicity**: Uses a single sort operation instead of complex nested dictionaries
2. **Reliability**: Less prone to errors and easier to debug
3. **Performance**: More efficient memory usage and faster execution
4. **Maintainability**: Clean, well-documented code that's easy to modify
5. **Statistics**: Provides summary statistics after processing

### How to Use

1. **Place your input CSV file** in the same directory as the script
   - The script will automatically find CSV files that don't contain "output" or "spanish" in their names

2. **Run the script**:
   ```bash
   python simplified_sorting_script.py
   ```

3. **Output file** will be created as: `DCHF-output-YYYY-MM-DD.csv`

### Features

- **Automatic encoding detection**: Handles different file encodings
- **Address capitalization**: Automatically capitalizes directional abbreviations (Ne→NE, Se→SE, etc.)
- **Summary statistics**: Shows counts by Source, Specialty, and County
- **Error handling**: Gracefully handles missing or malformed data

### Example Output

```
============================================================
DCHF Provider Data Sorting Script
============================================================
Reading input file: DCHFProviderPrintDir_12232025.csv
Detected encoding: utf-8-sig
Read 10051 rows
Sorting data...
Writing output file: DCHF-output-2026-01-07.csv
Successfully wrote 10051 rows to DCHF-output-2026-01-07.csv

--- Summary Statistics ---

Records by Source:
  PCP: 1377
  Specialist: 5253
  BehavioralHealthSpecialist: 1062
  Dental: 875
  Vision: 707
  Facility: 386
  Pharmacy: 391

Top 10 Specialties:
  Ophthalmology - Ophthalmology: 575
  Family Medicine: 540
  Pediatrics: 424
  ...

Records by County:
  Ward 5: 1764
  Ward 3: 651
  Montgomery: 1678
  ...

============================================================
Processing completed successfully!
============================================================
```

### Adding Spanish Translations

After running the main sorting script, use the existing `assign_spanish_speciality.py` script:

```bash
python assign_spanish_speciality.py
```

This will create `Spanish-DCHF-output-YYYY-MM-DD.csv` with Spanish specialty translations.

### Customization

#### To add new Source types:
Edit the `get_source_priority()` function:
```python
source_order = {
    'PCP': 1,
    'Specialist': 2,
    'NewSourceType': 3,  # Add here
    ...
}
```

#### To add new Counties:
Edit the `get_county_priority()` function:
```python
county_order = {
    'District of Columbia': 1,
    'NewCounty': 2,  # Add here
    ...
}
```

### File Structure

```
dchf_sorting/
├── simplified_sorting_script.py    # Main sorting script (NEW)
├── assign_spanish_speciality.py    # Spanish translation script
├── spanish_utils.py                # Spanish translation mappings
├── DCHFProviderPrintDir_*.csv      # Input file
├── DCHF-output-*.csv              # Output file (sorted)
└── Spanish-DCHF-output-*.csv      # Output with Spanish (optional)
```

### Troubleshooting

**Problem**: Script doesn't find input file
- **Solution**: Make sure your CSV file doesn't have "output" or "spanish" in the filename

**Problem**: Encoding errors
- **Solution**: The script auto-detects encoding, but you can manually specify it in the code

**Problem**: Missing columns
- **Solution**: Ensure your CSV has all required columns (LastName, Specialty, County, GroupName, Source)

### Technical Notes

- **Python version**: Works with Python 3.6+
- **Dependencies**: 
  - `chardet` (for encoding detection) - install with: `pip install chardet`
  - `csv`, `datetime`, `pathlib`, `re` (built-in modules)

### Comparison with Original Script

| Aspect | Original Script | Simplified Script |
|--------|----------------|-------------------|
| Lines of code | ~400+ | ~200 |
| Complexity | Very high (nested dicts) | Low (single sort) |
| Memory usage | High | Low |
| Execution time | Slower | Faster |
| Maintainability | Difficult | Easy |
| Debugging | Very difficult | Simple |
| Custom sorting | Complex to modify | Easy to modify |

### Support

For questions or modifications, refer to the inline code comments or modify the sorting functions as needed.

