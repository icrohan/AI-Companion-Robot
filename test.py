import cv2
import serial
import requests
import speech_recognition as sr
import pyttsx3

# text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

print("✅ Everything installed correctly")
speak("Everything installed correctly")
