import pandas as pd
import os

def load_data(file_path: str) -> pd.DataFrame:
    """
    Lädt die Teilnehmerdaten aus einer CSV-Datei.

    Args:
        file_path (str): Der Pfad zur Datei.

    Returns:
        pd.DataFrame: Der geladene Datensatz.
    """
    if os.path.exists(file_path):
        data = pd.read_csv(file_path, parse_dates=["Eintrittsdatum", "Austrittsdatum"])
        return data
    else:
        # Leere Datenstruktur, falls Datei nicht existiert
        return pd.DataFrame(
            columns=["Name", "SV-Nummer", "Eintrittsdatum", "Austrittsdatum", "Zielwert (%)"]
        )

def save_data(data: pd.DataFrame, file_path: str):
    """
    Speichert die Teilnehmerdaten in eine CSV-Datei.

    Args:
        data (pd.DataFrame): Der zu speichernde Datensatz.
        file_path (str): Der Pfad zur Datei.
    """
    data.to_csv(file_path, index=False)
