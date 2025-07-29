# Technology Inventory Processor

## Overview

This tool helps you **extract specific rows and metadata from multiple Excel sheets** and **merge them into a standardized output file**. It’s ideal for making sense of complex technology inventories, project tracking data, or any scenario where you curate and consolidate data across many Excel sources.

## What It Does

1. **Extracts row numbers and selected metadata**  
   Scans all relevant sheets in your filtered Excel workbook (`FILTERED.xlsx`), extracting the row numbers plus columns like “Relevance (1-5)”, “Notes”, and “Link”.

2. **Ignores nonstandard sheets**  
   Skips the `"Non-Inventory Technologies"` and `"Technology Gaps"` sheets; they must be handled manually as their structure differs.

3. **Pulls full row data from a master inventory**  
   Uses the collected row numbers to select corresponding rows from a master Excel inventory (`INVENTORY.xlsx`).

4. **Merges and standardizes the results**  
   Appends the metadata and reorganizes/renames columns for a clean, consistent output.  

5. **Outputs a JSON file**  
   Writes the standardized data to a JSON file, suitable for further analysis, publishing, or importing into other tools.

## Expected Input File Structure

- **`FILTERED.xlsx`** (User-curated workbook):
    - Contains multiple sheets, each with this header structure:
      ```
      | Row no. | Organization | Technology | Category | TRL | Description | Relevance (1-5) | Notes | Link |
      ```
    - Sheets named `"Non-Inventory Technologies"` and `"Technology Gaps"` are ignored.

- **`INVENTORY.xlsx`** (Master file):
    - Contains the definitive set of technologies/projects, must have a sheet named `"Inventory"` using the same or superset of columns.

## Example Output Fields

```
| Row no. | Technology | Producer | Description | Existing Technology | Category 1 | Category 2 | Category 3 | TRL | Functional Category 1 | Functional Category 2 | Relevance (1-5) | Notes | Link |
```

## Usage

1. **Place your data files** in a directory (default: `./data/`):  
   - `INVENTORY.xlsx` (master inventory)
   - `FILTERED.xlsx` (filtered identifiers)

2. **Run the script:**
   ```
   python your_script.py
   ```

3. **Optional:** You can override file and directory choices from the command line:
   ```
   python your_script.py \
       --data-dir "./my-data" \
       --inventory-name "master_inventory.xlsx" \
       --filtered-name "my_filtered.xlsx" \
       --standardized-name "output.json"
   ```

4. **Result:**  
   Your standardized data will be saved as JSON (default: `./data/standardized_data.json`).

## Command-line Options

- `--data-dir` &nbsp;: Directory containing your Excel files (default: `./data/`)
- `--inventory-name` &nbsp;: Master inventory filename (default: `INVENTORY.xlsx`)
- `--filtered-name` &nbsp;: Filtered selector filename (default: `FILTERED.xlsx`)
- `--standardized-name` &nbsp;: Output filename for standardized data (default: `standardized_data.json`)

## Notes

- You may need to adjust the `correct_header_index` in the code if your Excel header changes.
- The output format is easily customizable; pandas also supports writing CSV, XLSX, etc.
- Extra columns in your Excel files are tolerated; only the specified columns are extracted/renamed for output.
- The script currently ignores nonstandard sheets (by name); you can manually add those later if necessary.

## License

This project is **GPL v3 licensed**.  
See `LICENSE` for details. All modifications and redistributions must remain open source.