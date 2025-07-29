# Technology Inventory Processor

## Overview

This tool streamlines the process of **extracting specific rows from multiple sheets across Excel workbooks**, collating their metadata, and generating a new, clean standardized dataset. It’s especially helpful for technology inventories, project tracking, or any scenario where you need to curate and reassemble data from complex Excel sources.

## What It Does

1. **Extracts row numbers and key metadata** (such as “Relevance”, “Notes”, and “Link”) from all relevant sheets in a custom _FILTERED.xlsx_ file.
2. **Ignores special non-standard sheets** (`"Non-Inventory Technologies"` and `"Technology Gaps"`), which can be added manually later.
3. **Uses the captured row numbers** to pull full row data from a master source (_INVENTORY.xlsx_).
4. **Creates a standardized output file** that merges the extracted row data and metadata, suitable for further analysis or reporting.

## Expected Input Structure

- **FILTERED.xlsx**: 
  - Multiple sheets, each following this format:
    ```
    | Row no. | Organization | Technology | Category | TRL | Description | Relevance (1-5) | Notes | Link |
    ```
  - Two sheets ("Non-Inventory Technologies" and "Technology Gaps") are ignored.

- **INVENTORY.xlsx**:
  - Master list with full project/technology data, must contain an “Inventory” sheet.

## Output

- **STANDARDIZED.json** (or other formats as needed):
  - Contains standardized, merged row data using this structure:
    ```
    | Row no. | Technology | Producer | Description | Existing Technology | Category 1 | Category 2 | Category 3 | TRL | Functional Category 1 | Functional Category 2 | Relevance (1-5) | Notes | Link |
    ```

## How To Use

1. Place your `INVENTORY.xlsx` and `FILTERED.xlsx` in the script directory.
2. Adjust paths as needed in the script:
    ```python
    INVENTORY_PATH = './INVENTORY.xlsx'
    FILTERED_PATH = './FILTERED.xlsx'
    OUTPUT_PATH = './STANDARDIZED.'  # Filename suffix omitted for easy path resuse.
    ```
3. Run the script:
    ```
    python your_script_name.py
    ```
4. Review the output `STANDARDIZED.json` file for your clean, formatted dataset.

## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.  
See the LICENSE file for details.

## Notes

- The script skips non-standard sheets and expects consistent headers (adjust `correct_header_index` if your FILES change).
- Output format can be easily switched from JSON to Excel or CSV (just swap the relevant pandas export call).
- Feel free to extend or adapt the code for additional fields, more complex mapping, or different output needs.
