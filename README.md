# 🌾 AgriConnect — Smart Farming Management System

<p align="center">
  <img src="https://img.icons8.com/fluency/96/plant-under-rain.png" alt="AgriConnect Logo" width="90">
</p>

<h3 align="center">
  Smart Digital Farming Management Platform for Gujarat Farmers
</h3>

<p align="center">
  A modern full-stack farming management website built with Django, PostgreSQL, HTML, CSS and JavaScript.
</p>

<p align="center">

  <a href="https://github.com/GohilVijay07/AgriConnect">
    <img src="https://img.shields.io/badge/GitHub-AgriConnect-black?style=for-the-badge&logo=github">
  </a>

  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Django-5.x-green?style=for-the-badge&logo=django">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql">
  <img src="https://img.shields.io/badge/HTML5-Frontend-orange?style=for-the-badge&logo=html5">
  <img src="https://img.shields.io/badge/CSS3-Styling-blue?style=for-the-badge&logo=css3">
  <img src="https://img.shields.io/badge/JavaScript-Frontend-yellow?style=for-the-badge&logo=javascript">

</p>

---

## 🌾 About AgriConnect

**AgriConnect** is a modern, full-stack agricultural management platform developed using **Python Django, PostgreSQL, HTML5, CSS3 and JavaScript**.

The main purpose of this project is to provide farmers with a simple digital platform where they can manage their farming activities, crops, farm area, harvest schedules, farming knowledge and weather information.

The project is specially designed with a **Gujarat-focused farming approach**, making it suitable for farmers and agricultural activities across Gujarat, India.

AgriConnect combines:

- 🌾 Crop Management
- 👨‍🌾 Farmer Dashboard
- 🌦️ Gujarat Weather Information
- 💡 Farming Tips
- 🔐 Secure Authentication
- 📧 Email OTP Verification
- 🔑 Forgot Password with OTP
- 📬 Contact & Support
- 🛠️ Django Admin Panel
- 📊 Farmer Statistics
- 👤 Farmer Profile Management

---

# ✨ Key Features

## 🔐 Secure Authentication

AgriConnect includes a complete Django authentication system.

Features include:

- Farmer Registration
- Farmer Login
- Logout
- Remember Me
- Password Security
- Email Verification
- 6-Digit OTP Verification
- OTP Resend
- OTP Expiration
- Forgot Password
- Password Reset using OTP
- Unverified users cannot access protected pages

---

## 📧 Email OTP Verification

New users must verify their email address before accessing the farmer dashboard.

### OTP Flow

```text
User Registration
       ↓
Account Created
       ↓
6-Digit OTP Generated
       ↓
OTP Sent to Email
       ↓
User Enters OTP
       ↓
OTP Verified
       ↓
Account Activated
       ↓
User Can Login
```

Security features include:

- 🔢 6-digit numeric OTP
- 🔐 Hashed OTP storage
- ⏱️ OTP expiration
- 🚫 Maximum failed attempts
- 🔄 OTP resend cooldown
- ✅ Single-use verification
- 🔒 Unverified accounts remain inactive

---

# 🔑 Forgot Password with OTP

AgriConnect also provides a secure password recovery system.

### Password Reset Flow

```text
Forgot Password
       ↓
Enter Registered Email
       ↓
OTP Sent to Email
       ↓
Enter 6-Digit OTP
       ↓
OTP Verified
       ↓
Create New Password
       ↓
Password Updated
       ↓
Login
```

Users can recover their account without needing to contact the administrator.

---

# 👨‍🌾 Farmer Dashboard

After successful login, farmers get access to a personalized dashboard.

The dashboard displays:

- 🌾 Total Crops
- 🌱 Active Crops
- 📦 Harvested Crops
- 📐 Total Farm Area
- 📅 Recent Crop Plantings
- 🌦️ Weather Access
- 💡 Farming Tips
- 👤 Profile Management

The dashboard is designed to provide a quick overview of the farmer's agricultural activities.

---

# 🌾 Crop Management

AgriConnect provides complete **CRUD functionality** for crop management.

Farmers can:

- ➕ Add Crops
- 👁️ View Crops
- ✏️ Edit Crops
- 🗑️ Delete Crops
- 📅 Track Planting Dates
- 📅 Track Expected Harvest Dates
- 📐 Manage Farm Area
- 🌱 Select Crop Season
- 📝 Add Farming Notes

### Crop Status

The system supports statuses such as:

```text
Planted
Growing
Ready to Harvest
Harvested
```

Each farmer can only access their own crop records.

---

# 🔍 Crop Catalog

The website contains a searchable crop catalog.

Example crops:

- 🌾 Wheat
- 🌾 Rice
- 🌿 Cotton
- 🌽 Maize
- 🍅 Tomato
- 🥔 Potato
- 🎋 Sugarcane
- 🥜 Groundnut
- 🌱 Soybean
- 🌿 Mustard
- 🧅 Onion
- 🫘 Chickpea

The crop catalog includes JavaScript-powered instant search.

---

# 💡 Farming Tips

AgriConnect provides useful agricultural information organized into different categories.

### Categories

- 🌱 Soil Preparation
- 💧 Micro-Irrigation
- 🧪 Fertilizer & Nutrition
- 🐛 Integrated Pest Management
- 🔄 Crop Rotation
- 🌿 Organic Farming

The goal is to make useful farming information easier to access from one platform.

---

# 🌦️ Gujarat Weather System

AgriConnect provides weather information specifically focused on **Gujarat, India**.

The system uses **WeatherAPI.com** for weather data.

### Weather Features

- 🌡️ Current Temperature
- 🌤️ Weather Condition
- 💧 Humidity
- 🌬️ Wind Speed
- 🌧️ Rain Probability
- 🌡️ Feels Like Temperature
- 👁️ Visibility
- ☀️ UV Index
- 📅 5-Day Forecast
- 🌧️ Rainfall Information
- 🌾 Farmer-Friendly Weather Advice

---

## 📍 Gujarat Locations

The weather system supports Gujarat locations such as:

- Ahmedabad
- Amreli
- Anand
- Aravalli
- Banaskantha
- Bharuch
- Bhavnagar
- Botad
- Chhota Udepur
- Dahod
- Dang
- Devbhoomi Dwarka
- Gandhinagar
- Gir Somnath
- Jamnagar
- Junagadh
- Kheda
- Kutch
- Mahisagar
- Mehsana
- Morbi
- Narmada
- Navsari
- Panchmahal
- Patan
- Porbandar
- Rajkot
- Sabarkantha
- Surat
- Surendranagar
- Tapi
- Vadodara
- Valsad

The application is designed to prevent unsupported locations outside Gujarat from being used in the Gujarat-focused weather system.

---

# 🌦️ Weather Architecture

The WeatherAPI key is kept on the Django backend.

```text
User Browser
     │
     ▼
AgriConnect Weather Page
     │
     ▼
Django Weather Endpoint
     │
     ▼
WeatherAPI.com
     │
     ▼
Weather Data
     │
     ▼
Django Backend
     │
     ▼
AgriConnect Frontend
```

The API key is **not exposed to the browser**.

---

# 👤 Farmer Profile

Farmers can manage their profile information.

Profile includes:

- Full Name
- Email
- Phone Number
- Farm Location
- Account Information

---

# 📬 Contact & Support

Visitors can contact the AgriConnect support team using the contact form.

The system stores:

- Name
- Email
- Subject
- Message
- Date & Time

Contact messages can also be managed through the Django Admin Panel.

---

# 🛠️ Admin Panel

AgriConnect includes a customized **Django Administration Panel**.

Administrators can manage:

- 👨‍🌾 Farmers
- 🌾 Crop Records
- 📬 Contact Messages
- 📧 Verification Records
- 👤 User Accounts
- 📊 Website Data

The admin panel provides centralized management of the application.

---

# 📊 Admin Dashboard

The administration system can be used to monitor important application information such as:

- Total Registered Users
- Total Crops
- Active Crops
- Harvested Crops
- Total Farm Area
- Contact Messages
- Recent User Registrations
- Recent Crop Activities

---

# 🏛️ System Architecture

AgriConnect follows the **Django Model-View-Template (MVT)** architecture.

```text
                  ┌─────────────────────┐
                  │   User / Browser    │
                  │ HTML CSS JavaScript │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Django URLs     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Django Views     │
                  │ Auth / Validation   │
                  └───────┬───────┬─────┘
                          │       │
              ┌───────────┘       └───────────┐
              ▼                               ▼
      ┌─────────────────┐             ┌─────────────────┐
      │ Django Templates│             │ Django Models   │
      │ HTML/CSS/JS     │             │ Python ORM      │
      └─────────────────┘             └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │   PostgreSQL    │
                                      │    Database     │
                                      └─────────────────┘
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Backend programming |
| 🟢 Django | Web framework |
| 🌐 HTML5 | Website structure |
| 🎨 CSS3 | UI and responsive design |
| ⚡ JavaScript | Interactive functionality |
| 🐘 PostgreSQL | Database |
| 🛠️ pgAdmin | Database management |
| 🌦️ WeatherAPI.com | Weather data |
| 🔐 Django Auth | Authentication |
| 📧 SMTP | Email OTP |
| 🔑 python-dotenv | Environment variables |
| ⭐ Font Awesome | Icons |

---

# 🗄️ Database

AgriConnect uses:

**PostgreSQL**

with:

**pgAdmin**

for database management.

### Main database entities

```text
User
 │
 ├── FarmerProfile
 │
 ├── Crop
 │
 └── EmailVerificationOTP

ContactMessage
```

---

# 🧱 Database Models

### FarmerProfile

```text
id
user
full_name
phone
farm_location
created_at
updated_at
```

### Crop

```text
id
farmer
crop_name
crop_type
season
farm_area
planting_date
expected_harvest_date
status
notes
created_at
updated_at
```

### ContactMessage

```text
id
name
email
subject
message
created_at
```

### EmailVerificationOTP

```text
id
user
otp_hash
created_at
expires_at
is_verified
attempts
```

---

# 📂 Project Structure

```text
AgriConnect/
│
├── manage.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
│
├── agriconnect/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── farming/
    │
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
            ├── forgot_password.html
            ├── reset_password.html
            ├── dashboard.html
            ├── my_crops.html
            ├── add_crop.html
            ├── edit_crop.html
            └── profile.html
```

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/GohilVijay07/AgriConnect.git
```

```bash
cd AgriConnect
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🐘 PostgreSQL Setup

Make sure PostgreSQL is installed and running.

Open **pgAdmin**.

Create a database:

```text
agriconnect_db
```

Or execute:

```sql
CREATE DATABASE agriconnect_db;
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True

DB_NAME=agriconnect_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5432

WEATHER_API_KEY=your_weatherapi_key

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=AgriConnect <your_email@gmail.com>
```

⚠️ **Never upload the real `.env` file or API keys to GitHub.**

---

# 🗃️ Run Migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

# 👨‍💻 Create Admin Account

```bash
python manage.py createsuperuser
```

Follow the instructions and create your admin account.

---

# 🧪 Run Tests

```bash
python manage.py test
```

---

# ▶️ Run the Website

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

---

# 🔗 Main Pages

| Page | URL |
|---|---|
| 🏠 Home | `/` |
| ℹ️ About | `/about/` |
| 🌾 Crops | `/crops/` |
| 💡 Farming Tips | `/farming-tips/` |
| 🌦️ Weather | `/weather/` |
| 📬 Contact | `/contact/` |
| 📝 Register | `/register/` |
| 🔢 Verify OTP | `/verify-otp/` |
| 🔄 Resend OTP | `/resend-otp/` |
| 🔐 Login | `/login/` |
| 🔑 Forgot Password | `/forgot-password/` |
| 👨‍🌾 Dashboard | `/dashboard/` |
| 🌾 My Crops | `/my-crops/` |
| ➕ Add Crop | `/add-crop/` |
| 👤 Profile | `/profile/` |
| 🛠️ Admin | `/admin/` |

---

# 🔒 Security

AgriConnect implements several security practices:

- 🔐 Django password hashing
- 🛡️ CSRF protection
- 🔑 Environment variables
- 🚫 API key protection
- 👤 User-specific data isolation
- 🔒 Login-protected dashboard
- 🔐 Hashed OTP storage
- ⏱️ OTP expiration
- 🚫 OTP brute-force protection
- 🔄 OTP resend rate limiting
- 🗄️ Secure PostgreSQL database access

Each farmer can access only their own crop records.

---

# 📱 Responsive Design

AgriConnect is designed for:

- 💻 Desktop
- 💻 Laptop
- 📱 Mobile
- 📲 Tablet

The interface uses responsive CSS with:

- Flexbox
- CSS Grid
- Responsive navigation
- Mobile-friendly forms
- Responsive cards and tables

---

# 🎯 Project Objectives

The main objectives of AgriConnect are:

1. Build a real-world Django web application.
2. Learn Django MVT architecture.
3. Implement PostgreSQL database integration.
4. Implement secure authentication.
5. Implement email OTP verification.
6. Implement password recovery using OTP.
7. Build complete CRUD functionality.
8. Integrate real weather information.
9. Create a responsive frontend.
10. Build an administrative management system.
11. Develop a practical agricultural solution for Gujarat farmers.

---

# 🎓 College Project

AgriConnect was developed as a **college practical / academic capstone project** to demonstrate practical knowledge of:

```text
Python
Django
HTML
CSS
JavaScript
PostgreSQL
Database Management
Authentication
REST/API Integration
Responsive Web Design
```

---

# 🚧 Future Improvements

Possible future improvements:

- 📱 Progressive Web App
- 🌦️ Advanced weather alerts
- 🌾 Crop disease detection
- 🤖 AI farming assistant
- 📊 Advanced crop analytics
- 📈 Market price tracking
- 🛒 Agricultural marketplace
- 🚜 Farm equipment management
- 📍 Gujarat district-wise agricultural insights
- 🌐 Gujarati language support
- 📱 Mobile application
- 🔔 Weather notifications
- 📊 Advanced admin analytics

---

# ⚠️ Disclaimer

AgriConnect is an **educational and academic project** created for learning and demonstration purposes.

Weather information is provided through WeatherAPI.com.

Agricultural recommendations shown by the application are general informational guidance and should not replace professional agricultural advice.

---

# 👨‍💻 Developer

## Vijay Gohil

**Python Developer | Django Developer | Web Developer | AI & Technology Enthusiast**

I enjoy building practical applications using Python, Django, databases and modern web technologies.

### 🔗 Connect With Me

<p>
  <a href="https://github.com/GohilVijay07">
    <img src="https://img.shields.io/badge/GitHub-GohilVijay07-black?style=for-the-badge&logo=github">
  </a>
</p>

### GitHub Profile

https://github.com/GohilVijay07

### AgriConnect Repository

https://github.com/GohilVijay07/AgriConnect

---

# ⭐ Support

If you like this project:

⭐ Star the repository

🍴 Fork the repository

🐛 Report issues

💡 Suggest improvements

Your support motivates me to build more projects! 🚀

---

<p align="center">

### 🌾 Made with ❤️ by Vijay Gohil

**AgriConnect — Smart Farming Management for Gujarat**

</p>
