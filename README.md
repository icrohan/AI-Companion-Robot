# 🤖 AI Companion Robot

An AI-powered robotic assistant that combines **intent classification, RAG-based question answering, computer vision, and an interactive animated robot face**.

## 🚀 Features

* 🧠 Intent classification
* 📚 RAG-based question answering
* 👁️ Camera-based image/scene detection
* 🤖 Animated robot face with Listen, Talk, Think & Sleep modes
* 🌐 REST API communication with an AI backend
* 🎥 OpenCV camera integration

## 🛠️ Technologies

* Python
* OpenCV
* Tkinter
* Requests
* RAG
* Computer Vision
* REST APIs

## ⚙️ How It Works

```text
User Input
    ↓
Intent Classification
    ↓
 ┌───────────────┬────────────────┐
 │               │                │
Query       Detect Ahead       Other
 │               │
 ↓               ↓
RAG          Camera
 │               ↓
 ↓          Vision API
Answer      Description
```

## ▶️ Run

Install dependencies:

```bash
pip install requests opencv-python
```

Configure the backend server in:

```python
SERVER_URL = "http://YOUR_SERVER:5000"
```

Then run:

```bash
python robot_console.py
```

Type `exit` to stop.

## 🔮 Future Improvements

* Voice interaction
* Text-to-speech
* Face recognition
* Autonomous movement
* Sensor integration
* Physical robot integration

## 👨‍💻 Author

**Rohan Immidichetty**
