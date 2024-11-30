from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib  # Zum Speichern und Laden von Modellen
import pandas as pd

def train_model(tests: pd.DataFrame, save_path: str = "models/prediction_model.pkl"):
    """
    Trains a machine learning model and saves it.
    
    Args:
        tests (pd.DataFrame): DataFrame containing test data.
        save_path (str): Path to save the trained model.
    """
    # Prepare training data
    training_data = tests.copy()
    training_data["Datum"] = pd.to_datetime(training_data["Datum"]).astype(int) / 10**9  # Timestamps
    X = training_data[["Datum", "Textaufgaben", "Raumvorstellung", "Gleichungen", "Brüche", "Grundrechenarten", "Zahlenraum"]]
    y = training_data["Gesamtpunkte"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, save_path)

def load_trained_model(model_path: str):
    """
    Loads a trained machine learning model.
    
    Args:
        model_path (str): Path to the saved model file.
    
    Returns:
        object: Loaded model.
    """
    return joblib.load(model_path)
