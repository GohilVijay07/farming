# 🌾 AgriConnect — Smart Farming Management System

A full-stack, modern, clean, and beginner-friendly agricultural management web platform built using **Python Django**, **PostgreSQL**, **HTML5**, **CSS3**, and **JavaScript**.

Designed as a complete college practical/capstone project, **AgriConnect** empowers farmers to digitize crop cycles, monitor cultivated land acreage, track harvest schedules, explore agronomic best practices, and view weather forecasts through a responsive dashboard.

---

## 📸 Key Features

- 🔐 **Django Authentication System**: Secure farmer registration, split-screen login layout with quotes, session remember-me, and logout.
- 👨‍🌾 **Farmer Dashboard**: Interactive overview with real-time statistics (Total Crops, Active Plantings, Harvested Crops, Cultivated Land Area in acres).
- 🌾 **Full Crop CRUD Management**:
  - Add crops with variety, category, season, acreage, sowing date, expected harvest date, and agronomic notes.
  - Responsive **My Crops** table with live status badges (`Planted`, `Growing`, `Ready to Harvest`, `Harvested`).
  - Strict ownership-level security preventing farmers from viewing, editing, or deleting another user's crops.
  - JavaScript-powered deletion confirmation modal.
- 🔍 **Real-time Crop Catalog & Search**: Interactive library of major crops (Wheat, Rice, Cotton, Maize, Tomato, Potato, Sugarcane, Groundnut, Soybean, Mustard, Onion, Chickpea) with real-time instant search filtering.
- 💡 **Actionable Farming Tips**: Categorized guidance for Soil Preparation, Micro-Irrigation, Fertilizer Nutrition, Integrated Pest Management, Crop Rotation, and Organic Cultivation.
- 🌤️ **Agricultural Weather Advisory**: Weather metrics (temperature, humidity, wind velocity, rain probability) with region search and 5-day forecasts.
- 👤 **Farmer Profile Management**: Update full name, contact numbers, email, and farm location.
- 📬 **Contact & Inquiry Support**: Visitor inquiry form with message storage in PostgreSQL and instant feedback.
- 🛠️ **Django Administration Panel**: Customized administrative portal for managing farmers, crop inventories, and support messages.

---

## 🏛️ System Architecture (MVT Pattern)

AgriConnect follows the standard Django **Model-View-Template (MVT)** architecture:

```text
[ Browser / Client (HTML5 + CSS3 + Vanilla JS) ]
                     │  HTTP / CSRF
                     ▼
             [ Django URLs ]
                     │
                     ▼
            [ Django Views ] ─── (Forms & Auth Validation)
            ┌────────┴────────┐
            ▼                 ▼
   [ Django Templates ]  [ Django Models ]
       (HTML5/CSS/JS)         │
                              ▼
                    [ PostgreSQL Database ]
```

---

## 🛠️ Technology Stack

| Layer | Technology | Description |
|---|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | Bespoke agricultural design system (CSS variables, Flexbox, CSS Grid, mobile drawer). Zero React, zero heavy bloat. |
| **Backend** | Python (3.10+), Django (5.0+) | Robust web framework with built-in ORM, security, CSRF protection, and session management. |
| **Database** | PostgreSQL (with pgAdmin GUI) | High-performance enterprise relational database managed via `psycopg2-binary`. |
| **Icons & Typography** | Font Awesome 6.5, Outfit & Plus Jakarta Sans | Google Fonts and scalable vector icons. |
| **Configuration** | `python-dotenv` | Environment variable management for database credentials and secret keys. |

---

## 🧱 Database Models & Schema

```text
+---------------------+          +-----------------------------+
|   auth_user         | 1      1 |        FarmerProfile        |
+---------------------+----------+-----------------------------+
| id (PK)             |          | id (PK)                     |
| username            |          | user_id (OneToOne -> User)  |
| email               |          | full_name                   |
| password (hashed)   |          | phone                       |
| date_joined         |          | farm_location               |
+---------------------+          | created_at / updated_at     |
          | 1                    +-----------------------------+
          |
          | *
+------------------------------------+
|               Crop                 |
+------------------------------------+
| id (PK)                            |
| farmer_id (FK -> User)             |
| crop_name                          |
| crop_type (Cereal, Pulse, etc.)    |
| season (Kharif, Rabi, etc.)        |
| farm_area (Decimal in Acres)       |
| planting_date                      |
| expected_harvest_date              |
| status (Planted, Growing, etc.)    |
| notes                              |
| created_at / updated_at            |
+------------------------------------+

+------------------------------------+
|          ContactMessage            |
+------------------------------------+
| id (PK)                            |
| name                               |
| email                              |
| subject                            |
| message                            |
| created_at                         |
+------------------------------------+

+------------------------------------+
|        EmailVerificationOTP        |
+------------------------------------+
| id (PK)                            |
| user_id (FK -> User)               |
| otp_hash (Hashed 6-digit OTP)      |
| created_at                         |
| expires_at (10-min validity)       |
| is_verified (Boolean)              |
| attempts (Max 5 failed attempts)   |
+------------------------------------+
```

---

## 📂 Project Directory Structure

```text
d:\farming\
│
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── agriconnect/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── farming/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   └── js/
    │       └── script.js
    │
    └── templates/
        └── farming/
            ├── base.html
            ├── home.html
            ├── about.html
            ├── crops.html
            ├── farming_tips.html
            ├── weather.html
            ├── contact.html
            ├── login.html
            ├── register.html
            ├── verify_otp.html
            ├── dashboard.html
            ├── my_crops.html
            ├── add_crop.html
            ├── edit_crop.html
            └── profile.html
```


---

## 🚀 Quick Setup & Installation Guide

### Prerequisites
- Python 3.10 or higher
- PostgreSQL & pgAdmin installed and running on your Windows PC

---

### Step 1: Clone or Navigate to the Project Directory

```bash
cd d:\farming
```

---

### Step 2: Create and Activate a Python Virtual Environment

**On Windows (PowerShell / Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

---

### Step 3: Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4: Configure PostgreSQL & pgAdmin

1. Open **pgAdmin** (or `psql` command line):
   - Right-click **Databases** → **Create** → **Database...**
   - Set **Database Name**: `agriconnect_db`
   - Click **Save**

   *(Or execute in SQL Query Tool:)*
   ```sql
   CREATE DATABASE agriconnect_db;
   ```

2. Review or update your `.env` file in project root with your PostgreSQL password:
```env
SECRET_KEY=django-insecure-agriconnect-smart-farming-mgmt-system-key-2026
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=agriconnect_db
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
DB_HOST=localhost
DB_PORT=5432
```

---

### Step 5: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 6: Create an Admin Superuser

```bash
python manage.py createsuperuser
```
Follow prompts to set username (e.g. `admin`), email, and password.

---

### Step 7: Run Automated Tests

```bash
python manage.py test farming
```

---

### Step 8: Start the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:
- 🌾 **Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 🛡️ **Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔗 URL Routing Map

| URL Pattern | View Name | Description | Access Level |
|---|---|---|---|
| `/` | `home` | Landing page with hero & key pillars | Public |
| `/about/` | `about` | About platform, mission & advantages | Public |
| `/crops/` | `crops` | Crop catalog with instant search filter | Public |
| `/farming-tips/` | `farming_tips` | Agronomy best practices & category tabs | Public |
| `/weather/` | `weather` | Weather metrics & 5-day forecast | Public |
| `/contact/` | `contact` | Contact form saved to PostgreSQL | Public |
| `/register/` | `register` | Farmer account registration (generates 6-digit OTP) | Public |
| `/verify-otp/` | `verify_otp` | 6-digit numeric OTP verification page | Public |
| `/resend-otp/` | `resend_otp` | Resend fresh OTP with 60s cooldown | Public |
| `/login/` | `login` | Split-screen farmer login | Public |
| `/logout/` | `logout` | Session destroy & redirect | Authenticated |
| `/dashboard/` | `dashboard` | Farmer overview & live statistics | Farmer Only (`@login_required`) |
| `/my-crops/` | `my_crops` | Crop inventory table with badges | Farmer Only (`@login_required`) |
| `/add-crop/` | `add_crop` | Form to record new crop | Farmer Only (`@login_required`) |
| `/edit-crop/<id>/` | `edit_crop` | Update crop info (owner check) | Farmer Only (`@login_required`) |
| `/delete-crop/<id>/` | `delete_crop`| Remove crop record (owner check) | Farmer Only (`@login_required`) |
| `/profile/` | `profile` | View and edit farmer profile info | Farmer Only (`@login_required`) |
| `/admin/` | `admin:index` | Django administrative interface | Superuser / Staff |

---

## 📧 Email 6-Digit OTP Verification System

AgriConnect uses a **secure 6-digit numeric OTP email verification workflow** instead of token links.

```text
1. User enters registration details.
2. Account is created in inactive status (is_active = False).
3. A random, cryptographically secure 6-digit OTP is generated.
4. The OTP is salted & hashed using PBKDF2/SHA-256 before saving to PostgreSQL.
5. Rich HTML and plain-text fallback emails are dispatched to the user's email.
6. The user is redirected to /verify-otp/ with a modern 6-box input interface.
7. The OTP is valid for exactly 3 minutes (live countdown timer).

8. A maximum of 5 incorrect attempts is permitted before the OTP is invalidated.
9. Resending an OTP triggers a 60-second cooldown timer both client-side and server-side.
10. Correct OTP verification marks the account active (is_active = True) and redirects to Login.
11. Unverified accounts cannot log in and are prompted to verify or resend their OTP.
```

---

### 🧪 Local Testing without Sending Real Emails (Console Backend)

For instant local testing and grading without SMTP or internet credentials, configure your `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

When registering a new user or requesting an OTP resend, Django will automatically print the complete email and **6-digit OTP directly to your terminal console**.

---

### 📬 Gmail SMTP Configuration (Production with Google App Password)

To send real emails to Gmail or other inboxes:

1. Enable **2-Step Verification** on your Google Account:
   - Go to [Google Account Security](https://myaccount.google.com/security)
2. Generate an **App Password**:
   - Search for **App passwords** in your Google Account search bar
   - App Name: `AgriConnect`
   - Copy the generated 16-character password (e.g. `abcd efgh ijkl mnop`)
3. Update your `.env` file:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_16_char_app_password
DEFAULT_FROM_EMAIL=AgriConnect <your_email@gmail.com>
```

> [!NOTE]
> Do NOT use your regular Gmail login password. Always use a Google App Password.

---

### 🛡️ How OTP Security Works

1. **Cryptographically Secure Random Generation**: Generated using Python's `secrets.randbelow(1000000)` instead of pseudo-random generators.
2. **Database Hashing**: The actual 6-digit code is **never stored in plain text**. Only a salted PBKDF2-SHA256 hash is saved in `EmailVerificationOTP.otp_hash`.
3. **Single-Use Invalidation**: Upon successful verification, the OTP is marked `is_verified = True` and cannot be reused.
4. **10-Minute Expiration**: Requests older than 10 minutes are strictly rejected by the server.
5. **Brute-Force Protection**: Capped at 5 failed attempts per OTP record. Exceeding 5 attempts immediately invalidates the OTP.
6. **Rate-Limiting**: 60-second cooldown enforced on the server preventing spam requests.
7. **Session Segregation**: Unverified accounts have `is_active = False`, blocking all authenticated dashboard routes until verification completes.


---

## 🔒 Security Best Practices Implemented

1. **CSRF Protection**: All form submissions include `{% csrf_token %}` to prevent Cross-Site Request Forgery.
2. **Strict User Data Isolation**: Queries filter exclusively by `farmer=request.user`. Unauthorized modification attempts to another user's crop ID are blocked.
3. **Password Security**: Passwords are never stored in plain text; Django's PBKDF2 with SHA-256 algorithm is utilized.
4. **Environment Isolation**: Database credentials and secret keys are managed through `.env` and omitted from version control via `.gitignore`.
5. **Session Safety**: Supports session expiration on browser close unless "Remember Me" is selected.

---

## 🎓 College Viva / Practical Q&A Cheat Sheet

**Q1: What is Django MVT architecture?**
- **Model**: Python classes in `models.py` that map directly to PostgreSQL tables.
- **View**: Python functions in `views.py` that process incoming HTTP requests and return HTTP responses.
- **Template**: HTML5 files with Django Template Language (DTL) tags to dynamically render data.

**Q2: Why use PostgreSQL and psycopg2-binary with Django?**
- PostgreSQL is an advanced open-source Object-Relational Database Management System (ORDBMS) offering high concurrency, strict ACID compliance, and robust data integrity. `psycopg2-binary` provides the high-speed C-optimized database adapter between Django ORM and PostgreSQL.

**Q3: How does data isolation work between different farmers?**
- In `views.py`, functions use the `@login_required` decorator, and every query strictly applies `.filter(farmer=request.user)`. If an ID is passed in `/edit-crop/<id>/`, the view verifies `if crop.farmer != request.user:` before executing any updates.

---

## 📜 License
Developed for educational, university, and agricultural development purposes.
