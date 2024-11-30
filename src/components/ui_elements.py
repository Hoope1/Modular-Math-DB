import streamlit as st

def render_header():
    """
    Renders the header of the Streamlit app with a title and description.
    """
    st.title("Mathematik-Kurs Management Tool")
    st.caption("Verwalten Sie Teilnehmer, Tests und Prognosen effizient.")

def render_footer():
    """
    Renders a footer with credits or additional information.
    """
    st.markdown("---")
    st.markdown("Dieses Tool wurde entwickelt, um Mathematik-Kurse zu verwalten und zu optimieren.")
