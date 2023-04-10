import sqlite3
import streamlit as st

from data.antibiotic_classes import antibiotics_and_classes
from data.organisms import organisms as organism_data
from data.specimen import specimens as specimen_list

from modules.database import (
    init_db,
    fetch_reports,
)
from modules.frontend import (
    add_new_report_interface,
    view_reports_interface,
    add_new_antibiotic_interface,
    add_new_hospital_interface,
    add_new_organism_interface,
    add_new_specimen_interface
)

def main():

    st.sidebar.title("Microbiology Culture Reports")
    page = st.sidebar.selectbox("Choose an action", ["Add a New Report", "View Reports", "Add to DB"])

    if page == "View Reports":
        reports = fetch_reports()
        view_reports_interface(reports)
    elif page == "Add a New Report":
        add_new_report_interface()
    elif page == "Add to DB":
        add_new_antibiotic_interface()
        add_new_hospital_interface()
        add_new_organism_interface()
        add_new_specimen_interface()

def count_antibiotics_rows():
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM antibiotics;
    """)

    count = cursor.fetchone()[0]
    conn.close()

    return count

def insert_antibiotics(antibiotics_and_classes):
    conn = sqlite3.connect("microbiology_reports.db")
    for name, antibiotic_class in antibiotics_and_classes.items():
        conn.execute(
            "INSERT OR IGNORE INTO antibiotics (name, class) VALUES (?, ?);",
            (name, antibiotic_class),
        )
    conn.commit()
    conn.close()

def populate_organisms():
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()

    for organism_name, organism_type in organism_data.items():
        cursor.execute("SELECT id FROM organisms WHERE name = ?", (organism_name,))
        organism_id = cursor.fetchone()

        if organism_id is None:  # If the organism name is not already present
            cursor.execute("""
                INSERT INTO organisms (name, organism_type) VALUES (?, ?)
            """, (organism_name, organism_type))

    conn.commit()
    conn.close()

def populate_specimens():
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()

    for specimen_name in specimen_list:
        cursor.execute("""
            INSERT OR IGNORE INTO specimens (name)
            VALUES (?)
        """, (specimen_name,))

    conn.commit()
    conn.close()

if __name__ == "__main__":

    init_db()
    if count_antibiotics_rows() == 0:
        insert_antibiotics(antibiotics_and_classes)
    populate_organisms()
    populate_specimens()
    main()