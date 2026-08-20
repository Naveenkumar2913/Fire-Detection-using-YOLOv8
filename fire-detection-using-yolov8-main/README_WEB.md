# Fire Detection Web Application

## How to Run the Web Application

### Method 1: Using the Batch File (Easiest)
1. Double-click `run_web.bat`
2. Wait for the server to start
3. Open your browser and go to: **http://localhost:5000**

### Method 2: Using Command Line
1. Open Command Prompt or PowerShell
2. Navigate to the project folder:
   ```
   cd "C:\Users\vinay t\OneDrive\Desktop\FIRE"
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your browser and go to: **http://localhost:5000**

## Login Credentials
- **Username:** `admin`
- **Password:** `admin123`

## Troubleshooting

### If the web page doesn't open:
1. Make sure Flask is installed:
   ```
   pip install flask
   ```

2. Check if port 5000 is already in use:
   - Close any other applications using port 5000
   - Or change the port in `app.py` (line 260) to a different port like 5001

3. Check the console for error messages

4. Make sure your webcam is connected and not being used by another application

5. Try accessing: `http://127.0.0.1:5000` instead of `localhost:5000`

### If you see "ModuleNotFoundError":
- Make sure you're running the command from the project directory
- Make sure all dependencies are installed: `pip install -r requirements.txt`

### If the video feed doesn't show:
- Make sure your webcam is connected
- Check if the webcam is being used by another application
- Try restarting the application

## Features
- ✅ Login system with username/password
- ✅ Live webcam feed with fire detection
- ✅ Real-time fire detection using YOLO model
- ✅ Email notifications when fire is detected
- ✅ SMS notifications when fire is detected
- ✅ Alarm sound when fire is detected

## Default Configuration
- Server runs on: `http://localhost:5000`
- Login username: `admin`
- Login password: `admin123`

**⚠️ IMPORTANT:** Change the login credentials in `app.py` (lines 29-30) for security!

