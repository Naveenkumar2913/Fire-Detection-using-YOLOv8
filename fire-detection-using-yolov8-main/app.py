from flask import Flask, render_template, Response, request, redirect, url_for, session
from ultralytics import YOLO
import cv2
import cvzone
import threading
import winsound
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import base64
try:
    from win10toast import ToastNotifier
    DESKTOP_NOTIF_AVAILABLE = True
except ImportError:
    DESKTOP_NOTIF_AVAILABLE = False

try:
    from twilio.rest import Client
    SMS_AVAILABLE = True
except ImportError:
    SMS_AVAILABLE = False

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production!

# ========== CONFIGURATION ==========
# Login Credentials
LOGIN_USERNAME = "admin"
LOGIN_PASSWORD = "admin123"  # Change this password!

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "mrvinayvini@gmail.com"
EMAIL_PASSWORD = "gzyc jhkk ovmz rral"
FROM_EMAIL = "mrvinayvini@gmail.com"

EMPLOYEE_EMAILS = [
    "mrvinayv66@example.com"
]

# SMS Configuration (Twilio)
TWILIO_ACCOUNT_SID = "AC8252015029906324781242689001275"
TWILIO_AUTH_TOKEN = "35a230a7d105596a57a8505211410277"
TWILIO_PHONE_NUMBER = "+19733645508"

EMPLOYEE_PHONES = [
    "+916363385506"
]

# Enable/Disable notification types
ENABLE_EMAIL_NOTIFICATIONS = True
ENABLE_DESKTOP_NOTIFICATIONS = True
ENABLE_SMS_NOTIFICATIONS = True

# Detection Filtering Settings
MIN_CONFIDENCE = 0.5
MIN_DETECTION_FRAMES = 3
MIN_BOX_AREA = 3000
MAX_ASPECT_RATIO = 3.0
MIN_ASPECT_RATIO = 0.3
# ===================================

# Global variables for video capture and model
cap = None
model = None
alarm_playing = False
notification_sent = False
detection_count = 0

def init_camera():
    global cap, model
    if cap is None:
        cap = cv2.VideoCapture(0)
        # Optimize camera buffer - reduce buffer size for lower latency
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if model is None:
        try:
            model = YOLO("best.pt")
        except:
            model = YOLO("venv/best.pt")
    return cap, model

def play_alarm():
    try:
        winsound.PlaySound("mixkit-facility-alarm-sound-999.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    except:
        try:
            winsound.PlaySound("venv/mixkit-facility-alarm-sound-999.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        except:
            print("Alarm sound file not found")

def stop_alarm():
    winsound.PlaySound(None, winsound.SND_PURGE)

def send_email_notification():
    if not ENABLE_EMAIL_NOTIFICATIONS or not EMPLOYEE_EMAILS:
        return
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = ", ".join(EMPLOYEE_EMAILS)
        msg['Subject'] = "🚨 FIRE DETECTED - IMMEDIATE ACTION REQUIRED"
        body = f"""
        ⚠️ EMERGENCY ALERT ⚠️
        
        FIRE HAS BEEN DETECTED IN THE FACILITY!
        
        Detection Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        Please evacuate immediately and contact emergency services.
        
        This is an automated alert from the Fire Detection System.
        """
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, EMPLOYEE_EMAILS, text)
        server.quit()
        print(f"✅ Email notifications sent to {len(EMPLOYEE_EMAILS)} employees")
    except Exception as e:
        print(f"❌ Error sending email notifications: {str(e)}")

def send_sms_notification():
    if not ENABLE_SMS_NOTIFICATIONS or not SMS_AVAILABLE or not EMPLOYEE_PHONES:
        return
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message_body = f"🚨 FIRE DETECTED! Fire has been detected in the facility at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Please evacuate immediately!"
        for phone in EMPLOYEE_PHONES:
            try:
                message = client.messages.create(
                    body=message_body,
                    from_=TWILIO_PHONE_NUMBER,
                    to=phone
                )
                print(f"✅ SMS sent to {phone}")
            except Exception as e:
                print(f"❌ Error sending SMS to {phone}: {str(e)}")
        print(f"✅ SMS notifications sent to {len(EMPLOYEE_PHONES)} employees")
    except Exception as e:
        print(f"❌ Error sending SMS notifications: {str(e)}")

def send_notifications():
    threads = []
    if ENABLE_EMAIL_NOTIFICATIONS:
        email_thread = threading.Thread(target=send_email_notification, daemon=True)
        email_thread.start()
        threads.append(email_thread)
    if ENABLE_SMS_NOTIFICATIONS:
        sms_thread = threading.Thread(target=send_sms_notification, daemon=True)
        sms_thread.start()
        threads.append(sms_thread)
    return threads

def generate_frames():
    global alarm_playing, notification_sent, detection_count
    cap, model = init_camera()
    
    # Optimize camera settings for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    frame_count = 0
    process_every_n_frames = 2  # Process every 2nd frame for detection (faster)
    last_detections = []  # Store last detections to draw on skipped frames
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize for display
        display_frame = cv2.resize(frame, (640, 480))
        frame_count += 1
        
        # Only run detection on every Nth frame to improve performance
        if frame_count % process_every_n_frames == 0:
            # Use smaller resolution for faster inference
            detection_frame = cv2.resize(frame, (640, 480))
            
            # Optimized YOLO inference with lower confidence threshold for speed
            results = model(detection_frame, conf=MIN_CONFIDENCE, imgsz=640, verbose=False)
            
            fire_detected = False
            valid_detection = False
            last_detections = []  # Clear previous detections
            
            for r in results:
                for box in r.boxes:
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    
                    if conf < MIN_CONFIDENCE:
                        continue
                    
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    box_width = x2 - x1
                    box_height = y2 - y1
                    box_area = box_width * box_height
                    
                    if box_area < MIN_BOX_AREA:
                        continue
                    
                    aspect_ratio = box_width / box_height if box_height > 0 else 0
                    if aspect_ratio > MAX_ASPECT_RATIO or aspect_ratio < MIN_ASPECT_RATIO:
                        continue
                    
                    valid_detection = True
                    # Store detection for drawing
                    last_detections.append((x1, y1, x2, y2, conf))
            
            # Draw detections on display frame
            for x1, y1, x2, y2, conf in last_detections:
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cvzone.putTextRect(display_frame, f"FIRE {int(conf*100)}%", (x1, y1 - 10), scale=1, thickness=2)
            
            if valid_detection:
                detection_count += 1
                if detection_count >= MIN_DETECTION_FRAMES:
                    fire_detected = True
            else:
                detection_count = 0
            
            if fire_detected and not alarm_playing:
                alarm_playing = True
                threading.Thread(target=play_alarm, daemon=True).start()
                if not notification_sent:
                    notification_sent = True
                    print("🚨 FIRE DETECTED! Sending notifications to employees...")
                    send_notifications()
            
            if not fire_detected:
                if alarm_playing:
                    stop_alarm()
                    print("✅ Fire cleared. Alarm stopped.")
                alarm_playing = False
                notification_sent = False
        else:
            # Draw last detections on skipped frames for smooth display
            for x1, y1, x2, y2, conf in last_detections:
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cvzone.putTextRect(display_frame, f"FIRE {int(conf*100)}%", (x1, y1 - 10), scale=1, thickness=2)
        
        # Encode frame as JPEG with optimized quality for faster encoding
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 85]  # Slightly lower quality for speed
        ret, buffer = cv2.imencode('.jpg', display_frame, encode_params)
        if ret:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/video_feed')
def video_feed():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

