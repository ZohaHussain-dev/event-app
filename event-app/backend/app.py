import os, time
import psycopg2
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # exposes /metrics for Prometheus

DB = dict(
    host=os.getenv("DB_HOST", "postgres"),
    dbname=os.getenv("DB_NAME", "eventdb"),
    user=os.getenv("DB_USER", "eventuser"),
    password=os.getenv("DB_PASSWORD", "eventpass"),
)

EVENTS = [
    {"id": 1, "name": "NESCON", "date": "2026-11-20", "venue": "Main Auditorium", "desc": "Annual national engineering & science convention."},
    {"id": 2, "name": "ACM Hackathon", "date": "2026-11-27", "venue": "CS Lab Block", "desc": "24-hour coding hackathon by ACM chapter."},
    {"id": 3, "name": "Execup", "date": "2026-12-05", "venue": "Seminar Hall", "desc": "Business and entrepreneurship competition."},
    {"id": 4, "name": "Visionspark", "date": "2026-12-12", "venue": "Open Arena", "desc": "Innovation showcase and project exhibition."},
]

def get_conn():
    return psycopg2.connect(**DB)

def init_db():
    for _ in range(30):
        try:
            with get_conn() as c, c.cursor() as cur:
                cur.execute("""CREATE TABLE IF NOT EXISTS registrations(
                    id SERIAL PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL,
                    event_id INT NOT NULL, created_at TIMESTAMP DEFAULT NOW())""")
            return
        except Exception as e:
            print("waiting for db...", e)
            time.sleep(2)

init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/events")
def events():
    return jsonify(EVENTS)

@app.post("/register")
def register():
    d = request.get_json(force=True)
    if not d.get("name") or not d.get("email") or not d.get("event_id"):
        return {"error": "name, email and event_id required"}, 400
    with get_conn() as c, c.cursor() as cur:
        cur.execute("INSERT INTO registrations(name,email,event_id) VALUES(%s,%s,%s)",
                    (d["name"], d["email"], int(d["event_id"])))
    return {"message": "Registered successfully"}, 201

@app.get("/registrations")
def registrations():
    with get_conn() as c, c.cursor() as cur:
        cur.execute("SELECT id,name,email,event_id,created_at FROM registrations ORDER BY id DESC LIMIT 20")
        rows = cur.fetchall()
    return jsonify([{"id": r[0], "name": r[1], "email": r[2], "event_id": r[3], "at": str(r[4])} for r in rows])
