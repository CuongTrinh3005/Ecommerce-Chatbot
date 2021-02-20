import speech_recognition as sr
import pyttsx3
r = sr.Recognizer()
speaker = pyttsx3.init()

def speech_to_text(recognizer):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
    return text

def text_to_speech(engine, content):
    engine = pyttsx3.init()
    engine.say(content)
    engine.runAndWait()

# while(1):
#     try:
#         text = speech_to_text(r)
#         text_to_speech(speaker, text)
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
#     except sr.UnknownValueError as uv:
#         print("Unknow error occurred")