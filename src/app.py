import streamlit as st
import pandas as pd
from src.utils.data_processing import load_data, save_data
from src.utils.predictions import (
    train_h2o_automl,
    generate_h2o_predictions,
    generate_prediction_chart,
)
from src.utils.report_generation import generate_report
import os

# Konfigurationsoptionen
MODEL_PATH = "models/h2o_automl_model"
DATA_PATH = "data/participants_data.csv"

# Daten laden
data = load_data(DATA_PATH)

# Streamlit UI
st.title("Mathematik-Kurs Teilnehmerverwaltung")

# Teilnehmer-Tabellendarstellung
st.header("Teilnehmerübersicht")
st.dataframe(data)

# Teilnehmer hinzufügen
st.subheader("Teilnehmer hinzufügen")
with st.form("add_participant"):
    name = st.text_input("Name")
    sv_number = st.text_input("SV-Nummer")
    entry_date = st.date_input("Eintrittsdatum")
    exit_date = st.date_input("Austrittsdatum")
    target_score = st.number_input("Zielwert (%)", min_value=0, max_value=100, value=50)
    submit = st.form_submit_button("Hinzufügen")

    if submit:
        new_participant = {
            "Name": name,
            "SV-Nummer": sv_number,
            "Eintrittsdatum": entry_date,
            "Austrittsdatum": exit_date,
            "Zielwert (%)": target_score,
        }
        data = data.append(new_participant, ignore_index=True)
        save_data(data, DATA_PATH)
        st.success("Teilnehmer hinzugefügt!")

# Vorhersagen generieren
st.subheader("Vorhersagen generieren")
participant = st.selectbox("Teilnehmer auswählen", data["Name"].unique())
if st.button("Vorhersagen erstellen"):
    participant_data = data[data["Name"] == participant]

    # H2O AutoML trainieren
    train_h2o_automl(data, "Zielwert (%)", MODEL_PATH)

    # Vorhersagen generieren
    predictions = generate_h2o_predictions(participant_data, MODEL_PATH)

    # Diagramm erstellen
    chart = generate_prediction_chart(participant_data, predictions, participant)
    st.plotly_chart(chart)

# Bericht generieren
st.subheader("Bericht generieren")
report_participant = st.selectbox("Teilnehmer für Bericht", data["Name"].unique())
if st.button("Bericht erstellen"):
    report_path = generate_report(report_participant, data, MODEL_PATH)
    st.success(f"Bericht erstellt: {report_path}")

# Fußzeile
st.write("---")
st.write("Mathematik-Kurs Teilnehmerverwaltung - Erstellt mit H2O AutoML")
