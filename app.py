import os
import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
DB_NAME = "data.db"

# --- BAZA YARATISH ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Asosiy baza
    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ism TEXT NOT NULL,
        familya TEXT NOT NULL,
        tel1 TEXT NOT NULL,
        tel2 TEXT,
        izoh TEXT,
        fani TEXT,
        admin TEXT,
        bosh_vaqti TEXT,
        sinfi TEXT,
        sana TEXT
    )
    """)

    # Registratsiya jadvali
    c.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ism TEXT NOT NULL,
        familya TEXT NOT NULL,
        tel1 TEXT NOT NULL,
        tel2 TEXT,
        izoh TEXT,
        fani TEXT,
        admin TEXT,
        bosh_vaqti TEXT,
        sinfi TEXT,
        sana TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# --- ASOSIY MENU ---
@app.route("/")
def index():
    return render_template_string("""
    <!doctype html>
    <html lang="uz">
    <head>
        <meta charset="utf-8">
        <title>MAGISTR BAZA</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style> body { background: #f0f2f5; } </style>
    </head>
    <body class="text-center p-5">
        <h1 class="mb-4">📊 O'quvchilar CRM tizimi</h1>
        <div class="d-flex justify-content-center gap-4">
            <a href="{{ url_for('registratsiya') }}" class="btn btn-primary btn-lg">
                <i class="fas fa-user-plus"></i> Registratsiya
            </a>
            <a href="{{ url_for('baza') }}" class="btn btn-success btn-lg">
                <i class="fas fa-database"></i> Baza
            </a>
        </div>
    </body>
    </html>
    """)
    
# --- REGISTRATSIYA SAHIFASI ---
@app.route("/registratsiya", methods=["GET", "POST"])
def registratsiya():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if request.method == "POST":
        ism = request.form["ism"]
        familya = request.form["familya"]
        tel1 = request.form["tel1"]
        tel2 = request.form.get("tel2")
        izoh = request.form.get("izoh")
        fani = request.form.get("fani")
        admin = request.form.get("admin")
        bosh_vaqti = request.form.get("bosh_vaqti")
        sinfi = request.form.get("sinfi")
        sana = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if ism and familya and tel1:
            c.execute("""INSERT INTO registrations 
                      (ism, familya, tel1, tel2, izoh, fani, admin, bosh_vaqti, sinfi, sana) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (ism, familya, tel1, tel2, izoh, fani, admin, bosh_vaqti, sinfi, sana))
            conn.commit()

    # Qidiruv
    search = request.args.get("search", "")
    if search:
        c.execute("SELECT * FROM registrations WHERE ism LIKE ? OR familya LIKE ? OR tel1 LIKE ?",
                  (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        c.execute("SELECT * FROM registrations")
    registrations = c.fetchall()
    conn.close()

    return render_template_string("""
    <!doctype html>
    <html lang="uz">
    <head>
        <meta charset="utf-8">
        <title>Registratsiya</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body class="p-4">
        <h2>📝 Yangi o‘quvchi registratsiyasi</h2>
        <form method="post" class="row g-3 mb-4">
            <div class="col-md-3"><input name="ism" placeholder="Ism" class="form-control" required></div>
            <div class="col-md-3"><input name="familya" placeholder="Familya" class="form-control" required></div>
            <div class="col-md-2"><input name="tel1" placeholder="Tel 1" class="form-control" required></div>
            <div class="col-md-2"><input name="tel2" placeholder="Tel 2" class="form-control"></div>
            <div class="col-md-2"><input name="izoh" placeholder="Izoh" class="form-control"></div>
            <div class="col-md-2"><input name="fani" placeholder="Fani" class="form-control"></div>
            <div class="col-md-2"><input name="admin" placeholder="Admin" class="form-control"></div>
            <div class="col-md-2"><input name="bosh_vaqti" placeholder="Bo'sh vaqti" class="form-control"></div>
            <div class="col-md-2"><input name="sinfi" placeholder="Sinfi" class="form-control"></div>
            <div class="col-12">
                <button class="btn btn-primary">Qo‘shish</button>
                <a href="{{ url_for('baza') }}" class="btn btn-success">📊 Bazaga o‘tish</a>   
            </div>
        </form>

        <form method="get" class="mb-3">
            <input type="text" name="search" value="{{ request.args.get('search','') }}" placeholder="Qidiruv..." class="form-control">
        </form>

        <h3>⏳ Registratsiyadagi o‘quvchilar</h3>
        <table class="table table-bordered table-hover bg-white shadow">
            <tr class="table-primary">
                <th>ID</th><th>Ism</th><th>Familya</th><th>Tel1</th><th>Tel2</th>
                <th>Izoh</th><th>Fani</th><th>Admin</th>
                <th>Bo'sh vaqti</th><th>Sinfi</th><th>Sana</th><th>Amallar</th>
            </tr>
            {% for s in registrations %}
            <tr>
                <td>{{ s[0] }}</td><td>{{ s[1] }}</td><td>{{ s[2] }}</td>
                <td>{{ s[3] }}</td><td>{{ s[4] }}</td><td>{{ s[5] }}</td>
                <td>{{ s[6] }}</td><td>{{ s[7] }}</td><td>{{ s[8] }}</td>
                <td>{{ s[9] }}</td><td>{{ s[10] }}</td>
                <td>
                    <a href="{{ url_for('move_to_baza', reg_id=s[0]) }}" class="btn btn-success btn-sm">✔</a>
                    <a href="{{ url_for('delete_registration', reg_id=s[0]) }}" class="btn btn-danger btn-sm">🗑</a>
                </td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """, registrations=registrations)

# Registratsiyadan bazaga o‘tkazish
@app.route("/move_to_baza/<int:reg_id>")
def move_to_baza(reg_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM registrations WHERE id=?", (reg_id,))
    student = c.fetchone()
    if student:
        c.execute("""INSERT INTO students 
                  (ism, familya, tel1, tel2, izoh, fani, admin, bosh_vaqti, sinfi, sana) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (student[1], student[2], student[3], student[4], student[5],
                   student[6], student[7], student[8], student[9], student[10]))
        c.execute("DELETE FROM registrations WHERE id=?", (reg_id,))
        conn.commit()
    conn.close()
    return redirect(url_for("registratsiya"))

# Registratsiyadan o‘chirish
@app.route("/delete_registration/<int:reg_id>")
def delete_registration(reg_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM registrations WHERE id=?", (reg_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("registratsiya"))

# --- BAZA SAHIFASI ---
@app.route("/baza", methods=["GET", "POST"])
def baza():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if request.method == "POST":
        ism = request.form["ism"]
        familya = request.form["familya"]
        tel1 = request.form["tel1"]
        tel2 = request.form.get("tel2")
        izoh = request.form.get("izoh")
        fani = request.form.get("fani")
        admin = request.form.get("admin")
        bosh_vaqti = request.form.get("bosh_vaqti")
        sinfi = request.form.get("sinfi")
        sana = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if ism and familya and tel1:
            c.execute("""INSERT INTO students 
                      (ism, familya, tel1, tel2, izoh, fani, admin, bosh_vaqti, sinfi, sana) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (ism, familya, tel1, tel2, izoh, fani, admin, bosh_vaqti, sinfi, sana))
            conn.commit()

    # Qidiruv
    search = request.args.get("search", "")
    if search:
        c.execute("SELECT * FROM students WHERE ism LIKE ? OR familya LIKE ? OR tel1 LIKE ?",
                  (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()

    return render_template_string("""
    <!doctype html>
    <html lang="uz">
    <head>
        <meta charset="utf-8">
        <title>Baza</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body class="p-4">
        <h2>📚 O‘quvchilar bazasi (soni: {{ students|length }})</h2>

        <form method="post" class="row g-3 mb-4">
            <div class="col-md-2"><input name="ism" placeholder="Ism" class="form-control" required></div>
            <div class="col-md-2"><input name="familya" placeholder="Familya" class="form-control" required></div>
            <div class="col-md-2"><input name="tel1" placeholder="Tel 1" class="form-control" required></div>
            <div class="col-md-2"><input name="tel2" placeholder="Tel 2" class="form-control"></div>
            <div class="col-md-2"><input name="izoh" placeholder="Izoh" class="form-control"></div>
            <div class="col-md-2"><input name="fani" placeholder="Fani" class="form-control"></div>
            <div class="col-md-2"><input name="admin" placeholder="Admin" class="form-control"></div>
            <div class="col-md-2"><input name="bosh_vaqti" placeholder="Bo'sh vaqti" class="form-control"></div>
            <div class="col-md-2"><input name="sinfi" placeholder="Sinfi" class="form-control"></div>
            <div class="col-12">
                    <button class="btn btn-success">Qo‘shish</button>
                    <a href="{{ url_for('registratsiya') }}" class="btn btn-primary">📝 Registratsiyaga o‘tish</a>
            </div>
        </form>

        <form method="get" class="mb-3">
            <input type="text" name="search" value="{{ request.args.get('search','') }}" placeholder="Qidiruv..." class="form-control">
        </form>

        <table class="table table-bordered table-hover bg-white shadow">
            <tr class="table-success">
                <th>ID</th><th>Ism</th><th>Familya</th><th>Tel1</th><th>Tel2</th>
                <th>Izoh</th><th>Fani</th><th>Admin</th>
                <th>Bo'sh vaqti</th><th>Sinfi</th><th>Sana</th><th>Amallar</th>
            </tr>
            {% for s in students %}
            <tr>
                <td>{{ s[0] }}</td><td>{{ s[1] }}</td><td>{{ s[2] }}</td>
                <td>{{ s[3] }}</td><td>{{ s[4] }}</td><td>{{ s[5] }}</td>
                <td>{{ s[6] }}</td><td>{{ s[7] }}</td><td>{{ s[8] }}</td>
                <td>{{ s[9] }}</td><td>{{ s[10] }}</td>
                <td>
                    <a href="{{ url_for('delete_student', student_id=s[0]) }}" class="btn btn-danger btn-sm">🗑</a>
                </td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """, students=students)

# Bazadan o‘chirish
@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("baza"))

# Favicon uchun route
@app.route("/favicon.ico")
def favicon():
    return "", 204

# --- FLASK RUN RAILWAY UCHUN ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
