from database import add_application_to_db, fetch_all_jobs_from_db, fetch_job_from_db
from flask import Flask, jsonify, render_template, request

COMPANY_NAME = "Company"

app = Flask(__name__)


@app.route("/")
def show_all_jobs():
    jobs = fetch_all_jobs_from_db()
    return render_template("home.html", company_name=COMPANY_NAME, jobs=jobs)


@app.route("/api/jobs")
def fetch_all_jobs():
    jobs = fetch_all_jobs_from_db()
    return jsonify(jobs)


@app.route("/job/<id>")
def show_job(id: int):
    job = fetch_job_from_db(id)
    if not job:
        return "Not Found", 404
    return render_template('jobpage.html', company_name=COMPANY_NAME, job=job)


@app.route("/api/job/<id>")
def fetch_job(id: int):
    job = fetch_job_from_db(id)
    return jsonify(job)


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id: int):
    data = request.form
    add_application_to_db(id, data)
    job = fetch_job_from_db(id)
    return render_template('application_submitted.html', company_name=COMPANY_NAME, application=data, job=job)


if __name__ == "__main__":
    app.run(debug=True)
