from argparse import ArgumentParser
import pandas as pd
import os

COLUMNS = [
    "Technology Name",
    "Tech Producer",
    "Producer Type",
    "Category",
    "Level Three Category",
    "Level 3 Taxonomy",
    "TRL",
    "Relevance (1-5)",
    "Notes"
]
STANDARDIZED_PATH = "./data/standardized_data.json"
SLIM_PATH = "./data/slim_data"

def get_dataframe_from_json(file_path: str) -> pd.DataFrame:
    """
    Load a DataFrame from a JSON file.
    Args:
        file_path (str): Path to the JSON file.
    Returns:
        pd.DataFrame: DataFrame loaded from the JSON file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    return pd.read_json(file_path, orient='records')

def create_slim_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a slim DataFrame with only the specified columns.
    Args:
        df (pd.DataFrame): The DataFrame to process.
    Returns:
        pd.DataFrame: A slimmed-down version of the original DataFrame.
    """
    slim_df = df.reindex(columns=COLUMNS).copy()

    # Fill NaN values with empty strings
    slim_df.fillna("", inplace=True)
    return slim_df

def is_academia(producer: str) -> bool:
    """
    Check if the producer is an academic institution.
    Args:
        producer (str): The name of the producer.
    Returns:
        bool: True if the producer is an academic institution, False otherwise.
    """
    academia_keywords = ["University", "College", "Institute", "Academy", "(Academia)"]
    return any(keyword in producer for keyword in academia_keywords)

def is_government(producer: str) -> bool:
    """
    Check if the producer is a government entity.
    Args:
        producer (str): The name of the producer.
    Returns:
        bool: True if the producer is a government entity, False otherwise.
    """
    government_keywords = [
        "AFRL",
        "NASA",
        "National Aeronautics and Space Administration",
        "NASA Ames",
        "Ames Research Center",
        "NASA Langley",
        "Langley Research Center",
        "Goddard",
        "Goddard Space Flight Center",
        "NASA Goddard",
        "Johnson Space Center",
        "Kennedy Space Center",
        "Marshall",
        "Marshall Space Flight Center",
        "Jet Propulsion Laboratory",
        "JPL",
        "Wallops Flight Facility",
        "German Space Agency",
        "DLR",
        "European Space Agency",
        "ESA",
        "(Government)"
    ]
    return any(keyword in producer for keyword in government_keywords)

def is_industry(producer: str) -> bool:
    """
    Check if the producer is an industry entity.
    Args:
        producer (str): The name of the producer.
    Returns:
        bool: True if the producer is an industry entity, False otherwise.
    """
    industry_keywords = ["Company", "Corporation", "LLC", "Inc.", "(Industry)"]
    return any(keyword in producer for keyword in industry_keywords)

def fill_producer_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill the 'Producer Type' column based on the 'Tech Producer' column.
    Args:
        df (pd.DataFrame): The DataFrame to process.
    Returns:
        pd.DataFrame: The DataFrame with 'Producer Type' filled.
    """
    df['Producer Type'] = df['Tech Producer'].apply(lambda x: 'Academia' if is_academia(x) else
                                                     'Government' if is_government(x) else
                                                     'Industry' if is_industry(x) else
                                                     'Unknown')
    return df

def fill_level_3_taxonomy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill the 'Level 3 Taxonomy' column based on the 'Level Three Category' column.
    Args:
        df (pd.DataFrame): The DataFrame to process.    
    Returns:
        pd.DataFrame: The DataFrame with 'Level 3 Taxonomy' filled.
    """
    df['Level 3 Taxonomy'] = df['Level Three Category'].apply(lambda x: x if isinstance(x, str) and x else "Unknown")
    # Remove the 'Level Three Category' column as it's no longer needed
    df.drop(columns=['Level Three Category'], inplace=True, errors='ignore')
    return df

def fill_tlr_with_zero(df: pd.DataFrame) -> pd.DataFrame:
    """    Fill the 'TRL' column with 0 where it is NaN or empty.
    Args:
        df (pd.DataFrame): The DataFrame to process.
    Returns:
        pd.DataFrame: The DataFrame with 'TRL' filled.
    """
    df['TRL'] = df['TRL'].fillna(0)
    df['TRL'] = df['TRL'].replace('', 0)
    df['TRL'] = pd.to_numeric(df['TRL'], errors='coerce').fillna(0).astype(int)
    df['TRL'] = df['TRL'].astype(int)
    df['TRL'] = df['TRL'].clip(lower=0, upper=9)
    return df

def fill_relevance_with_zero(df: pd.DataFrame) -> pd.DataFrame:
    """Fill the 'Relevance (1-5)' column with 0 where it is NaN or empty.
    Args:
        df (pd.DataFrame): The DataFrame to process.
    Returns:
        pd.DataFrame: The DataFrame with 'Relevance (1-5)' filled.
    """
    df['Relevance (1-5)'] = df['Relevance (1-5)'].fillna(0)
    df['Relevance (1-5)'] = df['Relevance (1-5)'].replace('', 0)
    df['Relevance (1-5)'] = pd.to_numeric(df['Relevance (1-5)'], errors='coerce').fillna(0).astype(int)
    df['Relevance (1-5)'] = df['Relevance (1-5)'].clip(lower=0, upper=5)
    df['Relevance (1-5)'] = df['Relevance (1-5)'].astype(int)
    return df

def main():
    """Main function to execute the script.
    """
    parser = ArgumentParser(description="Process and standardize technology data.")
    parser.add_argument('--input', type=str, default=STANDARDIZED_PATH, help='Path to the input JSON file containing technology data.')
    parser.add_argument('--output', type=str, default=SLIM_PATH, help='Path to save the standardized data.')
    parser.add_argument('--save-type', type=str, choices=['json', 'excel'], default='json',
                        help='Format to save the standardized data (json or excel).')
    args = parser.parse_args()
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"The input file {args.input} does not exist.")
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Load the DataFrame from the JSON file
    df = get_dataframe_from_json(args.input)
    slim_df = create_slim_dataframe(df)
    standardized_df = fill_producer_type(slim_df)
    standardized_df = fill_level_3_taxonomy(standardized_df)
    standardized_df = fill_tlr_with_zero(standardized_df)
    standardized_df = fill_relevance_with_zero(standardized_df)
    
    # Save the standardized DataFrame
    if args.save_type == 'excel':
        path = args.output + ".xlsx"
        standardized_df.to_excel(path, index=False)
    else:
        path = args.output + ".json"
        standardized_df.to_json(path, orient='records', indent=4)
    print(f"Standardized data saved to {path}")

if __name__ == "__main__":
    main()