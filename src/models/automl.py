from pycaret.regression import setup, compare_models, save_model, load_model
import pandas as pd

def train_automl_model(tests: pd.DataFrame, save_path: str = "models/prediction_model.pkl"):
    """
    Trains an AutoML model using PyCaret and saves the best model.
    
    Args:
        tests (pd.DataFrame): DataFrame containing test data.
        save_path (str): Path to save the trained model.
    """
    # Prepare training data
    training_data = tests.copy()
    training_data["Datum"] = pd.to_datetime(training_data["Datum"]).astype(int) / 10**9  # Convert dates to timestamps
    features = ["Datum", "Textaufgaben", "Raumvorstellung", "Gleichungen", "Brüche", "Grundrechenarten", "Zahlenraum"]
    target = "Gesamtpunkte"

    # PyCaret setup
    setup(data=training_data, target=target, numeric_features=features, silent=True, session_id=123)

    # Train models and select the best
    best_model = compare_models()

    # Save the model
    save_model(best_model, save_path)

def load_trained_model(model_path: str):
    """
    Loads a trained AutoML model.
    
    Args:
        model_path (str): Path to the saved model file.
    
    Returns:
        object: Loaded model.
    """
    return load_model(model_path)
