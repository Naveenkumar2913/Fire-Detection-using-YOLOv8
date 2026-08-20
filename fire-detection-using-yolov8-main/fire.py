from ultralytics import YOLO
import cv2
import cvzone
import numpy as np
import threading
import winsound  # built-in on Windows
import os
import sms_notifier


# Play alarm sound (non-blocking)
def play_alarm():
    sound_file = "mixkit-facility-alarm-sound-999.wav"
    if os.path.isfile(sound_file):
        winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)


def main():
    cap = cv2.VideoCapture(0)
    model = YOLO("best.pt")

    # Determine which class indices correspond to 'fire' in the trained model
    fire_class_ids = []
    try:
        names = getattr(model, "names", {}) or {}
        # names may be a dict {0: 'person', 1: 'fire', ...}
        for k, v in names.items():
            if isinstance(v, str) and v.lower() == "fire":
                fire_class_ids.append(int(k))
        if not fire_class_ids:
            # also allow substring match as fallback
            for k, v in names.items():
                if isinstance(v, str) and "fire" in v.lower():
                    fire_class_ids.append(int(k))
    except Exception:
        fire_class_ids = []

    if not fire_class_ids:
        print("Warning: model does not contain a clear 'fire' class name. Falling back to 'fire' substring match where possible.")
    alarm_playing = False
    alert_sent = False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))
            results = model(frame)

            fire_detected = False

            for r in results:
                    for box in r.boxes:
                        try:
                            conf = float(box.conf[0])
                            cls = int(box.cls[0])

                            # 1) High confidence only
                            if conf < 0.75:
                                continue

                            # 1.5) Ensure the model predicted class corresponds to 'fire'
                            if fire_class_ids:
                                if cls not in fire_class_ids:
                                    continue
                            else:
                                # Fallback: check name string if available
                                try:
                                    name = model.names.get(cls, "").lower()
                                    if "fire" not in name:
                                        continue
                                except Exception:
                                    # if we cannot resolve name, skip (safer)
                                    continue

                            x1, y1, x2, y2 = map(int, box.xyxy[0])

                            # 2) Ignore tiny boxes (likely false positive)
                            box_w = max(1, x2 - x1)
                            box_h = max(1, y2 - y1)
                            box_area = box_w * box_h
                            if box_area < 5000:
                                continue

                            # 3) Check for fire color (orange/yellow)
                            roi = frame[y1:y2, x1:x2]
                            if roi.size == 0:
                                continue
                            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                            lower_fire = np.array([5, 80, 80])
                            upper_fire = np.array([40, 255, 255])
                            mask = cv2.inRange(hsv, lower_fire, upper_fire)
                            fire_pixels = int(cv2.countNonZero(mask))

                            # Use a relative threshold: require some minimum fraction of the box to match fire color
                            min_pixels = max(300, int(0.02 * box_area))
                            if fire_pixels < min_pixels:
                                continue

                            # Fire confirmed
                            fire_detected = True
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                            cvzone.putTextRect(frame, f"FIRE {int(conf*100)}%", (x1, y1 - 10), scale=1, thickness=2)
                        except Exception:
                            # Skip malformed box entries
                            continue

            # Alarm logic
            if fire_detected and not alarm_playing:
                alarm_playing = True
                threading.Thread(target=play_alarm, daemon=True).start()
                # Send SMS alert once per detected event (non-blocking)
                if not alert_sent:
                    alert_sent = True
                    try:
                        phones_env = os.getenv("ALERT_PHONES", "")
                        phones = [p.strip() for p in phones_env.split(",") if p.strip()]
                        if phones:
                            msg = "ALERT: Fire detected! Check camera feed immediately."
                            threading.Thread(target=sms_notifier.send_alert, args=(phones, msg), daemon=True).start()
                    except Exception:
                        # Don't let SMS errors break detection loop
                        pass

            if not fire_detected:
                alarm_playing = False
                alert_sent = False

            # Always show the frame (detected or not)
            cv2.imshow("Real-Time Fire Detection", frame)

            # Stop if user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            # Also stop if the window was closed by the user
            try:
                if cv2.getWindowProperty("Real-Time Fire Detection", cv2.WND_PROP_VISIBLE) < 1:
                    break
            except Exception:
                # Some OpenCV builds/platforms may raise here; ignore and continue
                pass
    except KeyboardInterrupt:
        # Allow clean exit on Ctrl-C
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
