import sqlite3
import streamlit as st

from antibiotic_classes import antibiotics_and_classes

from modules.database import (
    init_db,
    fetch_reports,
)
from modules.frontend import (
    add_new_report_interface,
    view_reports_interface,
    add_new_antibiotic_interface,
    add_new_hospital_interface,
)

init_db()

def insert_antibiotics(antibiotics_and_classes):
    conn = sqlite3.connect("microbiology_reports.db")
    for name, antibiotic_class in antibiotics_and_classes.items():
        conn.execute(
            "INSERT OR IGNORE INTO antibiotics (name, class) VALUES (?, ?);",
            (name, antibiotic_class),
        )
    conn.commit()
    conn.close()

# insert_antibiotics(antibiotics_and_classes)

init_db()

st.sidebar.title("Microbiology Culture Reports")
page = st.sidebar.selectbox("Choose an action", ["View Reports", "Add a New Report", "Add a New Antibiotic"])

if page == "View Reports":
    reports = fetch_reports()
    view_reports_interface(reports)
elif page == "Add a New Report":
    add_new_report_interface()
elif page == "Add a New Antibiotic":
    add_new_antibiotic_interface()
    add_new_hospital_interface()

