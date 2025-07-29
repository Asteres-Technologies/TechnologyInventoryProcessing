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

INVENTORY_PATH = './INVENTORY.xlsx' # "Master file" with all of the original data
FILTERED_PATH = './FILTERED.xlsx' # Handmade file with relevant identifed data
OUTPUT_PATH = './STANDARDIZED.' # Output file with standardized data

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
    xls = pd.ExcelFile(FILTERED_PATH)
    sheets_to_skip = ["Non-Inventory Technologies", "Technology Gaps"]

    correct_header_index = 3  # Use the value that produced the columns above!
    desired_columns = ['Row no.', 'Relevance (1-5)', 'Notes', 'Link']

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


def capture_master_content(filtered_data):
    """
    Capture the content of the specified rows from the INVENTORY_PATH file.
    Uses the row numbers captured from the FILTERED_PATH file.
    Appends the metadata to the master content as extra columns.

    Args:
    - filtered_data (dict): A dictionary containing row numbers and their metadata.
    Returns:
    - pd.DataFrame: A DataFrame containing the standardized data.
    """
    master_data = pd.read_excel(INVENTORY_PATH, sheet_name=None)
    standardized_data = []
    inventory_sheet_name = "Inventory"

    if inventory_sheet_name in master_data:
        df = master_data[inventory_sheet_name]
        df.columns = df.columns.str.strip()

        for row_no, metadata in filtered_data.items():
            if row_no in df.index:
                row_data = df.loc[row_no].to_dict()
                row_data.update(metadata)  # Add metadata to the row data
                standardized_data.append(row_data)

    return pd.DataFrame(standardized_data)

def main():
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
    standardized_df.to_json(OUTPUT_PATH + 'json', orient='records', indent=4)

if __name__ == "__main__":
    main()
