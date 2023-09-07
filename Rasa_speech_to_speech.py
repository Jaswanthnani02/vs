import speech_recognition as sr
import requests
from requests.exceptions import ConnectionError
import pyttsx3

def speech_to_text():
    
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... Say something!")
        recognizer.adjust_for_ambient_noise(source)  
        audio_data = recognizer.listen(source, timeout=3)  

    try:
        
        print("Recognizing...")
        text = recognizer.recognize_google(audio_data)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return None

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    sender = input("Enter your name: ")
    
    while True:
        user_input = speech_to_text()
        if user_input:
            print("Sending message now...")

            try:
                
                response = requests.post('http://localhost:5005/webhooks/rest/webhook',
                                         json={"sender": sender, "message": user_input})
                response.raise_for_status()  

                bot_message = ""
                
                for i in response.json():
                    bot_message = i['text']
                    print(bot_message)
                    text_to_speech(bot_message)  
                
                if bot_message == "Bye":
                    print("Exiting the conversation.")
                break  
                
            except ConnectionError:
                print("Connection error occurred. Please check your connection and try again.")
                break 