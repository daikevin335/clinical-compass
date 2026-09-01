import psycopg2
import os

""""
Connects Python to PSQL database & allows to filter nurse job postings

Basically:
- Connect to database
- Get the different sites, departments, and employment types
- Show them to the user
- User picks what they want to filter by
- Build the SQL query based on their choices
- Run the query
- Show the matching jobs
- Close the database connection

NOTES:
- fetchall() = get results back
- params = holds values that are being filtered
- selected_... = user choice of filter
- None = user skipped that filter

IMPORTANT:
%s in the SQL query are placeholders
the actual values are passed through the params 
so; not directly putting user input inot the SQL string
"""


# Connect to PSQL

conn = psycopg2.connect(
    dbname = os.getenv("CC_DB_NAME", "nurse_job_postings"),
    user = os.getenv("CC_DB_USER", "kevindai"),
    password = os.getenv("CC_DB_PASSWORD"),
    host = os.getenv("CC_DB_HOST", "localhost"), 
    port = os.getenv("CC_DB_HOST", "5432")
)
cursor = conn.cursor()

print("=== Clinical Compass - Job Filter ===\n")

# --- Show available sites --- 

cursor.execute("SELECT DISTINCT site FROM job_postings ORDER BY site;")
sites = [row[0] for row in cursor.fetchall()]
print("Available sites:")
for i, site in enumerate(sites, 1):
    print(f" {i}. {site}")
site_choice = input("\nFilter by site? (enter number or press Enter to skip): ").strip()
selected_site = sites[int(site_choice) - 1] if site_choice else None

# --- Show available departments --- 

cursor.execute("SELECT DISTINCT department FROM job_postings ORDER BY department;")
departments = [row[0] for row in cursor.fetchall()]
print("\nAvailable departments:")
for i, dept in enumerate(departments, 1):
    print(f" {i}. {dept}")
dept_choice = input("\nFilter by department? (enter number or press Enter to skip): ").strip()
selected_dept = departments[int(dept_choice) - 1] if dept_choice else None

# --- Show available employment types --- 

cursor.execute("SELECT DISTINCT employment FROM job_postings ORDER BY employment;")
employment_types = [row[0] for row in cursor.fetchall()]
print("\nAvailable employment types:")
for i, emp in enumerate(employment_types, 1):
    print(f" {i}. {emp}")
emp_choice = input("\nFilter by employment type? (enter number or press Enter to skip): ").strip()
selected_emp = employment_types[int(emp_choice) - 1] if emp_choice else None

# --- Build and run query --- 

query = "SELECT title, site, employment, department FROM job_postings WHERE 1=1"
params = [] 

if selected_site:
    query += " AND site = %s"
    params.append(selected_site)
if selected_dept:
    query += " AND department = %s"    
    params.append(selected_dept)    
if selected_emp:
    query += " AND employment = %s"
    params.append(selected_emp)

query += " ORDER BY site, title;"

cursor.execute(query, params)
results = cursor.fetchall()

# --- Print results --- 

print(f"\n=== {len(results)} matching jobs ===\n")
for title, site, employment, department in results:
    print(f" {title}")
    print(f" Site: {site}")
    print(f" Employment: {employment}")
    print(f" Department: {department}")
    print()

cursor.close()
conn.close()
