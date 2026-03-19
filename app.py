from flask import Flask, render_template, request, redirect, session, url_for,flash as Flash,jsonify
import mysql.connector
import datetime

app = Flask(__name__)
app.secret_key = "assignment_secret_key"

# ================= DATABASE =================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="vms@2025#2005",
        database="assignment1"
    )

# ================= HOME =================
@app.route("/")
def home():
    return render_template("home1.html")

# =================================================
# ================= STUDENT LOGIN =================
# =================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        password = request.form.get("password")

        if not full_name or not password:
            return render_template("login1.html", error="Full Name and Password are required")

        full_name = full_name.strip()
        password = password.strip()

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM register WHERE full_name=%s AND password=%s",
            (full_name, password)
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if not user:
            return render_template("login1.html", error="Invalid Full Name or Password")

        session.clear()
        session["role"] = "student"
        session["student_name"] = user["full_name"]
        return redirect(url_for("stdapp"))

    return render_template("login1.html")



# =================================================
# ================= STUDENT REGISTER =================
# =================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        reg_no = request.form["reg_no"]
        email = request.form["email"]
        department = request.form["department"]
        password = request.form["password"]

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO register (full_name, reg_no, email, department, password) VALUES (%s,%s,%s,%s,%s)",
            (full_name, reg_no, email, department, password)
        )
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for("login"))

    return render_template("register1.html")

# =================================================
# ================= ADMIN LOGIN =================
# =================================================
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )
        admin = cursor.fetchone()
        cursor.close()
        db.close()

        if admin:
            session.clear()
            session["role"] = "admin"
            session["admin_id"] = admin["id"]
            session["username"] = admin["username"]
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("adminlog.html", error="Invalid Admin Login")

    return render_template("adminlog.html")



# =================================================
# ================= STAFF LOGIN =================
# =================================================
@app.route("/staff_login", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check empty fields
        if not email or not password:
            return render_template("stafflog.html", error="Email and Password are required")

        # Remove extra spaces
        email = email.strip()
        password = password.strip()

        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)

            # Query staff table
            cursor.execute(
                "SELECT staff_id, staff_name, password FROM staff1 WHERE email=%s",
                (email,)
            )
            staff = cursor.fetchone()

            cursor.close()
            db.close()

            # Check if staff exists and password matches
            if staff and staff["password"] == password:
                session.clear()
                session["role"] = "staff"
                session["staff_id"] = staff["staff_id"]
                session["staff_name"] = staff["staff_name"]
                return redirect(url_for("staff_dashboard"))
            else:
                return render_template("stafflog.html", error="Invalid Email or Password")

        except Exception as e:
            print("DB Error:", e)
            return render_template("stafflog.html", error="Database Error")

    return render_template("stafflog.html")

# ---------------- STAFF DASHBOARD ----------------
@app.route("/staff_dashboard", methods=["GET", "POST"])
def staff_dashboard():
    if session.get("role") != "staff":
        return redirect(url_for("staff_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 🔹 Fetch student submissions
    cursor.execute("SELECT * FROM submit1 ORDER BY id DESC")
    submissions = cursor.fetchall()

    # 🔹 Fetch assignments created
    cursor.execute("SELECT title, due_date FROM assign1 ORDER BY due_date DESC")
    assignments = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "staffdash.html",
        submissions=submissions,
        assignments=assignments
    )

@app.route("/create_assignment", methods=["POST"])
def create_assignment():
    if session.get("role") != "staff":
        return redirect(url_for("staff_login"))

    subject = request.form.get("subject")
    title = request.form.get("title")
    due_date = request.form.get("due_date")

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO assi (subject, title, due_date) VALUES (%s,%s,%s)",
        (subject, title, due_date)
    )
    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("staff_dashboard"))

# ---------------- CREATE ASSIGNMENT ----------------
@app.route("/create_assignment_simple", methods=["POST"])

def create_assignment_post():

    if session.get("role") != "staff":
        return redirect(url_for("staff_login"))

    title = request.form.get("title")
    subject = request.form.get("subject")
    department = request.form.get("department")
    due_date = request.form.get("due_date")

    if not title or not subject or not department or not due_date:
        return "All fields are required", 400

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
    "INSERT INTO assign1(title, subject, department, due_date) VALUES (%s,%s,%s,%s)",
    (title, subject, department, due_date)
)

    db.commit()
    

    # staff dashboard ku thirumba pogum
    return redirect(url_for("staff_dashboard"))
# Fetch all student submissions
    cursor.execute("SELECT * FROM submit1 ORDER BY id DESC")
    submissions = cursor.fetchall()
    # Pass submissions to template, staff can also create assignments on the same page
    return render_template("staffdash.html", submissions=submissions, staff_name=session.get("staff_name"))

    cursor.close()
    db.close()
@app.route("/staffacc")
def staffacc():
    if session.get("role") != "staff":
        return redirect(url_for("staff_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT staff_id, staff_name, email, department FROM staff1 WHERE staff_id=%s",
        (session.get("staff_id"),)
    )
    staff = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template("staffacc.html", staff=staff)
@app.route("/update_staff_profile", methods=["POST"])
def update_staff_profile():
    if session.get("role") != "staff":
        return redirect(url_for("staff_login"))

    new_staff_id = request.form.get("staff_id")
    staff_name = request.form.get("staff_name")
    email = request.form.get("email")
    department = request.form.get("department")

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE staff1
        SET staff_id=%s,
            staff_name=%s,
            email=%s,
            department=%s
        WHERE staff_id=%s
    """, (
        new_staff_id,
        staff_name,
        email,
        department,
        session.get("staff_id")  # old id
    ))

    db.commit()
    cursor.close()
    db.close()

    # 🔥 Update session also
    session["staff_id"] = new_staff_id
    session["staff_name"] = staff_name

    return redirect(url_for("staff_dashboard"))
    

#----------------stdapp-----------------------
@app.route("/stdapp")
def stdapp():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    student_name = session.get("student_name")

    # 🔹 Get student info
    cursor.execute("SELECT * FROM register WHERE full_name=%s", (student_name,))
    student = cursor.fetchone()

    # 🔹 Total assignments
    cursor.execute("SELECT * FROM assign1 ORDER BY due_date ASC")
    assignments = cursor.fetchall()
    total_assignments = len(assignments)

    # 🔹 Student submitted assignments (DISTINCT to avoid duplicates)
    cursor.execute(
        "SELECT DISTINCT assignment_title FROM submit1 WHERE student_name=%s",
        (student_name,)
    )
    submitted_data = cursor.fetchall()
    submitted_titles = [s["assignment_title"] for s in submitted_data]
    submitted_count = len(submitted_titles)

    # ✅ CORRECT PENDING CALCULATION
    pending_count = 0
    for a in assignments:
        if a["title"] not in submitted_titles:
            pending_count += 1

    # ✅ NEXT DUE (First unsubmitted assignment only)
    next_due = None
    for a in assignments:
        if a["title"] not in submitted_titles:
            next_due = a["due_date"]
            break

    cursor.close()
    db.close()

    return render_template(
        "stdapp.html",
        assignments=assignments,
        student=student,
        student_name=student_name,
        total_assignments=total_assignments,
        submitted_count=submitted_count,
        pending_count=pending_count,
        next_due=next_due,
        submitted_titles=submitted_titles
    )
@app.route("/update_student_profile", methods=["POST"])
def update_student_profile():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    full_name = request.form.get("full_name")
    email = request.form.get("email")
    department = request.form.get("department")

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE register
        SET full_name=%s, email=%s, department=%s
        WHERE full_name=%s
    """, (
        full_name,
        email,
        department,
        session.get("student_name")
    ))

    db.commit()
    cursor.close()
    db.close()

    # update session name also
    session["student_name"] = full_name

    return redirect(url_for("stdapp"))



# ---------------- SUBMIT ASSIGNMENT (STUDENT) ----------------
@app.route("/submit_assignment", methods=["POST"])
def submit_assignment():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    assignment_title = request.form.get("assignment_title")
    student_name = session.get("student_name")
    reg_no = request.form.get("reg_no")
    email = request.form.get("email")
    department = request.form.get("department")
    year = request.form.get("year")
    section = request.form.get("section")
    pdf = request.files.get("pdf_file")

    if not assignment_title or not pdf:
        return "Required fields missing", 400

    import os
    os.makedirs("static/uploads", exist_ok=True)

    filename = f"{reg_no}_{assignment_title}.pdf"
    pdf.save(os.path.join("static/uploads", filename))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO submit1
        (assignment_title, student_name, reg_no, email,
         department, year, section, pdf_file)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        assignment_title,
        student_name,
        reg_no,
        email,
        department,
        year,
        section,
        filename
    ))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("stdapp"))

# ---------------- UPDATE MARKS / STATUS (STAFF) ----------------
@app.route("/update_submission/<int:submission_id>", methods=["POST"])
def update_submission(submission_id):
    if session.get("role") != "staff":
        return redirect(url_for("staff_login"))

    marks = request.form.get("marks")
    status = request.form.get("status")

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE submit1 SET marks=%s, status=%s WHERE id=%s",
        (marks, status, submission_id)
    )
    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("staff_dashboard"))




# ---------------- LOGOUT ----------------
@app.route("/staff_logout")
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ================= STAFF REGISTER =================
@app.route("/staff_register", methods=["GET", "POST"])
def staff_register():
    if request.method == "POST":
        staff_name = request.form.get("staff_name")
        email = request.form.get("email")
        staff_id = request.form.get("staff_id")
        department = request.form.get("department")
        password = request.form.get("password")

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO staff1 (staff_id, staff_name, department, email, password) VALUES (%s,%s,%s,%s,%s)",
            (staff_id, staff_name, department, email, password)
        )
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for("staff_login"))

    return render_template("staffreg.html")

# ================= STATIC PAGES =================
@app.route("/about")
def about():
    return render_template("about1.html")
#------------------------------CONTACT FORM-------

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Insert into MySQL table `contact`
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO contact (full_name, email, subject, message) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (full_name, email, subject, message))
        conn.commit()
        cursor.close()
        conn.close()

        Flash("Feedback submitted successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")
# ---------- ADMIN DASHBOARD PAGE ----------
@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # -------- FACULTY --------
    cursor.execute("""
        SELECT staff_id, staff_name, department, 'Active' AS status
        FROM staff1
    """)
    faculty = cursor.fetchall()

    # -------- STUDENTS --------
    cursor.execute("""
        SELECT reg_no, full_name, department, 'Active' AS status
        FROM register
    """)
    students = cursor.fetchall()

    # -------- ASSIGNMENT SUBMISSIONS --------
    cursor.execute("""
        SELECT id,
               assignment_title,
               student_name,
               reg_no,
               department,
               year,
               section,
               pdf_file,
               IFNULL(marks, '-') AS marks,
               IFNULL(status, 'Pending') AS status
        FROM submit1
        ORDER BY id DESC
    """)
    submissions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admindash.html",
        username=session.get("username"),
        faculty=faculty,
        students=students,
        submissions=submissions
    )



# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
