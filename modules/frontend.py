import streamlit as st

from modules.database import (
    fetch_antibiotics,
    add_antibiotic,
    fetch_hospitals,
    add_hospital,
    add_report,
    fetch_reports,
)

def add_new_report_interface():

    st.title("Add a Microbiology Culture Report")

    patient_name = st.text_input("Patient Name:")
    mrn = st.text_input("MRN:")
    patient_type = st.selectbox("Inpatient/Outpatient:", ["Inpatient", "Outpatient"])
    icu_status = st.selectbox("ICU/Non-ICU:", ["ICU", "Non-ICU"])

    hospitals = fetch_hospitals()
    hospital_options = [h[0] for h in hospitals]
    selected_hospital = st.selectbox("Hospital:", options=hospital_options)

    state_options = sorted(set(h[1] for h in hospitals))
    selected_state = st.selectbox("State:", options=state_options)

    diagnosis = st.text_input("Diagnosis:")
    sample_type = st.text_input("Sample Type:")
    organism = st.text_input("Organism:")
    antibiotic_options = fetch_antibiotics()
    selected_antibiotics = st.multiselect(
        "Antibiotic Sensitivity:", options=antibiotic_options
    )
    antibiotic_sensitivity = ", ".join(selected_antibiotics)
    report_date = st.date_input("Report Date:")

    if st.button("Add Report"):
        add_report(patient_name, sample_type, organism, antibiotic_sensitivity, report_date)
        st.success("Report added successfully.")

def view_reports_interface(reports):

    st.title("Microbiology Culture Reports")
    reports = fetch_reports()

    for report in reports:
        st.markdown(f"**Report ID:** {report[0]}")
        st.markdown(f"**Patient Name:** {report[1]}")
        st.markdown(f"**Sample Type:** {report[2]}")
        st.markdown(f"**Organism:** {report[3]}")
        st.markdown(f"**Antibiotic Sensitivity:** {report[5]}")
        st.markdown(f"**Report Date:** {report[4]}")
        st.write("---")

def add_new_antibiotic_interface():

    st.title("Add a New Antibiotic")

    antibiotic_name = st.text_input("Antibiotic Name:")
    antibiotic_class = st.text_input("Antibiotic Class:")

    if st.button("Add Antibiotic"):
        add_antibiotic(antibiotic_name, antibiotic_class)
        st.success("Antibiotic added successfully.")

def add_new_hospital_interface():

    st.header("Add a New Hospital")

    hospital_name = st.text_input("Hospital Name:")
    state = st.text_input("State:")

    if st.button("Add Hospital"):
        add_hospital(hospital_name, state)
        st.success("Hospital added successfully.")