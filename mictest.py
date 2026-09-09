import speech_recognition as sr

rec = sr.Recognizer()
mic = sr.Microphone()

print("Speak something...")

with mic as source:
    rec.adjust_for_ambient_noise(source, duration=1)
    audio = rec.listen(source)

print("Captured audio, trying to recognize...")

try:
    text = rec.recognize_google(audio)
    print("You said:", text)
except Exception as e:
    print("ERROR:", e)
