import streamlit as st
import pandas as pd
from src.components.ui_elements import render_header, render_footer
from src.components.table import render_participants_table
from src.components.forms import render_participant_form, render_test_form
from src.utils.data_processing import load_data, save_data
from src.utils.predictions import train_h2o_automl, generate_h2o_predictions, generate_prediction_chart
from src.utils.report_generation import generate_report
import os

# Konfigurationen
DATA_FILE = "data/participants.csv"
MODEL_FILE = "models/h2o_model"

# Lade Daten
data = load_data(DATA_FILE)

# Streamlit-App
render_header()

# Tabellenansicht
st.subheader("Teilnehmerübersicht")
render_participants_table(data)

# Teilnehmer hinzufügen
render_participant_form(data, lambda updated_data: save_data(updated_data, DATA_FILE))

# Testdaten hinzufügen
selected_participant = st.selectbox("Wähle einen Teilnehmer für Tests:", data["Name"].unique())
if selected_participant:
    participant_data = data[data["Name"] == selected_participant]
    render_test_form(data, selected_participant, lambda updated_data: save_data(updated_data, DATA_FILE))

# Modelltraining
if st.button("Modell trainieren"):
    st.info("Training startet...")
    try:
        train_h2o_automl(data, target_column="Zielwert (%)", model_path=MODEL_FILE)
        st.success("Modell erfolgreich trainiert und gespeichert!")
    except Exception as e:
        st.error(f"Fehler beim Training: {str(e)}")

# Vorhersagediagramm
if selected_participant:
    st.subheader(f"Vorhersagen für {selected_participant}")
    try:
        predictions = generate_h2o_predictions(participant_data, MODEL_FILE)
        fig = generate_prediction_chart(participant_data, predictions, selected_participant)
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Fehler beim Generieren der Vorhersagen: {str(e)}")

# Bericht generieren
if st.button("Bericht generieren"):
    try:
        report_path = generate_report(selected_participant, data, MODEL_FILE)
        st.success(f"Bericht erfolgreich generiert: {report_path}")
    except Exception as e:
        st.error(f"Fehler beim Generieren des Berichts: {str(e)}")

render_footer()
