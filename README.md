# 🔥 Fire Detection using YOLOv8

A real-time **AI-powered fire detection system** that uses **YOLOv8 and OpenCV** to detect fire through a webcam or video feed. When fire is detected, the system can trigger an alarm and send automated notifications through SMS, email, and desktop alerts.

## 🚀 Features

* 🔥 Real-time fire detection using YOLOv8
* 📷 Webcam-based detection
* 🎥 Video-based fire detection
* 🎯 Confidence-based detection filtering
* 🚨 Automatic alarm sound
* 📱 SMS alerts using Twilio
* 📧 Email notifications
* 🖥️ Desktop notifications
* 🌐 Flask-based web dashboard
* 🔐 Login-protected dashboard
* 📊 Live video detection interface

## 🛠️ Tech Stack

* **Python**
* **YOLOv8 / Ultralytics**
* **OpenCV**
* **Flask**
* **NumPy**
* **CVZone**
* **Twilio**
* **HTML/CSS**
* **Windows Sound API**

## 📂 Project Structure

```text
Fire-Detection-using-YOLOv8/
│
├── app.py
├── fire.py
├── fire (1).py
├── sms_notifier.py
├── best.pt
├── requirements.txt
├── run_web.bat
│
├── templates/
│   ├── dashboard.html
│   └── login.html
│
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Fire-Detection-using-YOLOv8.git
cd Fire-Detection-using-YOLOv8
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Fire Detection System

### Webcam detection

```bash
python fire.py
```

### Web application

```bash
python app.py
```

Then open:

```text
http://localhost:5000
```

The web interface provides a login page and a live fire-detection dashboard.

## 📱 Configure SMS Alerts

SMS notifications can be enabled using Twilio.

Set the following environment variables:

```text
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM=your_twilio_number
ALERT_PHONES=recipient_number
```

Never store Twilio credentials directly in the source code.

## 📧 Email Alerts

The system can also send email notifications when fire is detected.

Configure your email credentials through environment variables rather than committing passwords or app passwords to GitHub.

## 🧠 How It Works

```text
Webcam / Video
      ↓
OpenCV Frame Capture
      ↓
YOLOv8 Model
      ↓
Fire Detection
      ↓
Confidence Filtering
      ↓
Fire Detected?
   ↙          ↘
 YES           NO
  ↓             ↓
Alarm        Continue
  ↓
Notifications
 ↙    ↓     ↘
SMS  Email  Desktop
```

## 🎯 Applications

This system can be adapted for:

* 🏭 Industrial safety monitoring
* 🏢 Office and building surveillance
* 🏠 Smart home safety systems
* 🏪 Shops and warehouses
* 🚗 Parking and facility monitoring
* 🌲 Fire-risk monitoring environments

## 🔮 Future Improvements

* Cloud-based monitoring
* Mobile application integration
* Multiple camera support
* Fire severity estimation
* Cloud notification dashboard
* Database-based detection history
* Improved model accuracy with a larger dataset
* Edge-device deployment

## ⚠️ Security

Before deploying this project:

* Never commit API keys or passwords.
* Store Twilio credentials in environment variables.
* Store email credentials securely.
* Change the default login credentials.
* Change the Flask secret key before production deployment.

## 👨‍💻 Author

**Naveen Kumar B L**

Computer Science & Data Science Student

---

⭐ If you find this project useful, consider giving the repository a star!
