import streamlit as st
import pandas as pd

from modules.database import (
    fetch_antibiotics,
    get_organism_list,
    add_antibiotic,
    fetch_hospitals,
    add_hospital,
    add_organism,
    add_report,
    fetch_reports,
    get_specimen_list,
    add_specimen
)

def add_new_report_interface():

    st.title("Add a Microbiology Culture Report")

    col1, col2 = st.columns(2)

    with col1:

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

    with col2:

        specimen_list = get_specimen_list()
        sample_type = st.selectbox("Sample Type", specimen_list)
        organism_list = get_organism_list()
        organism = st.multiselect("Organisms", organism_list)
        antibiotic_options = fetch_antibiotics()
        antibiotics_with_none = ["None"] + antibiotic_options
        selected_antibiotics_sensitive = st.multiselect(
            "Antibiotic Sensitivity:", options=antibiotics_with_none
        )
        selected_antibiotics_resistant = st.multiselect(
            "Antibiotic Resistance:", options=antibiotics_with_none
        )
        selected_antibiotics_intermediate = st.multiselect(
            "Antibiotic Int. Sensitivity:", options=antibiotics_with_none
        )
        organism = ", ".join(organism)
        antibiotic_sensitivity = ", ".join(selected_antibiotics_sensitive)
        resistant_antibiotics = ", ".join(selected_antibiotics_resistant)
        intermediate_antibiotics = ", ".join(selected_antibiotics_intermediate)
        report_date = st.date_input("Report Date:")

    # Check if the user has selected an antibiotic in each dropdown
    antibiotics_selected = (
        any(organism)
        or any(selected_antibiotics_sensitive)
        or any(selected_antibiotics_resistant)
        or any(selected_antibiotics_intermediate)
    )

    if st.button("Add Report", disabled= not antibiotics_selected):
        add_report(patient_name, sample_type, organism, antibiotic_sensitivity, resistant_antibiotics, intermediate_antibiotics, report_date)
        st.success("Report added successfully.")

def view_reports_interface(reports):
    st.subheader("View Reports")
    reports = fetch_reports()
    for report in reports:
        st.write("ID:", report[0])
        st.write("Patient Name:", report[1])
        st.write("Sample Type:", report[2])
        st.write("Organism:", report[3])
        st.write("Sensitive Antibiotics:", report[4])
        st.write("Resistant Antibiotics:", report[5])  # Display resistant antibiotics
        st.write("Intermediate Antibiotics:", report[6])  # Display intermediate antibiotics
        st.write("Report Date:", report[7])
        st.write("---")

def add_new_antibiotic_interface():

    st.title("Add to DB")
    st.header("Add a New Antibiotic")

    antibiotic_name = st.text_input("Antibiotic Name:")
    antibiotic_class = st.text_input("Antibiotic Class:")

    if st.button("Add Antibiotic"):
        add_antibiotic(antibiotic_name, antibiotic_class)
        st.success("Antibiotic added successfully.")

def add_new_organism_interface():

    st.header("Add New Organism")

    organism_name = st.text_input("Organism Name")
    organism_type = st.text_input("Organism Type")

    add_organism_button = st.button("Add Organism")

    if add_organism_button:
        add_organism(organism_name, organism_type)
        st.success(f"Organism '{organism_name}' added successfully.")

def add_new_specimen_interface():

    st.header("Add New Specimen")

    specimen_name = st.text_input("Specimen Name")

    add_specimen_button = st.button("Add Specimen")

    if add_specimen_button:
        
        add_specimen(specimen_name)
        st.success(f"Specimen '{specimen_name}' added successfully.")


def add_new_hospital_interface():

    st.header("Add a New Hospital")

    hospital_name = st.text_input("Hospital Name:")
    state = st.text_input("State:")

    if st.button("Add Hospital"):
        add_hospital(hospital_name, state)
        st.success("Hospital added successfully.")

def reports_as_df():

    reports = fetch_reports()

    reports_df = pd.DataFrame(
        reports,
        columns=[
            "ID",
            "Patient Name",
            "Sample Type",
            "Organism",
            "Sensitive Antibiotics",
            "Resistant Antibiotics",  # Add resistant antibiotics
            "Intermediate Antibiotics",  # Add intermediate antibiotics
            "Report Date",
        ],
    )
    st.dataframe(reports_df)