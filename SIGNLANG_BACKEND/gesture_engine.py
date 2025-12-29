import cv2
import mediapipe as mp
import time

# ================== MEDIAPIPE SETUP ==================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

# ================== CAMERA ==================
cap = cv2.VideoCapture(0)

# ================== SHARED STATE ==================
CURRENT_GESTURE = "None"

# ================== FINGER COUNT ==================
def count_fingers(hand_landmarks, handedness):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if handedness == "Right":
        fingers.append(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x)
    else:
        fingers.append(hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x)

    # Other fingers
    for tip in tips[1:]:
        fingers.append(
            hand_landmarks.landmark[tip].y <
            hand_landmarks.landmark[tip - 2].y
        )

    return sum(fingers)

# ================== GESTURE MAP ==================
def map_gesture(count):
    return {
        1: "HELLO",
        2: "YES",
        3: "NO",
        4: "THANK YOU",
        5: "PLEASE"
    }.get(count, "None")

# ================== MAIN CAMERA LOOP ==================
def run():
    global CURRENT_GESTURE

    print("✋ Camera running — show gesture (press Q to exit)")

    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        gesture = "None"

        if result.multi_hand_landmarks and result.multi_handedness:
            for handLms, handType in zip(
                result.multi_hand_landmarks,
                result.multi_handedness
            ):
                mp_draw.draw_landmarks(
                    frame, handLms, mp_hands.HAND_CONNECTIONS
                )

                hand_label = handType.classification[0].label
                fingers = count_fingers(handLms, hand_label)
                gesture = map_gesture(fingers)

        CURRENT_GESTURE = gesture

        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("SIGNLANG - Gesture Engine", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
