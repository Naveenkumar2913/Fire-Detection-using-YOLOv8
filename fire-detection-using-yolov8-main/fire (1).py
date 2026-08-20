from ultralytics import YOLO
import cvzone
import cv2
import math
import os
import threading
import sms_notifier

cap = cv2.VideoCapture('fire2.mp4')
model = YOLO('best.pt')

classnames = ['fire']
alert_sent = False

try:
    while True:
    ret, frame = cap.read()

    if not ret:
        print("No frame received. Ending...")
        break   # Exit loop if video ends or can't read frame

    frame = cv2.resize(frame, (640, 480))
    result = model(frame, stream=True)

    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = math.ceil(box.conf[0] * 100)
            Class = int(box.cls[0])
            if confidence > 50:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', 
                                   [x1 + 8, y1 + 100], scale=1.5, thickness=2)
                fire_detected = True
            else:
                # ensure fire_detected is defined when no boxes exceed threshold
                try:
                    fire_detected
                except NameError:
                    fire_detected = False

        cv2.imshow('frame', frame)

        # SMS alert logic: send once per detection event
        if 'fire_detected' in locals() and fire_detected and not alert_sent:
            alert_sent = True
            try:
                phones_env = os.getenv('ALERT_PHONES', '')
                phones = [p.strip() for p in phones_env.split(',') if p.strip()]
                if phones:
                    msg = 'ALERT: Fire detected in video feed!'
                    threading.Thread(target=sms_notifier.send_alert, args=(phones, msg), daemon=True).start()
            except Exception:
                pass

        if not ('fire_detected' in locals() and fire_detected):
            alert_sent = False

        # Stop if user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Also stop if the window was closed by the user
        try:
            if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
                break
        except Exception:
            pass
except KeyboardInterrupt:
    pass
finally:
    cap.release()
    cv2.destroyAllWindows()

cap.release()
cv2.destroyAllWindows()
