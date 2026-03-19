from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import json
import random
import string
import qrcode
import qrcode.image.svg
import io
import base64
import hashlib
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'biometric_secure_key_2024'

# ─────────────────────────────────────────────
# In-memory databases (simulates MySQL tables)
# ─────────────────────────────────────────────
DOCTORS = {
    'DR001': {'name': 'Dr. Arjun Sharma', 'password': 'doctor123', 'specialty': 'General Physician', 'hospital': 'Apollo Medical Center'},
    'DR002': {'name': 'Dr. Priya Nair', 'password': 'doctor123', 'specialty': 'Cardiologist', 'hospital': 'City Heart Hospital'},
    'DR003': {'name': 'Dr. Ravi Kumar', 'password': 'doctor123', 'specialty': 'Neurologist', 'hospital': 'NeuroLife Hospital'},
}

PHARMACISTS = {
    'PH001': {'name': 'MedPlus Pharmacy', 'password': 'pharma123', 'location': 'Koramangala, Bangalore'},
    'PH002': {'name': 'Apollo Pharmacy', 'password': 'pharma123', 'location': 'MG Road, Bangalore'},
}

PATIENTS = {}
PRESCRIPTIONS = {}
PRESCRIPTION_LOGS = []

# Sample pre-loaded patients
PATIENTS['PAT-2024-0001'] = {
    'id': 'PAT-2024-0001', 'name': 'Rahul Verma', 'age': 34, 'gender': 'Male',
    'phone': '9876543210', 'blood_group': 'O+', 'address': 'Koramangala, Bangalore',
    'registered_by': 'DR001', 'registered_on': '2024-01-15'
}
PATIENTS['PAT-2024-0002'] = {
    'id': 'PAT-2024-0002', 'name': 'Deepa Menon', 'age': 45, 'gender': 'Female',
    'phone': '8765432109', 'blood_group': 'A+', 'address': 'Indiranagar, Bangalore',
    'registered_by': 'DR002', 'registered_on': '2024-01-20'
}

# Sample pre-loaded prescriptions
PRESCRIPTIONS['RX-20240101-001'] = {
    'rx_id': 'RX-20240101-001', 'doctor_id': 'DR001', 'doctor_name': 'Dr. Arjun Sharma',
    'patient_id': 'PAT-2024-0001', 'patient_name': 'Rahul Verma',
    'medicines': [{'name': 'Amoxicillin', 'dosage': '500mg', 'frequency': 'Twice daily', 'duration': '7 days'}],
    'notes': 'Take after meals. Avoid alcohol.', 'created_on': '2024-01-15 10:30:00',
    'status': 'Active', 'issued_by': None, 'issued_on': None
}

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def generate_patient_id():
    year = datetime.now().year
    existing = [int(k.split('-')[-1]) for k in PATIENTS.keys() if k.startswith(f'PAT-{year}-')]
    next_num = (max(existing) + 1) if existing else 1
    return f"PAT-{year}-{next_num:04d}"

def generate_rx_id():
    date_str = datetime.now().strftime('%Y%m%d')
    existing = [k for k in PRESCRIPTIONS.keys() if k.startswith(f'RX-{date_str}-')]
    next_num = len(existing) + 1
    return f"RX-{date_str}-{next_num:03d}"

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=6, border=3,
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(json.dumps(data))
    qr.make(fit=True)
    img = qr.make_image(fill_color='#0d47a1', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def login_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if role not in session:
                flash(f'Please login as {role} first.', 'warning')
                return redirect(url_for(f'{role}_login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ─────────────────────────────────────────────
# Routes — Public
# ─────────────────────────────────────────────
@app.route('/')
def home():
    stats = {
        'doctors': len(DOCTORS),
        'patients': len(PATIENTS),
        'prescriptions': len(PRESCRIPTIONS),
        'pharmacies': len(PHARMACISTS),
    }
    return render_template('home.html', stats=stats)

# ─────────────────────────────────────────────
# Doctor Module
# ─────────────────────────────────────────────
@app.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        doc_id = request.form.get('doctor_id', '').strip()
        password = request.form.get('password', '').strip()
        biometric = request.form.get('biometric_verified') == 'true'
        if doc_id in DOCTORS and DOCTORS[doc_id]['password'] == password and biometric:
            session['doctor'] = doc_id
            session['doctor_name'] = DOCTORS[doc_id]['name']
            flash('Biometric login successful!', 'success')
            return redirect(url_for('doctor_dashboard'))
        flash('Invalid credentials or biometric verification failed.', 'danger')
    return render_template('doctor_login.html')

@app.route('/doctor/logout')
def doctor_logout():
    session.pop('doctor', None)
    session.pop('doctor_name', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/doctor/dashboard')
@login_required('doctor')
def doctor_dashboard():
    doc_id = session['doctor']
    my_patients = [p for p in PATIENTS.values() if p.get('registered_by') == doc_id]
    my_rxs = [r for r in PRESCRIPTIONS.values() if r.get('doctor_id') == doc_id]
    return render_template('doctor_dashboard.html', doctor=DOCTORS[doc_id],
                           patients=my_patients, prescriptions=my_rxs)

@app.route('/doctor/register-patient', methods=['GET', 'POST'])
@login_required('doctor')
def register_patient():
    if request.method == 'POST':
        pid = generate_patient_id()
        PATIENTS[pid] = {
            'id': pid,
            'name': request.form['name'],
            'age': request.form['age'],
            'gender': request.form['gender'],
            'phone': request.form['phone'],
            'blood_group': request.form.get('blood_group', 'Unknown'),
            'address': request.form.get('address', ''),
            'registered_by': session['doctor'],
            'registered_on': datetime.now().strftime('%Y-%m-%d'),
        }
        flash(f'Patient registered successfully! Patient ID: {pid}', 'success')
        return redirect(url_for('patient_profile', pid=pid))
    return render_template('register_patient.html')

@app.route('/doctor/patient/<pid>')
@login_required('doctor')
def patient_profile(pid):
    patient = PATIENTS.get(pid)
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('doctor_dashboard'))
    rxs = [r for r in PRESCRIPTIONS.values() if r['patient_id'] == pid]
    return render_template('patient_profile.html', patient=patient, prescriptions=rxs)

@app.route('/doctor/create-prescription', methods=['GET', 'POST'])
@login_required('doctor')
def create_prescription():
    doc_id = session['doctor']
    my_patients = {k: v for k, v in PATIENTS.items() if v.get('registered_by') == doc_id}
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        patient = PATIENTS.get(patient_id)
        if not patient:
            flash('Patient not found.', 'danger')
            return redirect(url_for('create_prescription'))

        medicines = []
        med_names = request.form.getlist('med_name[]')
        med_dosages = request.form.getlist('med_dosage[]')
        med_freqs = request.form.getlist('med_freq[]')
        med_durs = request.form.getlist('med_dur[]')
        for i in range(len(med_names)):
            if med_names[i].strip():
                medicines.append({'name': med_names[i], 'dosage': med_dosages[i],
                                  'frequency': med_freqs[i], 'duration': med_durs[i]})

        rx_id = generate_rx_id()
        rx_data = {
            'rx_id': rx_id,
            'doctor_id': doc_id,
            'doctor_name': DOCTORS[doc_id]['name'],
            'hospital': DOCTORS[doc_id]['hospital'],
            'patient_id': patient_id,
            'patient_name': patient['name'],
            'patient_age': patient['age'],
            'patient_phone': patient['phone'],
            'medicines': medicines,
            'notes': request.form.get('notes', ''),
            'created_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Active',
            'issued_by': None,
            'issued_on': None,
        }
        PRESCRIPTIONS[rx_id] = rx_data

        qr_payload = {'rx_id': rx_id, 'patient_id': patient_id,
                      'doctor': DOCTORS[doc_id]['name'], 'patient': patient['name']}
        qr_b64 = generate_qr_code(qr_payload)
        session['last_qr'] = qr_b64
        session['last_rx_id'] = rx_id
        return redirect(url_for('qr_display', rx_id=rx_id))
    return render_template('create_prescription.html', patients=my_patients)

@app.route('/prescription/qr/<rx_id>')
def qr_display(rx_id):
    rx = PRESCRIPTIONS.get(rx_id)
    if not rx:
        flash('Prescription not found.', 'danger')
        return redirect(url_for('home'))
    qr_b64 = session.get('last_qr')
    if not qr_b64:
        qr_b64 = generate_qr_code({'rx_id': rx_id, 'patient_id': rx['patient_id'],
                                    'doctor': rx['doctor_name'], 'patient': rx['patient_name']})
    return render_template('qr_display.html', rx=rx, qr_b64=qr_b64)

# ─────────────────────────────────────────────
# Pharmacy Module
# ─────────────────────────────────────────────
@app.route('/pharmacy/login', methods=['GET', 'POST'])
def pharmacy_login():
    if request.method == 'POST':
        ph_id = request.form.get('pharmacy_id', '').strip()
        password = request.form.get('password', '').strip()
        if ph_id in PHARMACISTS and PHARMACISTS[ph_id]['password'] == password:
            session['pharmacy'] = ph_id
            session['pharmacy_name'] = PHARMACISTS[ph_id]['name']
            flash('Pharmacy login successful!', 'success')
            return redirect(url_for('pharmacy_dashboard'))
        flash('Invalid pharmacy credentials.', 'danger')
    return render_template('pharmacy_login.html')

@app.route('/pharmacy/logout')
def pharmacy_logout():
    session.pop('pharmacy', None)
    session.pop('pharmacy_name', None)
    return redirect(url_for('home'))

@app.route('/pharmacy/dashboard')
@login_required('pharmacy')
def pharmacy_dashboard():
    ph_id = session['pharmacy']
    issued = [r for r in PRESCRIPTIONS.values() if r.get('issued_by') == ph_id]
    return render_template('pharmacy_dashboard.html', pharmacy=PHARMACISTS[ph_id], issued=issued)

@app.route('/pharmacy/verify', methods=['GET', 'POST'])
@login_required('pharmacy')
def pharmacy_verify():
    rx = None
    if request.method == 'POST':
        rx_id = request.form.get('rx_id', '').strip()
        rx = PRESCRIPTIONS.get(rx_id)
        if not rx:
            flash('Prescription not found. Please check the ID.', 'danger')
        elif rx.get('status') == 'Issued':
            flash('This prescription has already been dispensed.', 'warning')
            rx = None
    return render_template('pharmacy_verify.html', rx=rx)

@app.route('/pharmacy/patient-verify/<rx_id>', methods=['GET', 'POST'])
@login_required('pharmacy')
def patient_verify(rx_id):
    rx = PRESCRIPTIONS.get(rx_id)
    if not rx:
        flash('Prescription not found.', 'danger')
        return redirect(url_for('pharmacy_verify'))
    patient = PATIENTS.get(rx['patient_id'])
    otp = session.get(f'otp_{rx_id}')
    if request.method == 'POST':
        method = request.form.get('method')
        verified = False
        if method == 'fingerprint':
            verified = request.form.get('fingerprint_ok') == 'true'
        elif method == 'patient_id':
            verified = request.form.get('patient_id_input', '').strip() == rx['patient_id']
        elif method == 'otp':
            entered = request.form.get('otp_input', '').strip()
            verified = (otp is not None and entered == otp)
        if verified:
            return redirect(url_for('issue_medicine', rx_id=rx_id))
        flash('Verification failed. Please try again.', 'danger')
    return render_template('patient_verify.html', rx=rx, patient=patient)

@app.route('/pharmacy/generate-otp/<rx_id>')
@login_required('pharmacy')
def generate_otp_route(rx_id):
    rx = PRESCRIPTIONS.get(rx_id)
    if not rx:
        return jsonify({'error': 'Prescription not found'}), 404
    otp = generate_otp()
    session[f'otp_{rx_id}'] = otp
    patient = PATIENTS.get(rx['patient_id'])
    phone = patient['phone'] if patient else 'N/A'
    return jsonify({'otp': otp, 'phone': phone,
                    'message': f'OTP sent to {phone[-4:].rjust(len(phone), "*")}'})

@app.route('/pharmacy/issue/<rx_id>', methods=['GET', 'POST'])
@login_required('pharmacy')
def issue_medicine(rx_id):
    rx = PRESCRIPTIONS.get(rx_id)
    if not rx:
        flash('Prescription not found.', 'danger')
        return redirect(url_for('pharmacy_verify'))
    if request.method == 'POST':
        rx['status'] = 'Issued'
        rx['issued_by'] = session['pharmacy']
        rx['issued_pharmacy'] = PHARMACISTS[session['pharmacy']]['name']
        rx['issued_on'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        PRESCRIPTION_LOGS.append({
            'rx_id': rx_id, 'pharmacy': rx['issued_pharmacy'],
            'issued_on': rx['issued_on'], 'patient': rx['patient_name']
        })
        return redirect(url_for('issue_confirmation', rx_id=rx_id))
    return render_template('issue_medicine.html', rx=rx, pharmacy=PHARMACISTS[session['pharmacy']])

@app.route('/pharmacy/confirmation/<rx_id>')
@login_required('pharmacy')
def issue_confirmation(rx_id):
    rx = PRESCRIPTIONS.get(rx_id)
    if not rx:
        return redirect(url_for('pharmacy_dashboard'))
    return render_template('issue_confirmation.html', rx=rx)

# ─────────────────────────────────────────────
# Admin Module
# ─────────────────────────────────────────────
@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html',
                           prescriptions=PRESCRIPTIONS,
                           patients=PATIENTS,
                           doctors=DOCTORS,
                           logs=PRESCRIPTION_LOGS)

# ─────────────────────────────────────────────
# API
# ─────────────────────────────────────────────
@app.route('/api/prescription/<rx_id>')
def api_prescription(rx_id):
    rx = PRESCRIPTIONS.get(rx_id)
    if rx:
        return jsonify(rx)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/patients')
def api_patients():
    return jsonify(list(PATIENTS.values()))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
