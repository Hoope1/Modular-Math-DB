import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from src.components.ui_elements import render_header, render_footer
from src.components.table import render_participants_table
from src.components.forms import render_participant_form, render_test_form
from src.utils.data_processing import load_data, save_data
from src.utils.predictions import generate_prediction_chart
from src.utils.report_generation import generate_report

# Konfigurationsoptionen
st.set_page_config(page_title="Mathematik-Kurs Management", layout="wide")

# Daten laden
participants = load_data("data/participants.csv")
tests = load_data("data/tests.csv")

# UI-Header
render_header()

# Teilnehmerverwaltung
st.subheader("Teilnehmerverwaltung")
participants = render_participants_table(participants)
if st.button("Teilnehmer hinzufügen"):
    new_participant = render_participant_form()
    if new_participant:
        participants = participants.append(new_participant, ignore_index=True)
        save_data(participants, "data/participants.csv")

# Tests zu Teilnehmern hinzufügen
st.subheader("Tests hinzufügen")
if st.button("Test hinzufügen"):
    selected_participant = st.selectbox("Teilnehmer auswählen", participants["Name"])
    new_test = render_test_form(selected_participant)
    if new_test:
        tests = tests.append(new_test, ignore_index=True)
        save_data(tests, "data/tests.csv")

# Prognose-Diagramm
st.subheader("Prognose")
selected_participant = st.selectbox("Teilnehmer auswählen für Prognose", participants["Name"])
chart = generate_prediction_chart(selected_participant, tests)
st.plotly_chart(chart, use_container_width=True)

# Berichtsgenerierung
st.subheader("Bericht erstellen")
if st.button("Bericht generieren"):
    selected_participant = st.selectbox("Teilnehmer auswählen für Bericht", participants["Name"])
    generate_report(selected_participant, participants, tests)
    st.success("Bericht wurde erfolgreich erstellt!")

# UI-Footer
render_footer()
