import sqlite3
import pandas as pd

def execute_query(database, query):
    conn = sqlite3.connect(database)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

print(execute_query("microbiology_reports.db", 
                    "SELECT * FROM antibiotics where name like 'Remdesivir'"))