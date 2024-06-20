# app.py
from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)
light_status = {'status': 'off'}

@app.route('/light', methods=['GET', 'POST'])
def control_light():
    global light_status
    if request.method == 'POST':
        command = request.json.get('command', '')
        if 'turn on' in command.lower():
            light_status['status'] = 'on'
        elif 'turn off' in command.lower():
            light_status['status'] = 'off'
    return jsonify(light_status)

@app.route('/voice-command', methods=['POST'])
def voice_command():
    recognizer = sr.Recognizer()
    with sr.AudioFile(request.files['file']) as source:
        audio = recognizer.record(source)
    try:
        command = recognizer.recognize_google(audio)
        if 'turn on' in command.lower():
            light_status['status'] = 'on'
            response = "Turning on the light"
        elif 'turn off' in command.lower():
            light_status['status'] = 'off'
            response = "Turning off the light"
        else:
            response = "Command not recognized"
        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()
    except sr.UnknownValueError:
        response = "Could not understand audio"
    except sr.RequestError:
        response = "Could not request results"

    return jsonify({'status': light_status['status'], 'response': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

