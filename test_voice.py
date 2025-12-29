import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Set speaking speed (optional)
engine.setProperty('rate', 160)

# IMPORTANT: Use VB-CABLE (CABLE Input)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

print("Speaking into VB-CABLE...")

engine.say("Hello. This is sign language voice output.")
engine.runAndWait()

print("Done speaking.")
