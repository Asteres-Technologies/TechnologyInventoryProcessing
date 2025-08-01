"""
This module checks to see if all of the standardized rows are in the filtered data.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from inventory_processor import capture_rows_and_metadata, capture_master_content, standardize_data, capture_filtered_data
import pandas as pd


def test_all_standardized_in_filtered():
    """
    Test to ensure that all standardized rows are present in the filtered data.
    Uses DATA_DIR and INVENTORY_PATH directly from the inventory_processor module.
    """
    # Load filtered data as a dict and associated metadata
    original_filtered_data = capture_filtered_data()  # dict[int, dict]
    metadata, rows_to_use = capture_rows_and_metadata()
    # Load the master content
    master_content = capture_master_content()
    # Standardize the data
    standardized_df = standardize_data(master_content, metadata, rows_to_use)

    # All index-values in standardized_df are assumed to correspond to row numbers ("Row no.")
    ofd_keys = list(original_filtered_data.keys())
    ofd_keys.sort()
    for index, row in standardized_df.iterrows():
        master_row_reference = ofd_keys[index]
        ofd_row = original_filtered_data.get(master_row_reference, None)
        std_row = row.to_dict()
        assert ofd_row is not None, f"Row {master_row_reference} not found in original filtered data."
        
        ofd_relevance = ofd_row.get('Relevance (1-5)', None)
        std_relevance = std_row.get('Relevance (1-5)', None)
        # Avoid nan comparison issues
        if pd.isna(ofd_relevance):
            ofd_relevance = None
        if pd.isna(std_relevance):
            std_relevance = None
        assert ofd_relevance == std_relevance, f"Relevance mismatch for row {master_row_reference}: {ofd_relevance} != {std_relevance}"

        ofd_notes = ofd_row.get('Notes', None)
        std_notes = std_row.get('Notes', None)
        # Avoid nan comparison issues
        if pd.isna(ofd_notes):
            ofd_notes = None
        if pd.isna(std_notes):
            std_notes = None
        assert ofd_notes == std_notes, f"Notes mismatch for row {master_row_reference}: {ofd_notes} != {std_notes}"

        ofd_link = ofd_row.get('Link', None)
        std_link = std_row.get('Link', None)
        # Avoid nan comparison issues
        if pd.isna(ofd_link):
            ofd_link = None
        if pd.isna(std_link):
            std_link = None
        assert ofd_link == std_link, f"Link mismatch for row {master_row_reference}: {ofd_link} != {std_link}"