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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organisms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            organism_type TEXT NOT NULL
        );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS specimens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS sensitivities (
            report_id INTEGER,
            antibiotic_id INTEGER,
            FOREIGN KEY(report_id) REFERENCES reports(id),
            FOREIGN KEY(antibiotic_id) REFERENCES antibiotics(id)
        );"""
    )
    conn.execute("""
        CREATE TABLE IF NOT EXISTS resistance (
            report_id INTEGER,
            antibiotic_id INTEGER,
            FOREIGN KEY (report_id) REFERENCES reports (id),
            FOREIGN KEY (antibiotic_id) REFERENCES antibiotics (id)
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS intermediate (
            report_id INTEGER,
            antibiotic_id INTEGER,
            FOREIGN KEY (report_id) REFERENCES reports (id),
            FOREIGN KEY (antibiotic_id) REFERENCES antibiotics (id)
        );
    """)
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

def get_organism_list():
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM organisms")
    organisms = [item[0] for item in cursor.fetchall()]

    conn.close()
    return organisms

def get_specimen_list():
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM specimens")
    specimen_list = [row[0] for row in cursor.fetchall()]

    conn.close()
    return specimen_list

def add_specimen(specimen_name):
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO specimens (name)
        VALUES (?)
    """, (specimen_name,))

    conn.commit()
    conn.close()

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

def add_organism(organism_name, organism_type):
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO organisms (name, organism_type)
        VALUES (?, ?)
    """, (organism_name, organism_type))

    conn.commit()
    conn.close()

def fetch_hospitals():
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, state FROM hospitals ORDER BY name;")
    hospitals = cursor.fetchall()
    conn.close()
    return hospitals

def add_report(patient_name, sample_type, organism, antibiotic_sensitivity,resistant_antibiotics, intermediate_antibiotics, report_date):
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

    if antibiotic_sensitivity:
        antibiotic_sensitivity = antibiotic_sensitivity.split(", ")
        for antibiotic_name in antibiotic_sensitivity:
            if antibiotic_name != "None":
                cursor.execute(
                    "SELECT id FROM antibiotics WHERE name = ?;", (antibiotic_name,)
                )
                antibiotic_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO sensitivities (report_id, antibiotic_id) VALUES (?, ?);",
                    (report_id, antibiotic_id),
                )
    
    if resistant_antibiotics:
        resistant_antibiotics = resistant_antibiotics.split(", ")
        for antibiotic_name in resistant_antibiotics:
            if antibiotic_name != "None":
                cursor.execute("""
                    SELECT id FROM antibiotics WHERE name = ?;
                """, (antibiotic_name,))

                antibiotic_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO resistance (report_id, antibiotic_id)
                    VALUES (?, ?);
                """, (report_id, antibiotic_id))

    if intermediate_antibiotics:
        intermediate_antibiotics = intermediate_antibiotics.split(", ")
        for antibiotic_name in intermediate_antibiotics:
            if antibiotic_name != "None":
                cursor.execute("""
                    SELECT id FROM antibiotics WHERE name = ?;
                """, (antibiotic_name,))

                antibiotic_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO intermediate (report_id, antibiotic_id)
                    VALUES (?, ?);
                """, (report_id, antibiotic_id))

    conn.commit()
    conn.close()


def fetch_reports():
    conn = sqlite3.connect("microbiology_reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT reports.id, patient_name, sample_type, organism, group_concat(sensitive.name, ', ') as sensitive_antibiotics,
               group_concat(resistant.name, ', ') as resistant_antibiotics, group_concat(intermediate.name, ', ') as intermediate_antibiotics, report_date
        FROM reports
        LEFT JOIN sensitivities ON reports.id = sensitivities.report_id
        LEFT JOIN antibiotics as sensitive ON sensitivities.antibiotic_id = sensitive.id
        LEFT JOIN resistance ON reports.id = resistance.report_id
        LEFT JOIN antibiotics as resistant ON resistance.antibiotic_id = resistant.id
        LEFT JOIN intermediate ON reports.id = intermediate.report_id
        LEFT JOIN antibiotics as intermediate ON intermediate.antibiotic_id = intermediate.id
        GROUP BY reports.id;
    """)

    reports = cursor.fetchall()
    conn.close()
    return reports
