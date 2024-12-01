import streamlit as st

def render_header():
    """
    Rendert die Kopfzeile der Anwendung.
    """
    st.title("Mathematik-Kurs Teilnehmerverwaltung")
    st.markdown("## Willkommen im Teilnehmerverwaltungssystem")
    st.markdown("---")

def render_footer():
    """
    Rendert die Fußzeile der Anwendung.
    """
    st.markdown("---")
    st.markdown("**Erstellt mit Streamlit und H2O AutoML**")
    st.markdown("© 2024 Mathematik-Kurs Management")
