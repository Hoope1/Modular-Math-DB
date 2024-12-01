import streamlit as st
import pandas as pd
from datetime import date

def render_participant_form(data: pd.DataFrame, save_callback):
    """
    Rendert das Formular zum Hinzufügen von Teilnehmern.

    Args:
        data (pd.DataFrame): Der aktuelle Teilnehmerdatensatz.
        save_callback (function): Funktion, um die aktualisierten Daten zu speichern.
    """
    st.subheader("Teilnehmer hinzufügen")
    with st.form("add_participant_form"):
        name = st.text_input("Name")
        sv_number = st.text_input("SV-Nummer (XXXXDDMMYY)")
        entry_date = st.date_input("Eintrittsdatum", value=date.today())
        exit_date = st.date_input("Austrittsdatum", value=date.today())
        target_score = st.number_input("Zielwert (%)", min_value=0, max_value=100, value=50)

        submitted = st.form_submit_button("Teilnehmer hinzufügen")

        if submitted:
            if not name or not sv_number:
                st.error("Name und SV-Nummer sind erforderlich!")
            else:
                # Teilnehmerdaten hinzufügen
                new_participant = {
                    "Name": name,
                    "SV-Nummer": sv_number,
                    "Eintrittsdatum": entry_date,
                    "Austrittsdatum": exit_date,
                    "Zielwert (%)": target_score,
                }
                data = data.append(new_participant, ignore_index=True)
                save_callback(data)
                st.success(f"Teilnehmer {name} wurde hinzugefügt!")

def render_test_form(data: pd.DataFrame, participant: str, save_callback):
    """
    Rendert das Formular zum Hinzufügen von Testergebnissen.

    Args:
        data (pd.DataFrame): Der aktuelle Datensatz.
        participant (str): Der ausgewählte Teilnehmer.
        save_callback (function): Funktion, um die aktualisierten Daten zu speichern.
    """
    st.subheader(f"Test für {participant} hinzufügen")
    with st.form(f"add_test_form_{participant}"):
        test_date = st.date_input("Testdatum", value=date.today())
        text_tasks = st.number_input("Textaufgaben (%)", min_value=0, max_value=100, value=0)
        spatial = st.number_input("Raumvorstellung (%)", min_value=0, max_value=100, value=0)
        equations = st.number_input("Gleichungen (%)", min_value=0, max_value=100, value=0)
        fractions = st.number_input("Brüche (%)", min_value=0, max_value=100, value=0)
        arithmetic = st.number_input("Grundrechenarten (%)", min_value=0, max_value=100, value=0)
        numbers = st.number_input("Zahlenraum (%)", min_value=0, max_value=100, value=0)

        submitted = st.form_submit_button("Test hinzufügen")

        if submitted:
            if not participant:
                st.error("Teilnehmer ist erforderlich!")
            else:
                # Testergebnis hinzufügen
                new_test = {
                    "Name": participant,
                    "Datum": test_date,
                    "Textaufgaben (%)": text_tasks,
                    "Raumvorstellung (%)": spatial,
                    "Gleichungen (%)": equations,
                    "Brüche (%)": fractions,
                    "Grundrechenarten (%)": arithmetic,
                    "Zahlenraum (%)": numbers,
                    "Gesamt (%)": (text_tasks + spatial + equations + fractions + arithmetic + numbers) / 6,
                }
                data = data.append(new_test, ignore_index=True)
                save_callback(data)
                st.success(f"Test für {participant} wurde hinzugefügt!")
