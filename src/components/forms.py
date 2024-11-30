import streamlit as st
import pandas as pd

def render_participant_form() -> dict:
    """
    Displays a form to add a new participant.

    Returns:
        dict: A dictionary containing the new participant's details or None if the form is cancelled.
    """
    with st.form("participant_form", clear_on_submit=True):
        st.write("### Teilnehmer hinzufügen")
        name = st.text_input("Name")
        sv_number = st.text_input("SV-Nummer (XXXXDDMMYY)")
        career_goal = st.text_input("Berufswunsch (Abkürzung)")
        entry_date = st.date_input("Eintrittsdatum")
        exit_date = st.date_input("Austrittsdatum")

        submitted = st.form_submit_button("Teilnehmer hinzufügen")
        if submitted and name and sv_number and career_goal:
            return {
                "Name": name,
                "SV-Nummer": sv_number,
                "Berufswunsch": career_goal,
                "Eintrittsdatum": entry_date,
                "Austrittsdatum": exit_date,
            }
    return None

def render_test_form(selected_participant: str) -> dict:
    """
    Displays a form to add a test for a specific participant.

    Args:
        selected_participant (str): The name of the selected participant.

    Returns:
        dict: A dictionary containing the test details or None if the form is cancelled.
    """
    with st.form(f"test_form_{selected_participant}", clear_on_submit=True):
        st.write(f"### Test für {selected_participant} hinzufügen")
        test_date = st.date_input("Testdatum")
        categories = {
            "Textaufgaben": st.number_input("Textaufgaben Punkte", min_value=0, max_value=100, step=1),
            "Raumvorstellung": st.number_input("Raumvorstellung Punkte", min_value=0, max_value=100, step=1),
            "Gleichungen": st.number_input("Gleichungen Punkte", min_value=0, max_value=100, step=1),
            "Brüche": st.number_input("Brüche Punkte", min_value=0, max_value=100, step=1),
            "Grundrechenarten": st.number_input("Grundrechenarten Punkte", min_value=0, max_value=100, step=1),
            "Zahlenraum": st.number_input("Zahlenraum Punkte", min_value=0, max_value=100, step=1),
        }
        submitted = st.form_submit_button("Test hinzufügen")
        if submitted and test_date:
            total_points = sum(categories.values())
            return {
                "Teilnehmer": selected_participant,
                "Datum": test_date,
                **categories,
                "Gesamtpunkte": total_points,
            }
    return None
