from collections import defaultdict
from config import db_config
import mysql.connector 
from mysql.connector import IntegrityError
from flask import Flask, redirect, render_template, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import re
import secrets
import string
from dotenv import load_dotenv
import os 
from datetime import datetime, time as dt_time

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def generate_pw(length=15):
    pw = string.ascii_letters + string.digits
    return ''.join(secrets.choice(pw) for _ in range(length))

def get_db_connection():
    return mysql.connector.connect(**db_config)

#check if slot is still valid (not in the past)
def valid_slot(slot):
    slot_dt = datetime.strptime(f"{slot['Date']} {slot['Time']}", "%Y-%m-%d %H:%M:%S")
    return slot_dt >= datetime.now()

#clear cache
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"      
    return r

@app.route("/")
def access():
    return render_template("access-portal.html", show_menu=False, show_footer=False, role=None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role") or request.args.get("role")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        table_map = {
            "doctor": "doctor",
            "nurse": "nurse",
            "patient": "patient"
        }
        
        if role not in table_map:
            flash("Invalid role.", "error")
            return redirect(f"/login?role={role}")

        cursor.execute(f"SELECT * FROM {table_map[role]} WHERE Username = %s", (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if user:
            if user["Password"] is None:
                flash("Account not registered yet. Please sign up!", "error")
                return redirect(f"/login?role={role}")
            
            if check_password_hash(user["Password"], password):
                id_role = {
                    "doctor": "DoctorID",
                    "nurse": "NurseID",
                    "patient": "PatientID"
                }

                session["user_id"] = user[id_role[role]]
                session["username"] = user["Username"]
                session["role"] = role
                
                return redirect(f"/{role}")
  
        flash("Invalid username or password.", "error")
        return redirect(f"/login?role={role}")

    return render_template("login.html", show_menu=False, show_footer=False)

# ====================================================================================

# Sign Up
@app.route("/signup", methods=["GET", "POST"])

def signup():
    
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            name = request.form.get("name")
            email = request.form.get("email")
            telno = request.form.get("telno")
            role = request.form.get("role")
            
            # validation
            if len(username) < 3:
                flash("Username must be at least 3 characters.", "error")
                return redirect("/signup")

            if len(password) < 15:
                flash("Password must be at least 15 characters.", "error")
                return redirect("/signup")
            
            table_map = {
                "doctor": "doctor",
                "nurse" : "nurse"
            }
            
            table = table_map.get(role)
            
            if not table:
                flash("Invalid role.", "error")
                return redirect("/signup")
            
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
        
            # Check name and email 
            cursor.execute(f"""
                SELECT * FROM {table} WHERE Name = %s AND Email = %s
            """, (name, email))
            
            registered_staff = cursor.fetchone()
            
            if not registered_staff:
                flash("Staff not found. Try again or contact admin.", "error")
                cursor.close()
                conn.close()
                return redirect("/signup")
            
            # prevent duplicate username
            cursor.execute(f"SELECT * FROM {table} WHERE Username = %s", (username,))
            if cursor.fetchone():
                flash("Username already exists.", "error")
                cursor.close()
                conn.close()
                return redirect("/signup")
            
            # check pw is already filled
            if registered_staff["Password"] is not None:
                flash("Account already registed. Please login.", "error")
                cursor.close()
                conn.close()
                return redirect(f"/login?role={role}")
            
            hash_pw = generate_password_hash(password)
            cursor.execute(f"""
                UPDATE {table}
                SET Username = %s, Password = %s, TelNo = %s
                WHERE Email = %s
            """, (username, hash_pw, telno, email))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash("Account created successfully! Please login.", "success")
            return redirect(f"/login?role={role}")
            
            
    except mysql.connector.IntegrityError:
        flash("Username or email already exists", "error")
        
    return render_template("sign-up.html", show_menu=False, show_footer=False, role=None)


# ====================================================================================
# Reset pw
@app.route("/reset-pw", methods=["GET", "POST"])
def reset_pw():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        role = request.form.get("role")
        new_pw = request.form.get("password")
        confirm_pw = request.form.get("confirm_pw")
        
        
        if len(new_pw) < 15:
            flash("Password must be at least 15 characters", "error")
            return redirect("/reset-pw")
        
        if new_pw != confirm_pw:
            flash("Passwords do not match.", "error")
            return redirect("/reset-pw")

        table_map = {
            "doctor": "doctor",
            "nurse" : "nurse",
            "patient": "patient"
        }
            
        table = table_map.get(role)
            
        if not table:
            flash("Invalid role.", "error")
            return redirect("/reset-pw")       

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(f"""
            SELECT * FROM {table}
            WHERE Name = %s AND Email = %s
        """, (name, email))
        user = cursor.fetchone()
        
        if not user:
            flash("User not found.", "error")
            cursor.close()
            conn.close()
            return redirect("/reset-pw")
        
        if user["Password"] is None:
            flash("Account not registered yet. Please sign up first.", "error")
            cursor.close()
            conn.close()
            return redirect("/reset-pw")
        
        hash_pw = generate_password_hash(new_pw)
        cursor.execute(f"""
            UPDATE {table}
                SET Password = %s
                WHERE Name = %s AND Email = %s
            """, (hash_pw, name, email))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash("Password reset successful!", "success")
        return redirect(f"/login?role={role}")
    
    return render_template("reset-pw.html", show_menu=False)

# ====================================================================================
# Sign out
@app.route("/signOut")
def signOut():
    session.clear()
    return redirect("/")   

# ====================================================================================
# Doctor

# Dashboard (DOCTOR)
@app.route("/doctor")
def doctor_dashboard():
    if "user_id" not in session or session.get("role") != "doctor":
        return redirect("/")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT DoctorID, Name, Email, Department FROM Doctor WHERE DoctorID = %s", (session["user_id"],))

    doctor = cursor.fetchone()

    # upcoming appts
    cursor.execute("""
        SELECT a.AppointmentID, a.PatientID, d.Date, d.Time, p.Name
        FROM Appointment a
        JOIN DoctorSlots d ON a.SlotID = d.SlotID
        JOIN Patient p ON a.PatientID = p.PatientID
        WHERE d.DoctorID = %s AND a.AppointmentStatus = 'Upcoming'
        ORDER BY d.Date, d.Time
        LIMIT 5
    """, (session["user_id"],)) 
    upcoming_appointments = cursor.fetchall()
    
    # ready to consult
    cursor.execute("""
        SELECT a.AppointmentID, a.PatientID, d.Date, d.Time, p.Name
        FROM Appointment a
        JOIN DoctorSlots d ON a.SlotID = d.SlotID
        JOIN Patient p ON a.PatientID = p.PatientID
        WHERE d.DoctorID = %s AND a.AppointmentStatus = 'VitalsSaved'
        ORDER BY d.Date, d.Time
        LIMIT 5
    """, (session["user_id"],))
    ready_appointments = cursor.fetchall()

    # Patient list
    cursor.execute("""
        SELECT p.PatientID, p.Name, MAX(a.AppointmentID) AS LatestAppointment
        FROM Patient p
        JOIN Appointment a ON p.PatientID = a.PatientID
        JOIN DoctorSlots d ON a.SlotID = d.SlotID
        WHERE d.DoctorID = %s AND a.AppointmentStatus = 'Completed'
        GROUP BY p.PatientID, p.Name
        ORDER BY LatestAppointment DESC
        LIMIT 5
    """, (session["user_id"],))

    patients = cursor.fetchall()
    
    # Free Slots
    cursor.execute("""
        SELECT SlotID, Date, Time
        FROM DoctorSlots
        WHERE DoctorID = %s
        AND IsBooked = 0
        AND TIMESTAMP(Date, Time) >= NOW()
        ORDER BY Date, Time
    """, (session["user_id"],))

    free_slots = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template("doctor/dashboard.html", show_menu=True, show_footer=True, role="doctor", doctor=doctor, upcoming_appointments=upcoming_appointments, ready_appointments=ready_appointments, patients=patients, free_slots=free_slots)

# =============================================================================

# Personal Info (DOCTOR)

@app.route("/doctor/personal-info", methods=["GET", "POST"])
def doctor_personal_info():
    if "user_id" not in session or session.get("role") != "doctor":
        return redirect("/")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # when nth is changed 
    cursor.execute("""
        SELECT Name, Email, TelNo
        FROM Doctor 
        WHERE DoctorID = %s
    """, (session["user_id"],))
    currentData = cursor.fetchone()

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        tel = request.form.get("phone")
        
        if (name == currentData["Name"] and
            email == currentData["Email"] and
            tel == currentData["TelNo"]):
            
            return redirect("/doctor/personal-info")
        
        # checking duplicate email
        cursor.execute("""
            SELECT Email FROM Doctor WHERE Email = %s
            AND DoctorID != %s
        """, (email, session["user_id"]))
        existing_email = cursor.fetchone()

        if existing_email:
            flash("Email already exists. Please use an alternative one.", "error")
            return redirect("/doctor/personal-info") 

        cursor.execute("""
            UPDATE Doctor
            SET Name = %s, Email = %s, TelNo = %s
            WHERE DoctorID = %s
        """, (name, email, tel, session["user_id"]))
        
        conn.commit()
        flash("Information updated successfully 🎉", "success")      
        return redirect("/doctor/personal-info")

    cursor.execute("SELECT DoctorID, Name, Email, TelNo, Department FROM doctor WHERE DoctorID = %s", (session["user_id"],))

    doctor = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template("doctor/info.html", show_menu=True, show_footer=True, role="doctor", doctor=doctor)


# =============================================================================

# Appointment (DOCTOR)

@app.route("/doctor/appointments", methods=["GET", "POST"])
def doctor_appointments():
    if "user_id" not in session or session.get("role") != "doctor":
        return redirect("/")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # missed appt
    cursor.execute("""
        UPDATE Appointment a 
        JOIN DoctorSlots s ON a.SlotID = s.SlotID
        SET a.AppointmentStatus = 'Missed'
        WHERE a.AppointmentStatus IN ('Upcoming', 'VitalsSaved')
        AND a.DoctorID = %s
        AND TIMESTAMP(s.Date, s.Time) < NOW()
    """, (session["user_id"],))
    conn.commit()

    if request.method == "POST":
        action = request.form.get("action")

        try:
            if action == "book":
                slot_id = request.form.get("slot_id")
                patient_id = request.form.get("patient_id")

                if not re.match(r"^PAT\d{2}$", patient_id):
                    flash("Invalid Patient ID format (Example: PAT01).", "error")
                    return redirect("/doctor/appointments")

                #check patient ID exists
                cursor.execute("SELECT 1 FROM Patient WHERE PatientID = %s",(patient_id,))
                if not cursor.fetchone():
                    flash("Patient ID does not exist 🚫", "error")
                    return redirect("/doctor/appointments")
                
                #get slot
                cursor.execute("""
                    SELECT Date, Time, IsBooked FROM DoctorSlots
                    WHERE SlotID = %s AND DoctorID = %s
                """, (slot_id, session["user_id"]))
                slot = cursor.fetchone()
                
                if not slot:
                    flash("Slot not found 🚫", "error")
                    return redirect("/doctor/appointments")
                
                if slot["IsBooked"] == 1:
                    flash("Slot already booked 🚫", "error")
                    return redirect("/doctor/appointments")
                
                if not valid_slot(slot):
                    flash("Cannot book past slots 🚫", "error")
                    return redirect("/doctor/appointments")
                
                #check if patient has appt on that time                 
                cursor.execute("""
                    SELECT 1 FROM Appointment a
                    JOIN DoctorSlots s ON a.SlotID = s.SlotID
                    WHERE a.PatientId = %s
                    AND a.AppointmentStatus In ('Upcoming', 'VitalsSaved')
                    AND s.Date = %s AND s.Time = %s    
                """, (patient_id, slot["Date"], slot["Time"]))
                if cursor.fetchone():
                    flash("Patient already has an appointment at this time 🚫", "error")
                    return redirect("/doctor/appointments")
                
                # assign nurse randomly
                cursor.execute("""
                    SELECT NurseID FROM Nurse ORDER BY RAND() LIMIT 1
                """)
                nurse = cursor.fetchone()
                nurse_id = nurse["NurseID"]

                # create appt
                cursor.execute("""
                    INSERT INTO Appointment (SlotID, PatientID, DoctorID, NurseID, AppointmentStatus)
                    VALUES (%s, %s, %s, %s, 'Upcoming')
                """, (slot_id, patient_id, session["user_id"], nurse_id))
                
                cursor.execute("""
                    UPDATE DoctorSlots
                    SET IsBooked = 1
                    WHERE SlotID = %s AND DoctorID = %s AND IsBooked = 0
                """, (slot_id, session["user_id"]))
                
                if cursor.rowcount == 0:
                    flash("Slot already booked 🚫", "error")
                    return redirect("/doctor/appointments")

                flash("Appointment booked successfully 🎉", "success")

            elif action == "complete":
                appointment_id = request.form.get("appointment_id")
                diagnosis = request.form.get("diagnosis")
                description = request.form.get("description")
                prescriptions = request.form.get("prescriptions")
                instruction = request.form.get("instruction")
                temperature = request.form.get("temperature")
                blood_pressure = request.form.get("blood_pressure")
                heart_rate = request.form.get("heart_rate")
                
                full_diagnosis = diagnosis
                if description:
                    full_diagnosis += "\n(" + description + ")"
            
                full_prescriptions = prescriptions
                if instruction:
                    full_prescriptions += "\n(" + instruction + ")"

                cursor.execute("""
                    UPDATE Appointment
                    SET Diagnosis = %s,
                        Prescriptions = %s,
                        Temperature = %s,
                        BloodPressure = %s,
                        HeartRate = %s,
                        AppointmentStatus = 'Completed'
                    WHERE AppointmentID = %s
                      AND DoctorID = %s
                """, (
                    full_diagnosis,
                    full_prescriptions,
                    temperature,
                    blood_pressure,
                    heart_rate,
                    appointment_id,
                    session["user_id"]
                ))

                flash("Appointment completed successfully!", "success")

            conn.commit()

        except Exception:
            conn.rollback()
            flash("Something went wrong.", "error")

        cursor.close()
        conn.close()
        return redirect("/doctor/appointments")


    # Upcoming
    cursor.execute("""
        SELECT a.AppointmentID, a.PatientID, p.Name, d.Date, d.Time, d.DoctorID
        FROM Appointment a
        JOIN DoctorSlots d ON a.SlotID = d.SlotID
        JOIN Patient p ON a.PatientID = p.PatientID
        WHERE d.DoctorID = %s AND a.AppointmentStatus = 'Upcoming'
        ORDER BY d.Date, d.Time
    """, (session["user_id"],))
    upcoming = cursor.fetchall()

    grouped_upcoming = defaultdict(list)
    for appt in upcoming:
        grouped_upcoming[appt["Date"]].append(appt)

    #VitalsSaved (Ready to consult)
    cursor.execute("""
        SELECT a.AppointmentID, a.PatientID, p.Name, d.Date, d.Time, d.DoctorId
        FROM Appointment a
        JOIN DoctorSlots d ON a.SlotID = d.SlotID
        JOIN Patient p ON a.PatientID = p.PatientID
        WHERE d.DoctorID = %s AND a.AppointmentStatus = 'VitalsSaved'
        ORDER BY d.Date, d.Time
    """, (session["user_id"],))
    readyToConsult = cursor.fetchall()
    
    grouped_ready = defaultdict(list)
    for ready in readyToConsult:
        grouped_ready[ready["Date"]].append(ready)
    
    # Completed
    cursor.execute("""
        SELECT a.AppointmentID, a.PatientID, p.Name, d.Date, d.Time,
               a.Diagnosis, a.Prescriptions,
               a.Temperature, a.BloodPressure, a.HeartRate
        FROM Appointment a
        JOIN DoctorSlots d ON a.SlotID = d.SlotID
        JOIN Patient p ON a.PatientID = p.PatientID
        WHERE d.DoctorID = %s AND a.AppointmentStatus = 'Completed'
        ORDER BY d.Date DESC, d.Time DESC
    """, (session["user_id"],))
    completed = cursor.fetchall()

    grouped_completed = defaultdict(list)
    for appt in completed:
        grouped_completed[appt["Date"]].append(appt)
        
    # missed 
    cursor.execute("""
        SELECT a.AppointmentID, a.PatientID, p.Name, d.Date, d.Time
        FROM Appointment a
        JOIN DoctorSlots d ON a.SlotID = d.SlotID
        JOIN Patient p ON a.PatientID = p.PatientID
        WHERE d.DoctorID = %s AND a.AppointmentStatus = 'Missed'
        ORDER BY d.Date DESC, d.Time DESC
    """, (session["user_id"],))
    missed = cursor.fetchall()
    
    grouped_missed = defaultdict(list)
    for appt in missed:
        grouped_missed[appt["Date"]].append(appt)

    # Available Slots
    cursor.execute("""
        SELECT SlotID, Date, Time
        FROM DoctorSlots
        WHERE DoctorID = %s 
        AND IsBooked = 0
        AND (Date > CURDATE() OR (Date = CURDATE() AND Time >= CURTIME()))
        ORDER BY Date, Time
    """, (session["user_id"],))
    available_slots = cursor.fetchall()
    
    selected_slot = request.args.get("slot_id")

    cursor.close()
    conn.close()
    
    return render_template(
        "doctor/appointment.html", show_menu=True, show_footer=True, role="doctor",
        grouped_upcoming=grouped_upcoming, grouped_ready=grouped_ready, grouped_completed=grouped_completed,
        grouped_missed=grouped_missed, available_slots=available_slots, selected_slot=selected_slot
    )
   
# =============================================================================

# Slot (DOCTOR)
@app.route("/doctor/slots", methods=["GET", "POST"])
def add_slot():
    if "user_id" not in session or session.get("role") != "doctor":
        return redirect("/")

    try:
        if request.method == "POST":
            date = request.form.get("date")
            time = request.form.get("time")
            
            # validate date and time
            selected_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            if selected_datetime < datetime.now():
                flash("Slot cannot be in the past 🚫", "error")
                return redirect("/doctor/slots")
            
            #working hours 8am-5pm
            start = dt_time(8, 0)
            end = dt_time(17, 0)
            
            if not (start <= selected_datetime.time() <= end):
                flash("Slot must be between 08:00 and 17:00 ⏰", "error")
                return redirect("/doctor/slots")
            
            if selected_datetime.minute % 30 != 0:
                flash("Slots must be every 30 minutes ⏰", "error")
                return redirect("/doctor/slots")

            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                INSERT INTO DoctorSlots (DoctorID, Date, Time)
                VALUES (%s, %s, %s)
            """, (session["user_id"], date, time))

            conn.commit()
            flash("Slot added successfully 🎉", "success")
            
    except mysql.connector.IntegrityError:
        flash("Slot already exists 🚫", "error")
        
        cursor.close()
        conn.close()

        return redirect("/doctor/slots")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT SlotID, Date, Time, IsBooked
        FROM DoctorSlots
        WHERE DoctorID = %s 
        AND IsBooked = 0
        AND (Date > CURDATE() OR (Date = CURDATE() AND Time >= CURTIME()))
        ORDER BY Date, Time
    """, (session["user_id"],))

    slots = cursor.fetchall()
    grouped_slots = defaultdict(list)
    for slot in slots:
        grouped_slots[slot["Date"]].append(slot)
    
    cursor.close()
    conn.close()

    return render_template("doctor/slots.html", show_menu=True, show_footer=True, role="doctor", slots=slots, grouped_slots=grouped_slots)

# =============================================================================

# update slot
@app.route("/doctor/update-slot", methods=["POST"])
def update_slot():
    if "user_id" not in session or session.get("role") != "doctor":
        return redirect("/")
    
    slot_id = request.form.get("slot_id")
    date = request.form.get("date")
    time = request.form.get("time")
    action = request.form.get("action")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    try:
        if action == "edit":
            if not date or not time:
                flash("Date and time required 🚫", "error")
                return redirect("/doctor/slots")
            
            # validate date and time
            selected_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            if selected_datetime < datetime.now():
                flash("Slot cannot be in the past 🚫", "error")
                return redirect("/doctor/slots")
            
            #working hours 8am-5pm
            start = dt_time(8, 0)
            end = dt_time(17, 0)
            
            if not (start <= selected_datetime.time() <= end):
                flash("Slot must be between 08:00 and 17:00 ⏰", "error")
                return redirect("/doctor/slots")

            if selected_datetime.minute % 30 != 0:
                flash("Slots must be every 30 minutes ⏰", "error")
                return redirect("/doctor/slots")

            cursor.execute("""
                UPDATE DoctorSlots
                SET Date=%s, Time=%s
                WHERE SlotID=%s
            """, (date, time, slot_id))   
            flash("Slot updated successfully 🎉", "success")
       
        elif action == "delete":
            cursor.execute("""
                DELETE FROM DoctorSlots
                WHERE SlotID = %s AND DoctorID = %s AND IsBooked = 0
            """, (slot_id, session["user_id"]))
            
            flash("Slot deleted successfully 🗑️", "success")
            
        else:
            flash("Invalid action 🚫", "error")
            return redirect("/doctor/slots")
        conn.commit()
    
    except Exception as e:
        print("Error updating slot:", e)
        conn.rollback()
        flash("Something went wrong 🚫", "error")

    finally:
        cursor.close()
        conn.close()

    return redirect("/doctor/slots")

# =============================================================================

# Patient Record (DOCTOR)
@app.route("/doctor/patient-records", methods=["GET", "POST"])
def doctor_patient_records():
    if "user_id" not in session or session.get("role") != "doctor":
        return redirect("/")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.PatientID, p.Name, a.AppointmentID, a.Diagnosis, a.Prescriptions
        FROM Patient p
        JOIN Appointment a ON p.PatientID = a.PatientID
        WHERE a.DoctorID = %s AND a.AppointmentStatus = 'Completed'
        ORDER BY a.AppointmentID 
    """, (session["user_id"],))

    patient_records = cursor.fetchall()

    cursor.close()
    conn.close()
    
    if request.method == "POST":
        appointmentID = request.form.get("appointment_id")
        diagnosis = request.form.get("diagnosis")
        prescriptions = request.form.get("prescriptions")

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            UPDATE Appointment
            SET Diagnosis = %s, Prescriptions = %s,
                AppointmentStatus = 'Completed'
            WHERE AppointmentID = %s AND DoctorID = %s
        """, (diagnosis, prescriptions, appointmentID, session["user_id"]))

        conn.commit()
        cursor.close()
        conn.close()
        
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT p.PatientID, p.Name, a.AppointmentID
        FROM Patient p
        JOIN Appointment a ON p.PatientID = a.PatientID
        WHERE a.DoctorID = %s AND a.AppointmentStatus = 'Upcoming'
    """, (session["user_id"],))
    
    upcoming_patients = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template("doctor/patient-records.html", show_menu=True, show_footer=True, role="doctor", patient_records=patient_records, upcoming_patients=upcoming_patients)



# =============================================================================
# Nurse

    
# Dashboard (Nurse)
@app.route("/nurse")
def nurse_dashboard():
    if "user_id" not in session or session.get("role") != "nurse":
        return redirect("/")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT NurseID, Name, Email, Ward FROM nurse WHERE NurseID = %s", (session["user_id"],))
    nurse = cursor.fetchone()
    
    # assigned ward
    ward = nurse["Ward"] if nurse else "N/A"
    
    # upcoming appts to record vitals
    cursor.execute("""
        SELECT a.AppointmentID, a.PatientID, d.Date, d.Time, p.Name
        FROM Appointment a
        JOIN DoctorSlots d ON a.SlotID = d.SlotID
        JOIN Patient p ON a.PatientID = p.PatientID
        JOIN Nurse n ON a.NurseID = n.NurseID
        WHERE n.NurseID = %s AND a.AppointmentStatus = 'Upcoming'
        AND a.Temperature IS NULL
        AND a.BloodPressure IS NULL
        AND a.HeartRate IS NULL
        ORDER BY d.Date, d.Time
        LIMIT 5
    """, (session["user_id"],)) 
    upcoming_appointments = cursor.fetchall()
    
    # total patients
    cursor.execute("""
        SELECT PatientID FROM Patient
    """)
    patients = cursor.fetchall()
    
    # assigned patients
    cursor.execute("""
        SELECT p.PatientID, p.Name FROM Patient p
        JOIN appointment a ON p.PatientID = a.PatientID
        WHERE NurseID = %s
    """, (session["user_id"],))
    assigned_patients = cursor.fetchall()
    
    # assigned ward buddies
    cursor.execute("""
        SELECT Name FROM Nurse
        WHERE Ward=%s AND NurseID != %s
    """, (ward, session["user_id"]))
    ward_buddies = cursor.fetchall()
    
    
    cursor.close()
    conn.close()
    
    return render_template("nurse/dashboard.html", show_menu=True, show_footer=True, role="nurse", nurse=nurse, ward=ward, upcoming_appointments=upcoming_appointments, patients=patients, assigned_patients=assigned_patients, ward_buddies=ward_buddies)

# =============================================================================

# Personal Info (Nurse)

@app.route("/nurse/personal-info", methods=["GET", "POST"])
def nurse_personal_info():
    if "user_id" not in session or session.get("role") != "nurse":
        return redirect("/")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # when nth is changed 
    cursor.execute("""
        SELECT Name, Email, TelNo
        FROM Nurse 
        WHERE NurseID = %s
    """, (session["user_id"],))
    currentData = cursor.fetchone()

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        tel = request.form.get("phone")
        
        if (name == currentData["Name"] and
            email == currentData["Email"] and
            tel == currentData["TelNo"]):
            
            return redirect("/nurse/personal-info")
        
        # checking duplicate email
        cursor.execute("""
            SELECT Email FROM Nurse WHERE Email = %s
            AND NurseID != %s
        """, (email, session["user_id"]))
        existing_email = cursor.fetchone()

        if existing_email:
            flash("Email already exists. Please use an alternative one.", "error")
            return redirect("/nurse/personal-info") 
        
        cursor.execute("""
            UPDATE nurse
            SET Name = %s, Email = %s, TelNo = %s
            WHERE NurseID = %s
        """, (name, email, tel, session["user_id"]))
        
        conn.commit()
        flash("Information updated successfully 🎉", "success")      
        return redirect("/nurse/personal-info")

    cursor.execute("SELECT NurseID, Name, Email, TelNo, Ward FROM nurse WHERE NurseID = %s", (session["user_id"],))
    nurse = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template("nurse/info.html", show_menu=True, show_footer=True, role="nurse", nurse=nurse)

# =============================================================================

# Upcoming Appt (Nurse)
@app.route("/nurse/upcoming-appt")
def nurse_upcoming_appt():
    if "user_id" not in session or session.get("role") != "nurse":
        return redirect("/")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    #upcoming appt
    cursor.execute("""
        SELECT a.AppointmentID, s.Date, s.Time, d.DoctorID, d.Name AS DoctorName,
        p.PatientID, p.Name AS PatientName, n.Name AS NurseName
        FROM Appointment a
        JOIN Doctor d ON a.DoctorID = d.DoctorID
        JOIN DoctorSlots s ON a.SlotID = s.SlotID
        JOIN Patient p ON a.PatientID = p.PatientID
        JOIN Nurse n ON a.NurseID = n.NurseID
        WHERE n.NurseID = %s AND a.AppointmentStatus = 'Upcoming'         
    """, (session["user_id"],))    
    upcoming_appt = cursor.fetchall()
    
    grouped_upcoming = defaultdict(list)
    for upcoming in upcoming_appt:
        grouped_upcoming[upcoming["Date"]].append(upcoming)
        
    #missed appt
    cursor.execute("""
        SELECT a.AppointmentID, s.Date, s.Time, d.DoctorID, d.Name AS DoctorName,
        p.PatientID, p.Name AS PatientName, n.Name AS NurseName
        FROM Appointment a
        JOIN Doctor d ON a.DoctorID = d.DoctorID
        JOIN DoctorSlots s ON a.SlotID = s.SlotID
        JOIN Patient p ON a.PatientID = p.PatientID
        JOIN Nurse n ON a.NurseID = n.NurseID
        WHERE n.NurseID = %s AND a.AppointmentStatus = 'Missed'         
    """, (session["user_id"],))    
    missed_appt = cursor.fetchall()
    
    grouped_missed = defaultdict(list)
    for missed in missed_appt:
        grouped_missed[missed["Date"]].append(missed)
    
    cursor.execute("SELECT * FROM Patient ORDER BY PatientID")
    patients = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("nurse/upcoming-appt.html", show_menu=True, show_footer=True, role="nurse", 
                           upcoming_appt=upcoming_appt, grouped_upcoming=grouped_upcoming, 
                           missed_appt=missed_appt, grouped_missed=grouped_missed, 
                           patients=patients)
    

# =============================================================================

# Patient List (Nurse)
@app.route("/nurse/patient", methods=["GET", "POST"])
def nurse_view_patient():
    if "user_id" not in session or session.get("role") != "nurse":
        return redirect("/")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    generated_username = None
    generated_pw = None
    preview = False
    new_id = None

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        telNo = request.form.get("telNo")
        username = request.form.get("username")
        pw = request.form.get("temp_pw")

        # checking duplicate email
        cursor.execute("SELECT Email FROM Patient WHERE Email = %s", (email,))
        existing_email = cursor.fetchone()

        if existing_email:
            flash("Email already exists. Please use an alternative one.", "error")
            return redirect("/nurse/patient")    


        # adding patient
        if request.form.get("confirm") == "yes":

            patient_id = request.form.get("patient_id")
            
            cursor.execute("""
                INSERT INTO Patient (PatientID, Name, Email, TelNo, Username, Password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                patient_id, name, email, telNo, username, generate_password_hash(pw)
            ))

            conn.commit()

            flash("Patient added successfully!", "success")
            return redirect("/nurse/patient") 
        
        else:
            # create new id
            cursor.execute("SELECT PatientID FROM Patient ORDER BY PatientID DESC LIMIT 1")
            last_patient = cursor.fetchone()

            if last_patient:
                lastId = last_patient["PatientID"]
                new_num = int(lastId[3:]) + 1
            else:
                new_num = 1

            new_id = f"PAT{new_num:02d}"

            generated_username = new_id
            generated_pw = generate_pw()
            preview = True

    # GET request OR after redirect
    cursor.execute("SELECT PatientID FROM Patient ORDER BY PatientID DESC LIMIT 1")
    last_patient = cursor.fetchone()

    if last_patient:
        lastId = last_patient["PatientID"]
        new_num = int(lastId[3:]) + 1
    else:
        new_num = 1

    new_id = f"PAT{new_num:02d}"

    cursor.execute("SELECT * FROM Patient ORDER BY PatientID")
    patients = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("nurse/patient.html", show_menu=True, show_footer=True, role="nurse", 
                           patients=patients, new_id=new_id, generated_username=generated_username, generated_pw=generated_pw, 
                           preview=preview
    )
    
# =============================================================================

# Add Vitals (Nurse)
@app.route("/nurse/add-vitals", methods=["GET", "POST"])
def nurse_vitals():
    if "user_id" not in session or session.get("role") != "nurse":
        return redirect("/")
    
    appt_id = request.args.get("appt_id")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Get Appointment and patient details
    if request.method == "GET":

        cursor.execute("""
            SELECT a.AppointmentID, a.PatientID,
            s.Date, s.Time, p.PatientID, 
            p.Name AS PatientName, 
            d.DoctorID, d.Name AS DoctorName
            FROM Appointment a
            JOIN DoctorSlots s ON a.SlotID = s.SlotID
            JOIN Patient p ON a.PatientID = p.PatientID
            JOIN Doctor d ON a.DoctorID = d.DoctorID
            WHERE a.AppointmentID = %s
        """, (appt_id,))
        
        appointment = cursor.fetchone()
        
        if not appt_id:
            flash("Invalid appointment.", "error")
            return redirect("/nurse/upcoming-appt")
        
        cursor.close()
        conn.close()
        
        return render_template("nurse/add-vitals.html", show_menu=True, show_footer=True, role="nurse", appointment=appointment)
        
    # Save vitals
    if request.method == "POST":
        temp = request.form.get("temperature")
        bp = request.form.get("blood_pressure")
        heart_rate = request.form.get("heart_rate")
        appointment_id = request.form.get("appt_id")
        
        cursor.execute("""
            UPDATE Appointment
            SET Temperature = %s,
            BloodPressure = %s, HeartRate = %s,
            AppointmentStatus = 'VitalsSaved'
            WHERE AppointmentID = %s
        """, (temp, bp, heart_rate, appointment_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash("Vitals added successfully!", "success")
        return redirect("/nurse/upcoming-appt")
    
# =============================================================================
# Patient

# Dashboard (Patient)
@app.route("/patient")
def patient_dashboard():
    if "user_id" not in session or session.get("role") != "patient":
        return redirect("/")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # profile info
    cursor.execute("SELECT PatientID, Name, Email FROM patient WHERE PatientID = %s", (session["user_id"],))

    patient = cursor.fetchone()
    
    # patient's upcoming appt
    cursor.execute("""
        SELECT a.AppointmentID, s.Date, s.Time,
        d.Name AS DoctorName, n.Name AS NurseName
        FROM Appointment a 
        JOIN DoctorSlots s ON a.SlotID = s.SlotID
        JOIN Doctor d ON a.DoctorID = d.DoctorID
        JOIN Nurse n ON a.NurseID = n.NurseID
        WHERE a.PatientID = %s AND a.AppointmentStatus != 'Completed' AND a.AppointmentStatus != 'Missed'
    """,(session["user_id"],))
    
    upcoming_appointments = cursor.fetchall()
    
    # medical record
    cursor.execute("""
        SELECT a.AppointmentID, s.Date, d.Name, a.Diagnosis, a.Prescriptions, a.Temperature, a.BloodPressure, a.HeartRate
        FROM Appointment a 
        JOIN Doctor d ON a.DoctorID = d.DoctorID
        JOIN DoctorSlots s ON a.SlotID = s.SlotID
        WHERE a.PatientID = %s AND a.AppointmentStatus = 'Completed'
    """, (session["user_id"],))
    
    records = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template("patient/dashboard.html", show_menu=True, show_footer=True, role="patient", patient=patient, upcoming_appointments=upcoming_appointments, records=records)

# =============================================================================

# Medical Records (Patient)
@app.route("/patient/medical_records")
def medical_records():
    if "user_id" not in session or session.get("role") != "patient":
        return redirect("/")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT a.AppointmentID, s.Date, d.DoctorID, d.Name, a.Diagnosis, a.Prescriptions, a.Temperature, a.BloodPressure, a.HeartRate
        FROM Appointment a 
        JOIN Doctor d ON a.DoctorID = d.DoctorID
        JOIN DoctorSlots s ON a.SlotID = s.SlotID
        WHERE a.PatientID = %s AND a.AppointmentStatus = 'Completed'
    """, (session["user_id"],))
    
    records = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("patient/medical-records.html",show_menu=True, show_footer=True, role="patient", records=records)

# =============================================================================

# Appointment (Patient)
@app.route("/patient/appointments", methods=["GET", "POST"])
def patient_appointments():
    if "user_id" not in session or session.get("role") != "patient":
        return redirect("/")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Patient's upcoming Appt
    cursor.execute("""
        SELECT a.AppointmentID, s.Date, s.Time, d.DoctorID, d.Name AS DoctorName, a.NurseID, n.Name AS NurseName
        FROM Appointment a
        JOIN Doctor d ON a.DoctorID = d.DoctorID
        JOIN Nurse n ON a.NurseID = n.NurseID
        JOIN DoctorSlots s ON a.SlotID = s.SlotID
        WHERE a.PatientID = %s AND a.AppointmentStatus != "Completed" AND a.AppointmentStatus != "Missed"
        
    """, (session["user_id"],))
    
    upcoming_appt = cursor.fetchall()
    grouped_upcoming = defaultdict(list)
    for upcoming in upcoming_appt:
        grouped_upcoming[upcoming["Date"]].append(upcoming)
    
    #missed appt
    cursor.execute("""
        SELECT a.AppointmentID, s.Date, s.Time, d.DoctorID, d.Name AS DoctorName, a.NurseID, n.Name AS NurseName
        FROM Appointment a
        JOIN Doctor d ON a.DoctorID = d.DoctorID
        JOIN Nurse n ON a.NurseID = n.NurseID
        JOIN DoctorSlots s ON a.SlotID = s.SlotID
        WHERE a.PatientID = %s AND a.AppointmentStatus = 'Missed'         
        
    """, (session["user_id"],))    
    missed_appt = cursor.fetchall()
    
    grouped_missed = defaultdict(list)
    for missed in missed_appt:
        grouped_missed[missed["Date"]].append(missed)
        
    # Departments
    cursor.execute("SELECT DISTINCT Department FROM Doctor")
    departments = cursor.fetchall()
    
    # Chosen department
    chosen_department = request.args.get("department")
    
    doctors=[]
    if chosen_department:
        cursor.execute("""
            SELECT DoctorID, Name 
            FROM Doctor 
            WHERE Department = %s
    """, (chosen_department,))
        doctors = cursor.fetchall()
        
    #slots of chosen doctor
    chosen_doctor = request.args.get("doctor")
    chosen_doctor_name = None
    
    slots=[]
    if chosen_doctor:
        cursor.execute("""
            SELECT SlotID, Date, Time
            FROM DoctorSlots
            WHERE DoctorID = %s AND IsBooked = 0
            AND (Date > CURDATE() OR (Date = CURDATE() AND Time >= CURTIME()))
            ORDER BY Date, Time
        """, (chosen_doctor,))
        slots = cursor.fetchall()
    
    if chosen_doctor:
        cursor.execute("""
            SELECT Name FROM Doctor WHERE DoctorID = %s
    """, (chosen_doctor,))
        doctor_name = cursor.fetchone()
        if doctor_name:
            chosen_doctor_name = doctor_name["Name"]
    
    slots_gp = {}
    for slot in slots:
        date = slot["Date"]
        if date not in slots_gp:
            slots_gp[date] = []
        
        slots_gp[date].append(slot)
        
    # book appt
    if request.method == "POST":
        slot_id = request.form.get("slotId")
        doctor_id = request.form.get("doctorId")
        patient_id = session["user_id"]
        
        cursor.execute("""
            SELECT Date, Time, IsBooked FROM DoctorSlots WHERE SlotID = %s               
        """, (slot_id,))
        slot = cursor.fetchone()
        
        if not slot:
            flash("Slot not found 🚫", "error")
            return redirect("/patient/appointments")
        
        if slot["IsBooked"] == 1:
            flash("Slot already booked 🚫", "error")
            return redirect("/patient/appointments")
        
        if not valid_slot(slot):
            flash("Cannot book past slots 🚫", "error")
            return redirect("/patient/appointments")
        
        
        # restrict booking same-day appt
        cursor.execute("""
            SELECT a.AppointmentID
            FROM Appointment a 
            JOIN DoctorSlots s ON a.SlotID = s.SlotID
            WHERE a.PatientID = %s 
            AND a.AppointmentStatus != 'Completed' 
            AND s.Date = %s 
        """, (patient_id, slot["Date"]))
        
        sameday_appt = cursor.fetchone()
        
        if sameday_appt:
            flash("Same-day appointment is not allowed.", "error")
            return redirect("/patient/appointments")
        
        # assigning nurse randomly
        cursor.execute("""
            SELECT NurseID, Name FROM Nurse 
            ORDER BY RAND()
            LIMIT 1
        """)
        nurse = cursor.fetchone()
        nurse_id = nurse["NurseID"]
        
        # create appt
        cursor.execute("""
            INSERT INTO Appointment (DoctorID, PatientID, NurseID, SlotID, AppointmentStatus)
            VALUES (%s, %s, %s, %s, 'Upcoming')
        """, (doctor_id, patient_id, nurse_id, slot_id))
      
        # update slot is booked
        cursor.execute("""
            UPDATE DoctorSlots
            SET IsBooked = 1
            WHERE SlotID = %s AND IsBooked = 0
        """, (slot_id,))
        
        if cursor.rowcount == 0:
            flash("Slot already booked 🚫", "error")
            return redirect("/patient/appointments")
        
        conn.commit()
        flash("Appointment booked successfully🎉", "success")
        return redirect("/patient/appointments")
        
    cursor.close()
    conn.close()
    
    return render_template("patient/appointments.html", show_menu=True, show_footer=True, role="patient", 
                           upcoming_appt=upcoming_appt, grouped_upcoming=grouped_upcoming, missed_appt=missed_appt,
                           grouped_missed=grouped_missed, departments=departments, doctors=doctors, 
                           chosen_department=chosen_department, slots_gp=slots_gp,
                           chosen_doctor=chosen_doctor, chosen_doctor_name=chosen_doctor_name)


# =============================================================================

# Personal Info (Patient)

@app.route("/patient/personal-info", methods=["GET", "POST"])
def patient_personal_info():
    if "user_id" not in session or session.get("role") != "patient":
        return redirect("/")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # when nth is changed 
    cursor.execute("""
        SELECT Name, Email, TelNo
        FROM Patient 
        WHERE PatientID = %s
    """, (session["user_id"],))
    currentData = cursor.fetchone()

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        tel = request.form.get("phone")
        
        if (name == currentData["Name"] and
            email == currentData["Email"] and
            tel == currentData["TelNo"]):
            
            return redirect("/patient/personal-info")
        
        # checking duplicate email
        cursor.execute("""
            SELECT Email FROM Patient WHERE Email = %s
            AND PatientID != %s
        """, (email, session["user_id"]))
        existing_email = cursor.fetchone()

        if existing_email:
            flash("Email already exists. Please use an alternative one.", "error")
            return redirect("/patient/personal-info") 
        
        cursor.execute("""
            UPDATE patient
            SET Name = %s, Email = %s, TelNo = %s
            WHERE PatientID = %s
        """, (name, email, tel, session["user_id"]))
        conn.commit()
        
        flash("Information updated successfully 🎉", "success")
        
        return redirect("/patient/personal-info")

    cursor.execute("SELECT PatientID, Name, Email, TelNo FROM patient WHERE PatientID = %s", (session["user_id"],))

    patient = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return render_template("patient/info.html", show_menu=True, show_footer=True, role="patient", patient=patient)



if __name__ == "__main__":
    app.run(debug=True)
