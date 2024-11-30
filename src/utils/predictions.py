import pandas as pd
import h2o
from h2o.automl import H2OAutoML
import plotly.graph_objects as go

# Initialisiere H2O-Server
h2o.init()

def train_h2o_automl(data: pd.DataFrame, target_column: str, model_path: str):
    """
    Trainiert ein H2O AutoML-Modell und speichert es.

    Args:
        data (pd.DataFrame): Der Datensatz, der das Training unterstützt.
        target_column (str): Der Zielwert (Target).
        model_path (str): Der Speicherpfad für das Modell.
    """
    # Daten vorbereiten
    h2o_data = h2o.H2OFrame(data)
    x_columns = [col for col in data.columns if col != target_column]
    y_column = target_column

    # H2O AutoML-Training
    aml = H2OAutoML(max_models=10, seed=42)
    aml.train(x=x_columns, y=y_column, training_frame=h2o_data)

    # Bestes Modell speichern
    h2o.save_model(aml.leader, path=model_path)

def load_h2o_model(model_path: str):
    """
    Lädt ein gespeichertes H2O-Modell.

    Args:
        model_path (str): Der Pfad zum gespeicherten Modell.

    Returns:
        H2OEstimator: Das geladene Modell.
    """
    return h2o.load_model(model_path)

def generate_h2o_predictions(data: pd.DataFrame, model_path: str):
    """
    Generiert Vorhersagen basierend auf einem H2O AutoML-Modell.

    Args:
        data (pd.DataFrame): Die Eingabedaten für die Vorhersagen.
        model_path (str): Der Pfad zum gespeicherten Modell.

    Returns:
        pd.DataFrame: Ein DataFrame mit den Vorhersagen.
    """
    h2o_data = h2o.H2OFrame(data)
    model = load_h2o_model(model_path)
    predictions = model.predict(h2o_data).as_data_frame()
    return predictions

def generate_prediction_chart(data: pd.DataFrame, predictions: pd.DataFrame, participant: str):
    """
    Generiert ein Vorhersagediagramm für einen Teilnehmer.

    Args:
        data (pd.DataFrame): Historische Daten des Teilnehmers.
        predictions (pd.DataFrame): Vorhergesagte Werte.
        participant (str): Der Name des Teilnehmers.

    Returns:
        go.Figure: Ein Plotly-Diagramm mit den historischen und vorhergesagten Werten.
    """
    historical_data = pd.to_datetime(data["Datum"])
    historical_scores = data["Gesamt (%)"]

    future_dates = pd.date_range(start=data["Datum"].max(), periods=len(predictions), freq="D")
    predicted_scores = predictions.iloc[:, 0]

    fig = go.Figure()

    # Historische Daten
    fig.add_trace(go.Scatter(
        x=historical_data,
        y=historical_scores,
        mode="lines+markers",
        name="Historisch"
    ))

    # Vorhersagen
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=predicted_scores,
        mode="lines",
        name="Vorhersagen"
    ))

    fig.update_layout(
        title=f"Vorhersagediagramm für {participant}",
        xaxis_title="Datum",
        yaxis_title="Prozent (%)",
        yaxis=dict(range=[0, 100])
    )

    return fig
