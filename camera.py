import cv2
import numpy as np
import time
import os
import pandas as pd
from datetime import datetime
from PIL import Image

from predict import predict_image
from voice import speak
from voice_alerts import VOICE_ALERTS




def detect_possible_sign(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color masks
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    largest = None
    max_area = 0

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 600 and area > max_area:

            max_area = area
            largest = cnt

    if largest is None:
        return False, None

    
    perimeter = cv2.arcLength(
        largest,
        True
    )

    approx = cv2.approxPolyDP(
        largest,
        0.04 * perimeter,
        True
    )

    sides = len(approx)

    

    if sides not in [3, 4, 8] and sides < 10:
        return False, None

    x, y, w, h = cv2.boundingRect(largest)

   
    if w < 60 or h < 60:
        return False, None

    padding = 20

    x = max(0, x - padding)
    y = max(0, y - padding)

    w = min(frame.shape[1] - x, w + padding * 2)
    h = min(frame.shape[0] - y, h + padding * 2)

    return True, (x, y, w, h)



def save_prediction(result):

    os.makedirs("history", exist_ok=True)

    csv_file = "history/predictions.csv"

    new_data = pd.DataFrame({

        "Date": [datetime.now().strftime("%d-%m-%Y")],

        "Time": [datetime.now().strftime("%I:%M:%S %p")],

        "Traffic Sign": [result["sign"]],

        "Confidence": [round(result["confidence"], 2)]

    })

    if os.path.exists(csv_file):

        history = pd.read_csv(csv_file)

        if len(history) > 0:

            last = history.iloc[-1]

            if (
                last["Traffic Sign"] == result["sign"]
                and abs(
                    last["Confidence"]
                    - result["confidence"]
                ) < 1
            ):
                return

        history = pd.concat(
            [history, new_data],
            ignore_index=True
        )

    else:

        history = new_data

    history.to_csv(
        csv_file,
        index=False
    )



def start_camera():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print("Cannot open webcam")
        return

    last_prediction = 0

    current_result = None

    current_box = None

    last_spoken_sign = ""

    detected_sign = ""

    stable_count = 0

    REQUIRED_STABLE_FRAMES = 3

    prev_time = time.time()

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        current = time.time()

        fps = 1 / (current - prev_time)
        prev_time = current

        
        if current - last_prediction >= 1:

            last_prediction = current

            found, box = detect_possible_sign(frame)

            if found:

                current_box = box

                x, y, w, h = box

                crop = frame[y:y+h, x:x+w]

                if crop.size != 0:

                    crop = cv2.resize(
                        crop,
                        (128,128)
                    )

                    rgb = cv2.cvtColor(
                        crop,
                        cv2.COLOR_BGR2RGB
                    )

                    image = Image.fromarray(rgb)

                    current_result = predict_image(image)

                    

                    if (
                        current_result["confidence"] < 95
                        or current_result["sign"] == "No Traffic Sign Detected"
                    ):

                        current_result = None
                        current_box = None
                        detected_sign = ""
                        stable_count = 0
                        continue

                    

                    if current_result["sign"] == detected_sign:

                        stable_count += 1

                    else:

                        detected_sign = current_result["sign"]
                        stable_count = 1

                    if stable_count < REQUIRED_STABLE_FRAMES:
                        continue

                    sign = current_result["sign"]

                    

                    if (
                        sign in VOICE_ALERTS
                        and sign != last_spoken_sign
                    ):

                        speak(
                            VOICE_ALERTS[sign]
                        )

                        last_spoken_sign = sign

                    save_prediction(current_result)

                else:

                    current_result = None
                    current_box = None
                    detected_sign = ""
                    stable_count = 0

            else:

                current_result = None
                current_box = None
                detected_sign = ""
                stable_count = 0

        

        if current_box is not None:

            x, y, w, h = current_box

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                3
            )

        

        if current_result is not None:

            cv2.putText(
                frame,
                "DriveSense AI",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Traffic Sign : {current_result['sign']}",
                (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Confidence : {current_result['confidence']:.2f}%",
                (20, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Risk : {current_result['risk']}",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                f"Action : {current_result['action']}",
                (20, 155),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

        else:

            cv2.putText(
                frame,
                "No Traffic Sign Detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        

        cv2.putText(
            frame,
            f"FPS : {fps:.1f}",
            (20, frame.shape[0] - 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        

        now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

        cv2.putText(
            frame,
            now,
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        

        cv2.imshow("DriveSense AI Camera", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    start_camera()                