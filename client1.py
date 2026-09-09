import requests
import cv2
import os

SERVER_URL = "http://10.32.6.236:5000"


def classify(text):
    r = requests.post(
        f"{SERVER_URL}/classify",
        json={"text": text}
    )
    return r.json().get("class_name", "")


def send_to_rag(text):
    r = requests.post(
        f"{SERVER_URL}/rag",
        json={"query": text}
    )
    return r.json().get("answer", "No answer")


def capture_and_send():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Camera error")
        return

    img_path = "capture.jpg"
    cv2.imwrite(img_path, frame)

    try:
        with open(img_path, "rb") as f:
            r = requests.post(
                f"{SERVER_URL}/des",
                files={"image": f}
            ).json()

        print("Bot:", r.get("description", "No description"))

    except:
        print("Vision server error")

    os.remove(img_path)


print("Robot Console Ready")
print("Type 'exit' to stop")
print("-" * 40)

while True:
    text = input("You: ").strip()

    if text.lower() == "exit":
        print("Stopping...")
        break

    try:
        intent = classify(text)
        print("Intent:", intent)

        if intent == "Query":
            print("Bot:", send_to_rag(text))

        elif intent == "Detect Ahead":
            capture_and_send()

        else:
            print("Bot:", intent)

    except Exception as e:
        print("Server error:", e)