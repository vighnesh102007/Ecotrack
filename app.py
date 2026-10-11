
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "ecotrack.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            waste_type TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        location = request.form.get("location", "").strip()
        waste_type = request.form.get("waste_type", "").strip()
        description = request.form.get("description", "").strip()

        if location and waste_type and description:
            conn = get_db()
            conn.execute(
                """INSERT INTO reports
                (location, waste_type, description)
                VALUES (?, ?, ?)""",
                (location, waste_type, description)
            )
            conn.commit()
            conn.close()
            message = "Your waste report has been saved successfully!"
        else:
            message = "Please fill in all fields."

    return render_template("index.html", message=message)


@app.route("/dashboard")
def dashboard():
    conn = get_db()
    reports = conn.execute(
        "SELECT * FROM reports ORDER BY id DESC"
    ).fetchall()

    total = len(reports)
    pending = sum(r["status"] == "Pending" for r in reports)
    in_progress = sum(r["status"] == "In Progress" for r in reports)
    resolved = sum(r["status"] == "Resolved" for r in reports)

    conn.close()

    return render_template(
        "dashboard.html",
        reports=reports,
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved
    )



from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "ecotrack.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            waste_type TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        location = request.form.get("location", "").strip()
        waste_type = request.form.get("waste_type", "").strip()
        description = request.form.get("description", "").strip()

        if location and waste_type and description:
            conn = get_db()
            conn.execute(
                """INSERT INTO reports
                (location, waste_type, description)
                VALUES (?, ?, ?)""",
                (location, waste_type, description)
            )
            conn.commit()
            conn.close()
            message = "Your waste report has been saved successfully!"
        else:
            message = "Please fill in all fields."

    return render_template("index.html", message=message)


@app.route("/dashboard")
def dashboard():
    conn = get_db()
    reports = conn.execute(
        "SELECT * FROM reports ORDER BY id DESC"
    ).fetchall()

    total = len(reports)
    pending = sum(r["status"] == "Pending" for r in reports)
    in_progress = sum(r["status"] == "In Progress" for r in reports)
    resolved = sum(r["status"] == "Resolved" for r in reports)

    conn.close()

    return render_template(
        "dashboard.html",
        reports=reports,
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved
    )


@app.route("/update-status/<int:report_id>", methods=["POST"])
def update_status(report_id):
    status = request.form.get("status", "")
    allowed_statuses = ["Pending", "In Progress", "Resolved"]

    if status not in allowed_statuses:
        return "Invalid status", 400

    conn = get_db()
    conn.execute(
        "UPDATE reports SET status = ? WHERE id = ?",
        (status, report_id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
