from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

type = os.getenv('DB_TYPE')
connector = os.getenv('DB_CONNECTOR')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')

db_connection_string = f"{type}+{connector}://{user}:{password}@{host}/{database}?charset=utf8mb4"

engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
)


def fetch_all_jobs_from_db():
    with engine.connect() as conn:
        query = text("SELECT * FROM jobs")
        result = conn.execute(query)
        jobs = [dict(row) for row in result.mappings()]
        return jobs


def fetch_job_from_db(job_id: int):
    with engine.connect() as conn:
        query = text("SELECT * FROM jobs WHERE id = :job_id LIMIT 1")
        params = dict(job_id=job_id)
        result = conn.execute(query, params)
        jobs = [dict(row) for row in result.mappings()]
        return None if len(jobs) == 0 else jobs[0]


def add_application_to_db(job_id: int, data):
    with engine.connect() as conn:
        query = text("""
            INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) 
            VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)
        """)
        params = dict(job_id=job_id, **data)
        conn.execute(query, params)
