import time
import threading

# ================== IMPORT PROJECT MODULES ==================
import gesture_engine          # camera + mediapipe (runs in main thread)
from tts_engine import speak   # Windows PowerShell TTS (non-blocking)

# ================== GLOBAL STATE ==================
last_spoken = ""
last_time = 0
COOLDOWN = 2  # seconds

print("🚀 SIGNLANG SYSTEM STARTED")
print("🟢 Camera running | 🟢 Voice enabled")
print("👉 Press Q in camera window to exit")

# ================== VOICE + EXTENSION LOOP ==================
def voice_and_output_loop():
    global last_spoken, last_time

    while True:
        gesture = gesture_engine.CURRENT_GESTURE

        if gesture and gesture != "None" and gesture != last_spoken:
            now = time.time()
            if now - last_time > COOLDOWN:
                # Speak gesture
                speak(gesture)

                # Save for Chrome extension / logging
                with open("current_gesture.txt", "w") as f:
                    f.write(gesture)

                last_spoken = gesture
                last_time = now

        time.sleep(0.1)

# ================== START VOICE THREAD ==================
voice_thread = threading.Thread(
    target=voice_and_output_loop,
    daemon=True
)
voice_thread.start()

# ================== RUN CAMERA IN MAIN THREAD ==================
try:
    gesture_engine.run()
except KeyboardInterrupt:
    print("\n🛑 SIGNLANG STOPPED SAFELY")
