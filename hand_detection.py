import cv2
import mediapipe as mp
import time
import threading
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
time.sleep(1)

gesture_map = {
    0: "STOP",
    1: "YES",
    2: "NO",
    5: "HELLO",
    10: "THANK YOU"
}

sentence = []
last_gesture = ""
gesture_start_time = 0
HOLD_TIME = 1.0  # seconds

print("Press 'q' to quit | Press 'c' to clear sentence")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    total_fingers = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            h, w, _ = frame.shape
            lm_list = [(int(lm[i].x * w), int(lm[i].y * h)) for i in range(21)]

            if abs(lm_list[4][0] - lm_list[5][0]) > 40:
                total_fingers += 1
            for tip in [8, 12, 16, 20]:
                if lm_list[tip][1] < lm_list[tip - 2][1]:
                    total_fingers += 1

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    gesture = gesture_map.get(total_fingers, "UNKNOWN")

    current_time = time.time()

    if gesture != "UNKNOWN":
        if gesture != last_gesture:
            gesture_start_time = current_time
            last_gesture = gesture
        elif current_time - gesture_start_time > HOLD_TIME:
            sentence.append(gesture)
            threading.Thread(target=speak, args=(gesture,), daemon=True).start()
            last_gesture = ""
            time.sleep(0.5)

    # Display
    cv2.putText(frame, f"Gesture: {gesture}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)

    cv2.putText(frame, "Sentence:", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 2)

    cv2.putText(frame, " ".join(sentence[-6:]), (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 2)

    cv2.imshow("Sign Language Sentence Builder", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        sentence.clear()

cap.release()
cv2.destroyAllWindows()
