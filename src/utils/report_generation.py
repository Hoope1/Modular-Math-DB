import pandas as pd
from fpdf import FPDF
import openpyxl

def generate_report(participant: str, participants: pd.DataFrame, tests: pd.DataFrame):
    """
    Generates a report in PDF and Excel format for a participant.
    
    Args:
        participant (str): Name of the participant.
        participants (pd.DataFrame): DataFrame of participants.
        tests (pd.DataFrame): DataFrame of tests.
    """
    participant_data = participants[participants["Name"] == participant].iloc[0]
    participant_tests = tests[tests["Teilnehmer"] == participant]

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Bericht für {participant}", ln=True, align="C")
    pdf.ln(10)

    # Participant Info
    pdf.cell(0, 10, txt=f"Name: {participant_data['Name']}", ln=True)
    pdf.cell(0, 10, txt=f"SV-Nummer: {participant_data['SV-Nummer']}", ln=True)
    pdf.cell(0, 10, txt=f"Berufswunsch: {participant_data['Berufswunsch']}", ln=True)
    pdf.cell(0, 10, txt=f"Eintrittsdatum: {participant_data['Eintrittsdatum']}", ln=True)
    pdf.cell(0, 10, txt=f"Austrittsdatum: {participant_data['Austrittsdatum']}", ln=True)
    pdf.ln(10)

    # Test Results
    pdf.cell(0, 10, txt="Testergebnisse:", ln=True)
    for index, test in participant_tests.iterrows():
        pdf.cell(0, 10, txt=f"- Datum: {test['Datum']}, Gesamt (%): {test['Gesamt (%)']:.2f}", ln=True)

    pdf.output(f"reports/{participant}-Bericht.pdf")

    # Generate Excel
    excel_path = f"reports/{participant}-Bericht.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        participants[participants["Name"] == participant].to_excel(writer, index=False, sheet_name="Teilnehmerdaten")
        participant_tests.to_excel(writer, index=False, sheet_name="Testergebnisse")
