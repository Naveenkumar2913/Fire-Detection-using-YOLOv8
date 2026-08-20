import os
from typing import List

# Try to import Twilio; functions will handle if it's not installed
try:
    from twilio.rest import Client
    _TWILIO_AVAILABLE = True
except Exception:
    _TWILIO_AVAILABLE = False


def _send_via_twilio(numbers: List[str], body: str) -> bool:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM")

    if not (account_sid and auth_token and from_number and _TWILIO_AVAILABLE):
        return False

    try:
        client = Client(account_sid, auth_token)
        for to in numbers:
            client.messages.create(body=body, from_=from_number, to=to)
        return True
    except Exception:
        return False


def send_alert(numbers, message: str) -> bool:
    """Send an alert SMS to a list of `numbers` (list of strings).

    Behavior:
    - If Twilio credentials and package are available, use Twilio.
    - Otherwise, print a helpful message (developer should configure env vars).

    Returns True on (attempted) send via Twilio, False otherwise.
    """
    if isinstance(numbers, str):
        numbers = [numbers]

    numbers = [n.strip() for n in numbers if n and n.strip()]
    if not numbers:
        return False

    # Try Twilio first
    sent = _send_via_twilio(numbers, message)
    if sent:
        return True

    # Fallback: print to console with instructions (useful in development)
    print("--- SMS Alert (fallback) ---")
    print(f"To: {', '.join(numbers)}")
    print(f"Message: {message}")
    print("Note: Twilio not configured or not installed. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM and install the 'twilio' package to enable real SMS sending.")
    return False
