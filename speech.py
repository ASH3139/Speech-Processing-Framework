import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print("Car:", text)
    engine.say(text)
    engine.runAndWait()


def get_best_mic():
    mics = sr.Microphone.list_microphone_names()

    for i, mic in enumerate(mics):
        name = mic.lower()
        if "headset" in name or "buds" in name or "bluetooth" in name:
            return i

    for i, mic in enumerate(mics):
        if "microphone" in mic.lower():
            return i

    return None


def get_voice():

    r = sr.Recognizer()

    mic_index = get_best_mic()

    if mic_index is None:
        print("No mic found")
        return ""

    try:
        with sr.Microphone(device_index=mic_index) as source:

            print("Listening...")

            audio = r.listen(source, timeout=5)

    except Exception as e:
        print("Mic Error:", e)
        return ""

    try:
        text = r.recognize_google(audio)
        print("Heard:", text)
        return text.lower()
    except:
        print("Nothing recognized")
        return ""