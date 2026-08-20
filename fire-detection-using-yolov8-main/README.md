Fire Detection SMS Alerts

Overview:
- The project detects fire using a YOLO model (`best.pt`).
- When fire is detected, the script `fire.py` will:
  - Play an alarm sound
  - Send an SMS alert (if configured)

Quick setup:
1. Create a Python virtual environment and activate it.

   PowerShell:
```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure Twilio environment variables to enable real SMS sending:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM` (your Twilio phone number, e.g. +1XXXXXXXXXX)
- `ALERT_PHONES` (comma-separated list of recipient numbers, e.g. +1AAA...,+1BBB...)

Example (PowerShell):
```
$env:TWILIO_ACCOUNT_SID = "AC..."
$env:TWILIO_AUTH_TOKEN = "your_token"
$env:TWILIO_FROM = "+1XXXXXXXXXX"
$env:ALERT_PHONES = "+1AAA...,+1BBB..."
```

3. Run the detection:
```
python fire.py
```

Notes & testing:
- If `twilio` isn't configured or installed, the script will print the SMS contents to console as a fallback.
- The `fire.py` implementation sends one SMS per detected event and won't spam while the fire remains continuously detected.

If you want, I can:
- Add SMTP-to-carrier fallback (less reliable),
- Add logging or persistent alert history, or
- Update `fire (1).py` similarly to send alerts for video input.
