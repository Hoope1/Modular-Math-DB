import pandas as pd
import plotly.graph_objects as go
from pycaret.regression import load_model, predict_model

def load_prediction_model(model_path: str):
    """
    Loads the saved AutoML prediction model.
    
    Args:
        model_path (str): Path to the saved model file.
    
    Returns:
        object: Loaded AutoML model.
    """
    return load_model(model_path)

def generate_predictions(participant: str, tests: pd.DataFrame, model):
    """
    Generates predictions for the next 60 days for a participant.
    
    Args:
        participant (str): Name of the participant.
        tests (pd.DataFrame): DataFrame of tests.
        model: Loaded AutoML model.
    
    Returns:
        pd.DataFrame: DataFrame with predicted scores.
    """
    participant_tests = tests[tests["Teilnehmer"] == participant]
    if participant_tests.empty:
        return pd.DataFrame()

    # Prepare data for prediction
    last_test_date = pd.to_datetime(participant_tests["Datum"]).max()
    future_dates = pd.date_range(last_test_date, periods=60, freq="D")
    prediction_data = pd.DataFrame({"Datum": future_dates})
    
    # Generate predictions
    prediction_data["Predicted (%)"] = predict_model(model, data=prediction_data)["Label"]
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
    # Load model
    model = load_prediction_model("models/prediction_model.pkl")
    predictions = generate_predictions(participant, tests, model)

    # Historical data
    participant_tests = tests[tests["Teilnehmer"] == participant]
    historical_dates = pd.to_datetime(participant_tests["Datum"])
    historical_scores = participant_tests["Gesamt (%)"]

    # Create plot
    fig = go.Figure()

    # Historical scores
    fig.add_trace(go.Scatter(
        x=historical_dates,
        y=historical_scores,
        mode="lines+markers",
        name="Historische Werte"
    ))

    # Predictions
    if not predictions.empty:
        fig.add_trace(go.Scatter(
            x=predictions["Datum"],
            y=predictions["Predicted (%)"],
            mode="lines",
            name="Vorhersage"
        ))

    # Layout
    fig.update_layout(
        title=f"Prognose für {participant}",
        xaxis_title="Datum",
        yaxis_title="Prozent (%)",
        yaxis=dict(range=[0, 100]),
        xaxis=dict(title="Tage (-30 bis +30)")
    )
    return fig
