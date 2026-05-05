import pyodbc

# פרטי החיבור
server = r'DESKTOP-I97K2IC\SQLEXPRESS'
database = 'healthyLifestyle'
username = 'sa'

# יצירת החיבור
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 18 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    r'Trusted_Connection=yes;'
    r'TrustServerCertificate=yes;'
)

cursor = conn.cursor()

# דוגמה: SELECT מטבלת tips


# סגירת החיבור
cursor.close()
conn.close()

def get_connection():
    conn1 = pyodbc.connect(
        r'DRIVER={ODBC Driver 18 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        r'Trusted_Connection=yes;'
        r'TrustServerCertificate=yes;'
    )
    return conn1

