import os
import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

def get_db():
    return psycopg2.connect(
        dbname=os.getenv("CC_DB_NAME", "nurse_job_postings"),
        user=os.getenv("CC_DB_USER", "kevindai"),
        password=os.getenv("CC_DB_PASSWORD"),
        host=os.getenv("CC_DB_HOST", "localhost"),
        port=os.getenv("CC_DB_PORT", "5432")
    )

@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()

    # Get filter options
    cursor.execute("SELECT DISTINCT site FROM job_postings ORDER BY site;")
    sites = [r[0] for r in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT department FROM job_postings ORDER BY department;")
    departments = [r[0] for r in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT employment FROM job_postings ORDER BY employment;")
    employment_types = [r[0] for r in cursor.fetchall()]

    # Get selected filters
    selected_site = request.args.get("site", "")
    selected_dept = request.args.get("department", "")
    selected_emp = request.args.get("employment", "")

    # Build query
    query = "SELECT id, title, site, department, employment FROM job_postings WHERE 1=1"
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
    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html",
        sites=sites,
        departments=departments,
        employment_types=employment_types,
        jobs=jobs,
        selected_site=selected_site,
        selected_dept=selected_dept,
        selected_emp=selected_emp
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)