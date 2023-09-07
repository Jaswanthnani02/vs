from flask import Flask, render_template, request
import speech_recognition as sr
import requests
from requests.exceptions import ConnectionError
import pyttsx3

app = Flask(__name__)

def speech_to_text():
    recognizer = sr.Recognizer()

    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Listening... Say something!")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio_data = recognizer.listen(source, timeout=3)  # Set a timeout of 5 seconds


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sender = request.form['sender']
        return render_template('index.html', sender=sender)
    return render_template('index.html')

@app.route('/get_response/<sender>/<user_input>', methods=['GET'])
def get_response(sender, user_input):
    try:
        response = requests.post('http://localhost:5005/webhooks/rest/webhook',
                                 json={"sender": sender, "message": user_input})
        response.raise_for_status()

        bot_message = ""
        for i in response.json():
            bot_message = i['text']
            text_to_speech(bot_message)
        return bot_message
    
    except ConnectionError:
        return "Connection error occurred. Please check your connection and try again."

if __name__ == "__main__":
    app.run(debug=True)
