import streamlit as st
import pandas as pd

def render_participants_table(participants: pd.DataFrame) -> pd.DataFrame:
    """
    Renders an editable table of participants and handles updates.
    
    Args:
        participants (pd.DataFrame): The current DataFrame of participants.

    Returns:
        pd.DataFrame: The updated DataFrame after edits.
    """
    # Statusberechnung (Aktiv/Inaktiv)
    today = pd.Timestamp("today")
    participants["Status"] = participants["Austrittsdatum"].apply(
        lambda x: "Aktiv" if pd.to_datetime(x) > today else "Inaktiv"
    )

    # Darstellung der Tabelle
    st.markdown("### Teilnehmerübersicht")
    updated_participants = st.data_editor(
        participants, num_rows="dynamic", key="participants_editor"
    )

    # Inaktive Teilnehmer ausgrauen
    if st.checkbox("Inaktive Teilnehmer anzeigen"):
        return updated_participants
    else:
        return updated_participants[updated_participants["Status"] == "Aktiv"]
