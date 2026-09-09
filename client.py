import requests, threading, queue, time, os, cv2, serial
import speech_recognition as sr
import pyttsx3
from face import *

SERVER_URL = "http://10.45.10.36:5000"
COOLDOWN = 1.2

is_speaking = False
last_spoken = 0

cmd_queue = queue.Queue()

# ================= FACE THREAD =================
threading.Thread(target=run_face, daemon=True).start()
sleep_expression()

# ================= ARDUINO THREAD =================
def arduino_loop():
    try:
        ser = serial.Serial("COM9", 9600, timeout=1)
        while True:
            cmd = cmd_queue.get()
            ser.write((cmd + "\n").encode())
    except:
        print("Arduino NOT connected, skipping motor control")

threading.Thread(target=arduino_loop, daemon=True).start()

# ================= SPEAK =================
engine = pyttsx3.init()
engine.setProperty("rate", 180)

def speak(text):
    global is_speaking, last_spoken
    is_speaking = True
    talk_expression()

    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

    last_spoken = time.time()
    is_speaking = False
    sleep_expression()

# ================= LISTEN =================
rec = sr.Recognizer()
mic = sr.Microphone()  # mic works (verified)

def listen():
    listen_expression()

    while is_speaking or time.time() - last_spoken < COOLDOWN:
        time.sleep(0.1)

    with mic as src:
        rec.adjust_for_ambient_noise(src, duration=0.5)
        try:
            audio = rec.listen(src, timeout=5, phrase_time_limit=5)
        except:
            return ""

    try:
        text = rec.recognize_google(audio).lower()
        print("You:", text)
        return text
    except sr.UnknownValueError:
        sleep_expression()
        return ""
    except sr.RequestError:
        speak("Speech service error")
        return ""

# ================= SERVER =================
def classify(text):
    think_expression()
    try:
        return requests.post(
            f"{SERVER_URL}/classify",
            json={"text": text},
            timeout=5
        ).json()["class_name"]
    except:
        return ""

def rag(text):
    think_expression()
    time.sleep(0.5)
    try:
        r = requests.post(
            f"{SERVER_URL}/rag",
            json={"query": text},
            timeout=6
        ).json()
        speak(r.get("answer", "No answer"))
    except:
        speak("Server error")

def capture_and_send():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        speak("Camera error")
        return

    img_path = "capture.jpg"
    cv2.imwrite(img_path, frame)

    try:
        with open(img_path, "rb") as f:
            r = requests.post(f"{SERVER_URL}/des", files={"image": f})
        speak(r.json().get("description", "Nothing detected"))
    except:
        speak("Vision server error")

    os.remove(img_path)

# ================= MOTOR MAP =================
def motor(intent):
    if intent == "MOVE_FORWARD": cmd_queue.put("F")
    elif intent == "MOVE_BACKWARD": cmd_queue.put("B")
    elif intent == "MOVE_LEFT": cmd_queue.put("L")
    elif intent == "MOVE_RIGHT": cmd_queue.put("R")
    elif intent == "STOP": cmd_queue.put("S")

# ================= MAIN =================
speak("System online. You can speak now.")

while True:
    text = listen()
    if not text:
        continue

    if text in ["hello", "hi"]:
        speak("Hello I am ready")
        continue

    if "exit" in text:
        speak("Stopping")
        break

    intent = classify(text)
    print("Intent:", intent)

    if intent == "Query":
        rag(text)
    elif intent == "Detect Ahead":
        capture_and_send()
    else:
        motor(intent)
