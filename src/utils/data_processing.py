import pandas as pd
import os

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV file into a Pandas DataFrame.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Loaded DataFrame or an empty DataFrame if the file does not exist.
    """
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # Return an empty DataFrame with predefined columns
        if "participants" in file_path:
            return pd.DataFrame(columns=["Name", "SV-Nummer", "Berufswunsch", "Eintrittsdatum", "Austrittsdatum"])
        elif "tests" in file_path:
            return pd.DataFrame(columns=[
                "Teilnehmer", "Datum", "Textaufgaben", "Raumvorstellung",
                "Gleichungen", "Brüche", "Grundrechenarten", "Zahlenraum", "Gesamtpunkte"
            ])
        else:
            return pd.DataFrame()

def save_data(data: pd.DataFrame, file_path: str):
    """
    Saves a Pandas DataFrame to a CSV file.
    
    Args:
        data (pd.DataFrame): DataFrame to save.
        file_path (str): Path to the CSV file.
    """
    data.to_csv(file_path, index=False)

def calculate_percentage(data: pd.DataFrame, categories: list) -> pd.DataFrame:
    """
    Calculates percentage scores for each category and the total score.
    
    Args:
        data (pd.DataFrame): DataFrame containing raw scores.
        categories (list): List of category column names to calculate percentages for.
    
    Returns:
        pd.DataFrame: DataFrame with percentage scores added.
    """
    for category in categories:
        data[f"{category} (%)"] = data[category] / 100 * 100  # Normalize to percentage
    data["Gesamt (%)"] = data["Gesamtpunkte"] / 600 * 100  # Assuming total max points is 600
    return data
