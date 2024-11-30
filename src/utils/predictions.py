import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import numpy as np

def train_model(tests: pd.DataFrame, save_path: str = "models/prediction_model.pkl"):
    """
    Trains a Random Forest Regressor and saves the trained model.
    
    Args:
        tests (pd.DataFrame): DataFrame containing test data.
        save_path (str): Path to save the trained model.
    """
    tests["Datum"] = pd.to_datetime(tests["Datum"]).astype(int) / 10**9
    X = tests[["Datum", "Textaufgaben", "Raumvorstellung", "Gleichungen", "Brüche", "Grundrechenarten", "Zahlenraum"]]
    y = tests["Gesamtpunkte"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, save_path)

def load_model(model_path: str):
    """
    Loads the trained model.
    
    Args:
        model_path (str): Path to the saved model.
    
    Returns:
        object: The trained model.
    """
    return joblib.load(model_path)

def generate_predictions(participant: str, tests: pd.DataFrame, model):
    """
    Generates predictions for the next 60 days for a participant.
    
    Args:
        participant (str): Name of the participant.
        tests (pd.DataFrame): DataFrame of tests.
        model: The trained model.
    
    Returns:
        pd.DataFrame: DataFrame with predicted scores.
    """
    participant_tests = tests[tests["Teilnehmer"] == participant]
    if participant_tests.empty:
        return pd.DataFrame()

    last_test_date = pd.to_datetime(participant_tests["Datum"]).max()
    future_dates = pd.date_range(last_test_date, periods=60, freq="D")
    future_timestamps = future_dates.astype(int) / 10**9

    prediction_data = pd.DataFrame({
        "Datum": future_timestamps,
        "Textaufgaben": np.zeros(60),
        "Raumvorstellung": np.zeros(60),
        "Gleichungen": np.zeros(60),
        "Brüche": np.zeros(60),
        "Grundrechenarten": np.zeros(60),
        "Zahlenraum": np.zeros(60),
    })

    prediction_data["Predicted (%)"] = model.predict(prediction_data)
    prediction_data["Datum"] = future_dates
    return prediction_data

def generate_prediction_chart(participant: str, tests: pd.DataFrame):
    """
    Generates a line chart with predictions and historical test scores.
    
    Args:
        participant (str): Name of the participant.
        tests (pd.DataFrame): DataFrame of tests.
    
    Returns:
        go.Figure: Plotly figure with the prediction chart.
    """
    model = load_model("models/prediction_model.pkl")
    predictions = generate_predictions(participant, tests, model)

    participant_tests = tests[tests["Teilnehmer"] == participant]
    historical_dates = pd.to_datetime(participant_tests["Datum"])
    historical_scores = participant_tests["Gesamt (%)"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=historical_dates,
        y=historical_scores,
        mode="lines+markers",
        name="Historische Werte"
    ))

    if not predictions.empty:
        fig.add_trace(go.Scatter(
            x=predictions["Datum"],
            y=predictions["Predicted (%)"],
            mode="lines",
            name="Vorhersage"
        ))

    fig.update_layout(
        title=f"Prognose für {participant}",
        xaxis_title="Datum",
        yaxis_title="Prozent (%)",
        yaxis=dict(range=[0, 100]),
        xaxis=dict(title="Tage (-30 bis +30)")
    )
    return fig
