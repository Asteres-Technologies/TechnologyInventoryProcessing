"""
A program to capture a specified row number from column A in an excel file.
After all rows are captured from all sheets, use those row numbers to make
a new excel file that pulls the row data from a master file.

The sheets look like this:

| Row no. | Organization | Technology | Category | TRL | Description | Relevance (1-5) | Notes | Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | Org A | Tech X | Cat 1 | 5 | Description A | 4 | Note A | Random Comment on ISAM Relation |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

Only two sheets do not follow this format:
- Non-Inventory Technologies
- Technology Gaps

We will ignore these and manually add them later.

Output format will be:
| Row no. |Technology | Producer | Description | Existing Technology | Category 1 | Category 2 | Category 3 | TRL | Functional Category 1 | Functional Category 2 | Relevance (1-5) | Notes | Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Tech X | Org A | Description A | Existing Tech A | Cat 1 | Cat 2 | Cat 3 | 5 | Func Cat 1 | Func Cat 2 | Relevance (1-5) | Notes | Link |
"""
import pandas as pd
import os

DATA_DIR = './data/'  # Directory where the data files are stored
INVENTORY_PATH = './INVENTORY.xlsx' # "Master file" with all of the original data
FILTERED_PATH = './FILTERED.xlsx' # Handmade file with relevant identifed data
STANDARDIZED_PATH = './standardized_data'  # Output file for standardized data

def capture_rows_and_metadata():
    """
    Capture the row numbers and metadata from the FILTERED_PATH file.
    Reads the specified sheets, extracts the row numbers and their associated metadata,
    and returns a dictionary where the keys are row numbers and the values are dictionaries
    containing the metadata.
    
    Returns:
    - dict: A dictionary where keys are row numbers and values are dictionaries of metadata.
    """
    filtered_data = {}
    xls = pd.ExcelFile(os.path.join(DATA_DIR, FILTERED_PATH))
    sheets_to_skip = ["Non-Inventory Technologies", "Technology Gaps"]

    correct_header_index = 3  # Use the value that produced the columns above!

    for sheet_name in xls.sheet_names:
        if sheet_name in sheets_to_skip:
            continue
        df = pd.read_excel(xls, sheet_name=sheet_name, header=correct_header_index)
        df.columns = df.columns.str.strip()

        for index, row in df.iterrows():
            row_no = row.get('Row no.')
            if pd.isna(row_no):
                continue
            filtered_data[row_no] = {
                'Relevance (1-5)': row.get('Relevance (1-5)', None),
                'Notes': row.get('Notes', None),
                'Link': row.get('Link', None)
            }
    return filtered_data


def capture_master_content(inventory_path: str, data_dir: str, sheet_name: str="Inventory") -> pd.DataFrame:
    """
    Capture the master content from the specified inventory file and sheet.
    Args:
        inventory_path (str): Path to the master inventory file.
        data_dir (str): Directory where the data files are stored.
        sheet_name (str): Name of the sheet to read from the Excel file.
    Returns:
        pd.DataFrame: DataFrame containing the captured rows and their metadata.
    """
    full_path = os.path.join(data_dir, inventory_path)
    df = pd.read_excel(full_path, sheet_name=sheet_name)
    df.columns = df.columns.str.strip()

    return df

def standardize_data(master_content: pd.DataFrame, rows_to_use: list, metadata_dict: dict) -> pd.DataFrame:
    """
    Standardize the data by enriching the rows with metadata.

    This function takes a DataFrame of rows and a dictionary of metadata,
    and returns a new DataFrame where each row is enriched with the corresponding metadata.

    Args:
        master_content (pd.DataFrame): DataFrame with master content
        rows_to_use (list): List of row indices to include
        metadata_dict (dict): {row_no: metadata_dict, ...}

    Returns:
        pd.DataFrame: Enriched DataFrame
    """
    # Map row number to DataFrame index if needed
    enriched_rows = []
    # Ensure the rows_to_use are integers then reduce the master_content to only those rows
    if not isinstance(rows_to_use, list):
        raise ValueError("rows_to_use should be a list of row numbers.")
    rows_to_use = [int(row) for row in rows_to_use if isinstance(row, (int, float)) and not pd.isna(row)]
    rows_df = master_content[master_content.index.isin(rows_to_use)]

    for idx, row in rows_df.iterrows():
        row_no = idx
        metadata = metadata_dict.get(row_no, {})
        row_data = row.to_dict()
        row_data.update(metadata)
        enriched_rows.append(row_data)
    return pd.DataFrame(enriched_rows)

def main(output_type: str = 'json'):
    """
    Main function to execute the row capture and standardization process.
    """
    filtered_data = capture_rows_and_metadata()
    standardized_df = capture_master_content(filtered_data)

    # Reorder and rename columns as per the output format
    standardized_df = standardized_df.rename(columns={
        "Technology": "Technology",
        "Organization": "Producer",
        "Description": "Description",
        "Category": "Category 1",
        "TRL": "TRL",
        "Relevance (1-5)": "Relevance (1-5)",
        "Notes": "Notes",
        "Link": "Link"
    })

    # Save as json for debugging first
    match output_type:
        case 'json':
            standardized_df.to_json(os.path.join(DATA_DIR, STANDARDIZED_PATH), orient='records', indent=4)
        case 'excel':
            standardized_df.to_excel(os.path.join(DATA_DIR, STANDARDIZED_PATH), index=False)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Process inventory data from Excel files.")
    parser.add_argument('--data-dir', type=str, default=DATA_DIR, help='Directory where the data files are stored.')
    parser.add_argument('--standardized-name', type=str, default=STANDARDIZED_PATH, help='Name of the standardized data file.')
    parser.add_argument('--inventory-name', type=str, default=INVENTORY_PATH, help='Name of the master inventory file.')
    parser.add_argument('--filtered-name', type=str, default=FILTERED_PATH, help='Name of the filtered data file.')
    parser.add_argument('--output-type', type=str, choices=['json', 'excel'], default='json', help='Output format for standardized data.')
    args = parser.parse_args()

    DATA_DIR = args.data_dir
    INVENTORY_PATH = args.inventory_name
    FILTERED_PATH = args.filtered_name
    STANDARDIZED_PATH = args.standardized_name + ('.json' if args.output_type == 'json' else '.xlsx')
    main(output_type=args.output_type)
    print(f"Data processing complete. Standardized data saved to '{STANDARDIZED_PATH}'.")

