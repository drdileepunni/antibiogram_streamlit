import sqlite3

def init_db():
    conn = sqlite3.connect("microbiology_reports.db")
    conn.execute(
        """CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            sample_type TEXT NOT NULL,
            organism TEXT NOT NULL,
            report_date DATE NOT NULL
        );"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS antibiotics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class TEXT NOT NULL
        );"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS sensitivities (
            report_id INTEGER,
            antibiotic_id INTEGER,
            FOREIGN KEY(report_id) REFERENCES reports(id),
            FOREIGN KEY(antibiotic_id) REFERENCES antibiotics(id)
        );"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS hospitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            state TEXT NOT NULL
        );"""
    )

    conn.commit()
    conn.close()

def add_antibiotic(antibiotic_name, antibiotic_class):
    with sqlite3.connect("microbiology_reports.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO antibiotics (name, class)
            VALUES (?, ?);
            """,
            (antibiotic_name, antibiotic_class),
        )
        conn.commit()

def fetch_antibiotics():
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM antibiotics ORDER BY name;")
    antibiotics = cursor.fetchall()
    conn.close()
    return [antibiotic[0] for antibiotic in antibiotics]

def add_hospital(hospital_name, state):
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO hospitals (name, state)
        VALUES (?, ?);
        """,
        (hospital_name, state),
    )
    conn.commit()
    conn.close()

def fetch_hospitals():
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, state FROM hospitals ORDER BY name;")
    hospitals = cursor.fetchall()
    conn.close()
    return hospitals

def add_report(patient_name, sample_type, organism, antibiotic_sensitivity, report_date):
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO reports (patient_name, sample_type, organism, report_date)
        VALUES (?, ?, ?, ?);
        """,
        (patient_name, sample_type, organism, report_date),
    )
    report_id = cursor.lastrowid

    antibiotic_sensitivity = antibiotic_sensitivity.split(", ")
    for antibiotic_name in antibiotic_sensitivity:
        print(antibiotic_name)
        cursor.execute(
            "SELECT id FROM antibiotics WHERE name = ?;", (antibiotic_name,)
        )
        antibiotic_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO sensitivities (report_id, antibiotic_id) VALUES (?, ?);",
            (report_id, antibiotic_id),
        )

    conn.commit()
    conn.close()


def fetch_reports():
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT r.*, GROUP_CONCAT(a.name, ', ') as antibiotic_sensitivity
        FROM reports r
        LEFT JOIN sensitivities s ON r.id = s.report_id
        LEFT JOIN antibiotics a ON s.antibiotic_id = a.id
        GROUP BY r.id;
        """
    )
    reports = cursor.fetchall()
    conn.close()
    return reports