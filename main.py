import speech_recognition as sr
import webbrowser as web
import pyttsx3
import musicLibrary
from mistralai import Mistral



recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()
def aiProcess(command):
    client = Mistral(
    api_key="sVmBpMq1KU84ZjfWxH8g6jVjHCh77bzl")
    chat_response = client.chat.complete(
        model= "mistral-small-latest",
        messages = [
            {
                "role": "system",
                "content": "You are Jarvis, a smart, voice-activated AI assistant. Handle tasks like Alexa or Google Assistant: set reminders, control devices, answer questions, give updates. Always reply in a short, clear, and concise way. Avoid long explanations. Be polite, accurate, and efficient. Ask for clarification if needed.",
            },
            {
                "role":"user", 
                "content":command
            }
        ]
    )
    return chat_response.choices[0].message.content

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        speak("Opening Google")
        web.open("https://google.com")
    elif "open facebook" in c:
        speak("Opening Facebook")
        web.open("https://facebook.com")
    elif "open youtube" in c:
        speak("Opening YouTube")
        web.open("https://youtube.com")
    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        web.open("https://linkedin.com")
    elif "open github" in c:
        speak("Opening Github")
        web.open("https://github.com")
    elif c.lower().startswith("play"):
        songs = c.lower().split(" ")[1]
        link = musicLibrary.music[songs]
        web.open(link)
    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)

                try:
                    word = recognizer.recognize_google(audio)
                    print(f"Heard: {word}")

                    if word.lower() == "jarvis":
                        speak("Yes Nehan")
                        with sr.Microphone() as source:
                            recognizer.adjust_for_ambient_noise(source, duration=0.5)
                            print("Jarvis Active. Listening for command...")
                            audio = recognizer.listen(source)
                            try:
                                command = recognizer.recognize_google(audio)
                                print(f"Command: {command}")
                                processCommand(command)
                            except sr.UnknownValueError:
                                speak("Sorry, I didn't catch that.")
                except sr.UnknownValueError:
                    print("Couldn't understand wake word. Try again.")
        except sr.WaitTimeoutError:
            print("Listening timed out, restarting...")
        except KeyboardInterrupt:
            speak("Shutting down.")
            break
        except Exception as e:
            print(f"Exception occurred: {e}")
