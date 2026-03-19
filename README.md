# AI-Based-Medical-Prescription-Authentication-Using-Signature-Verification
AI Based Medical Prescription Authentication Using Signature Verification
# 🏥 AI-Powered Biometric Secure Prescription Verification System

> A Flask-based web application that digitizes and secures the prescription workflow between **Doctors**, **Pharmacies**, and **Patients** using biometric login simulation, QR code generation, and multi-factor patient identity verification.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Demo Credentials](#demo-credentials)
- [Application Modules](#application-modules)
  - [Doctor Module](#-doctor-module)
  - [Pharmacy Module](#-pharmacy-module)
  - [Admin Module](#-admin-module)
- [API Endpoints](#api-endpoints)
- [Screenshots / Pages](#screenshots--pages)
- [How It Works](#how-it-works)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🔍 Overview

This system addresses the growing problem of **fake or misused medical prescriptions** by providing a secure, end-to-end digital prescription platform. Doctors create verified prescriptions with QR codes, and pharmacies can only dispense medicines after verifying the patient's identity through biometric, OTP, or Patient ID methods.

---

## ✨ Features

- 🔐 **Biometric Login Simulation** for Doctors (fingerprint scan UI)
- 📄 **Digital Prescription Creation** with unique Prescription IDs (e.g., `RX-20240101-001`)
- 📱 **QR Code Generation** for each prescription (encoded with patient & doctor details)
- 🧑‍⚕️ **Patient Registration & Profile Management** by Doctors
- 🔎 **Prescription Verification** by Pharmacies via QR scan or Prescription ID
- ✅ **Multi-Factor Patient Identity Verification**:
  - Fingerprint Simulation
  - Patient ID Input
  - OTP Sent to Registered Phone Number
- 🧾 **Medicine Issuance Confirmation** with audit logs
- 📊 **Admin Dashboard** to view all prescriptions, patients, doctors, and logs
- 🔗 **REST API** for prescription and patient data access

---

## 📁 Project Structure

```
doctor/
│
├── app.py                   # Main Flask application (routes, logic, in-memory DB)
├── requirements.txt         # Python dependencies
│
├── static/
│   └── style.css            # Global stylesheet
│
└── templates/
    ├── base.html            # Base layout (navbar, flash messages, footer)
    ├── home.html            # Landing page with system stats
    ├── admin_dashboard.html # Admin view: all records and logs
    │
    ├── doctor_login.html        # Doctor login with biometric verification
    ├── doctor_dashboard.html    # Doctor's patient & prescription overview
    ├── register_patient.html    # New patient registration form
    ├── patient_profile.html     # Patient detail & prescription history
    ├── create_prescription.html # New prescription form (multi-medicine)
    ├── qr_display.html          # QR code display after prescription creation
    │
    ├── pharmacy_login.html      # Pharmacy login
    ├── pharmacy_dashboard.html  # Pharmacy issued prescriptions overview
    ├── pharmacy_verify.html     # Search & verify prescription by ID
    ├── patient_verify.html      # Patient identity verification (biometric/OTP/ID)
    ├── issue_medicine.html      # Confirm medicine details before issuing
    └── issue_confirmation.html  # Final confirmation receipt after issuance
```

---

## 🛠 Tech Stack

| Layer       | Technology                          |
|-------------|--------------------------------------|
| Backend     | Python 3.x, Flask                   |
| Frontend    | HTML5, CSS3, Vanilla JavaScript     |
| QR Codes    | `qrcode[pil]`, `Pillow`             |
| Data Store  | In-memory Python dictionaries (simulates a database) |
| Sessions    | Flask server-side sessions          |

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+** installed
- `pip` package manager

### Installation

1. **Clone or download** this repository to your local machine.

2. **Navigate** to the project directory:
   ```bash
   cd doctor
   ```

3. **(Recommended)** Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
python app.py
```

The application will start on **`http://127.0.0.1:5000`**.

Open your browser and visit: [http://localhost:5000](http://localhost:5000)

---

## 🔑 Demo Credentials

### 👨‍⚕️ Doctors
> *(Biometric verification must be simulated/clicked on the login page)*

| Doctor ID | Name              | Specialty         | Password    |
|-----------|-------------------|-------------------|-------------|
| `DR001`   | Dr. Arjun Sharma  | General Physician | `doctor123` |
| `DR002`   | Dr. Priya Nair    | Cardiologist      | `doctor123` |
| `DR003`   | Dr. Ravi Kumar    | Neurologist       | `doctor123` |

### 💊 Pharmacies

| Pharmacy ID | Name             | Location                | Password    |
|-------------|------------------|-------------------------|-------------|
| `PH001`     | MedPlus Pharmacy | Koramangala, Bangalore  | `pharma123` |
| `PH002`     | Apollo Pharmacy  | MG Road, Bangalore      | `pharma123` |

### 🔓 Admin
> No login required. Access directly at: [http://localhost:5000/admin](http://localhost:5000/admin)

---

## 🧩 Application Modules

### 🩺 Doctor Module

| Route                        | Description                          |
|------------------------------|--------------------------------------|
| `/doctor/login`              | Login with Doctor ID + biometric     |
| `/doctor/dashboard`          | View patients & prescriptions        |
| `/doctor/register-patient`   | Register a new patient               |
| `/doctor/patient/<pid>`      | View patient profile & history       |
| `/doctor/create-prescription`| Create a new digital prescription    |
| `/prescription/qr/<rx_id>`   | View QR code for a prescription      |

**Workflow:**
1. Doctor logs in using their **Doctor ID + password + biometric scan**.
2. They register patients and create **digital prescriptions**.
3. Each prescription generates a **unique QR code** that encodes the Rx details.
4. The QR code and Rx ID are shared with the patient to present at the pharmacy.

---

### 💊 Pharmacy Module

| Route                              | Description                                      |
|------------------------------------|--------------------------------------------------|
| `/pharmacy/login`                  | Pharmacy login                                   |
| `/pharmacy/dashboard`              | View dispensed prescriptions                     |
| `/pharmacy/verify`                 | Search for a prescription by Rx ID               |
| `/pharmacy/patient-verify/<rx_id>` | Verify patient identity (3 methods)              |
| `/pharmacy/generate-otp/<rx_id>`   | Generate & send OTP to patient's phone           |
| `/pharmacy/issue/<rx_id>`          | Dispense medicines and mark prescription issued  |
| `/pharmacy/confirmation/<rx_id>`   | Show issuance confirmation receipt               |

**Workflow:**
1. Pharmacy staff logs in and searches for a prescription using the **Rx ID**.
2. The system displays medicine details and patient info.
3. Staff verifies the patient using one of three methods:
   - **Fingerprint Scan** (simulated)
   - **Patient ID** input
   - **OTP** sent to the registered phone number
4. Upon successful verification, medicines are dispensed and the prescription is **marked as Issued** (preventing duplicate dispensing).

---

### 🛡️ Admin Module

| Route    | Description                                      |
|----------|--------------------------------------------------|
| `/admin` | View all doctors, patients, prescriptions & logs |

The admin dashboard provides a **read-only overview** of all system data including the full prescription audit log.

---

## 🔗 API Endpoints

| Method | Endpoint                    | Description                     |
|--------|-----------------------------|---------------------------------|
| `GET`  | `/api/prescription/<rx_id>` | Get prescription details as JSON |
| `GET`  | `/api/patients`             | Get list of all patients as JSON |

**Example response** for `/api/prescription/RX-20240101-001`:
```json
{
  "rx_id": "RX-20240101-001",
  "doctor_name": "Dr. Arjun Sharma",
  "patient_name": "Rahul Verma",
  "medicines": [
    {
      "name": "Amoxicillin",
      "dosage": "500mg",
      "frequency": "Twice daily",
      "duration": "7 days"
    }
  ],
  "status": "Active",
  "created_on": "2024-01-15 10:30:00"
}
```

---

## 🖥️ Screenshots / Pages

| Page                    | URL                            |
|-------------------------|--------------------------------|
| 🏠 Home / Landing Page  | `/`                            |
| 🩺 Doctor Login         | `/doctor/login`                |
| 📋 Doctor Dashboard     | `/doctor/dashboard`            |
| 📄 Create Prescription  | `/doctor/create-prescription`  |
| 📱 QR Code Display      | `/prescription/qr/<rx_id>`     |
| 💊 Pharmacy Login       | `/pharmacy/login`              |
| 🔍 Verify Prescription  | `/pharmacy/verify`             |
| ✅ Issue Medicine        | `/pharmacy/issue/<rx_id>`      |
| 🛡️ Admin Dashboard     | `/admin`                       |

---

## ⚙️ How It Works

```
Doctor              System                 Pharmacy              Patient
  │                    │                      │                     │
  ├─ Login (Bio) ──────►│                      │                     │
  ├─ Register Patient ─►│                      │                     │
  ├─ Create Prescription►│                      │                     │
  │◄─ QR Code ──────────┤                      │                     │
  │                    │                      │                     │
  │                    │◄─ Search Rx ID ───────┤                     │
  │                    ├─ Rx Details ─────────►│                     │
  │                    │◄─ Verify Patient ─────┤                     │
  │                    │◄──── OTP / Fingerprint / ID ────────────────┤
  │                    ├─ Verification OK ────►│                     │
  │                    │◄─ Issue Medicine ─────┤                     │
  │                    ├─ Mark as Issued ──►   │                     │
  │                    ├─ Confirmation ────────►│                     │
```

---

## 🔮 Future Enhancements

- [ ] **Real database integration** (PostgreSQL / MySQL) replacing in-memory dicts
- [ ] **Actual biometric SDK** integration (WebAuthn or hardware fingerprint readers)
- [ ] **Real SMS OTP** delivery via Twilio or similar service
- [ ] **QR Code scanning** using device camera at pharmacy
- [ ] **Patient mobile app** for viewing prescriptions
- [ ] **Doctor registration & management** by admin
- [ ] **Prescription expiry** and validity period enforcement
- [ ] **PDF prescription download** with digital signature
- [ ] **Role-based access control** with hashed passwords (bcrypt)
- [ ] **Docker containerization** for easy deployment

---

## 📦 Dependencies

```
flask>=2.3.0
qrcode[pil]>=7.4.2
Pillow>=10.0.0
```

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## 📄 License

This project is intended for **educational and demonstration purposes**. Feel free to use, modify, and extend it for academic or hackathon projects.

---

> Built with ❤️ using Flask | QR Codes | Biometric Security Simulation
