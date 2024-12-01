import h2o
from h2o.automl import H2OAutoML
import pandas as pd
import plotly.graph_objects as go
import os

h2o.init()

def train_h2o_automl(data: pd.DataFrame, target_column: str, model_path: str):
    """
    Trainiert ein H2O AutoML-Modell auf den bereitgestellten Daten.

    Args:
        data (pd.DataFrame): Der Trainingsdatensatz.
        target_column (str): Der Name der Zielspalte.
        model_path (str): Der Pfad, um das Modell zu speichern.
    """
    # Konvertiere pandas DataFrame zu H2OFrame
    h2o_data = h2o.H2OFrame(data)

    # Aufteilen in Trainings- und Validierungsdaten
    train, valid = h2o_data.split_frame(ratios=[0.8], seed=1234)

    # Ziel- und Eingabefelder definieren
    x = [col for col in data.columns if col != target_column]
    y = target_column

    # AutoML-Modell trainieren
    aml = H2OAutoML(max_models=10, seed=1, stopping_metric="RMSE")
    aml.train(x=x, y=y, training_frame=train, validation_frame=valid)

    # Modell speichern
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    h2o.save_model(model=aml.leader, path=model_path, force=True)


def generate_h2o_predictions(participant_data: pd.DataFrame, model_path: str) -> pd.DataFrame:
    """
    Generiert Vorhersagen für einen Teilnehmer basierend auf dem trainierten H2O-Modell.

    Args:
        participant_data (pd.DataFrame): Die Daten des Teilnehmers.
        model_path (str): Der Pfad zum gespeicherten H2O-Modell.

    Returns:
        pd.DataFrame: Die Vorhersagen für den Teilnehmer.
    """
    # Lade das gespeicherte Modell
    model = h2o.load_model(model_path)

    # Konvertiere Daten zu H2OFrame
    h2o_data = h2o.H2OFrame(participant_data)

    # Vorhersagen generieren
    predictions = model.predict(h2o_data)

    # Zurück zu pandas DataFrame
    return predictions.as_data_frame()


def generate_prediction_chart(participant_data: pd.DataFrame, predictions: pd.DataFrame, participant: str):
    """
    Erstellt ein Vorhersagediagramm für einen Teilnehmer.

    Args:
        participant_data (pd.DataFrame): Historische Daten des Teilnehmers.
        predictions (pd.DataFrame): Vorhersagedaten.
        participant (str): Der Name des Teilnehmers.

    Returns:
        go.Figure: Ein Plotly-Diagramm der Vorhersagen.
    """
    # Zeitachsen-Daten
    days = list(range(1, len(predictions) + 1))

    # Plotly-Diagramm erstellen
    fig = go.Figure()

    # Historische Daten
    fig.add_trace(
        go.Scatter(
            x=participant_data.index,
            y=participant_data["Zielwert (%)"],
            mode="lines+markers",
            name="Historische Daten",
        )
    )

    # Vorhersagen
    fig.add_trace(
        go.Scatter(
            x=days,
            y=predictions.iloc[:, 0],
            mode="lines",
            name="Vorhersagen",
            line=dict(dash="dot"),
        )
    )

    # Diagramm-Layout
    fig.update_layout(
        title=f"Vorhersagen für {participant}",
        xaxis_title="Tage",
        yaxis_title="Prozent",
        template="plotly_white",
    )

    return fig
