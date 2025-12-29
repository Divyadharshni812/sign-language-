import subprocess

def speak(text):
    if not text or text == "None":
        return

    # Escape quotes
    text = text.replace('"', '')

    command = f'''
    Add-Type -AssemblyName System.Speech;
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $speak.Speak("{text}");
    '''

    subprocess.Popen(
        ["powershell", "-Command", command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
