import speech_recognition as sr
import pyttsx3
import requests
import json

def get_local_ai_response(prompt):
    url = "http://localhost:11434/api/generate"
    data = {"model": "mistral", "prompt": f"You are a medical assistant. Only answer questions related to medical topics. If a question is not related to medicine, politely refuse to answer. Question: {prompt}", "stream": False}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        response_json = response.json()
        return response_json.get("response", "I don't know the answer.").strip()
    return "Error: Could not connect to the local AI model. Make sure Ollama is running."

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print("You said:", text) 
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Could not request results. Check your internet connection."

def write_response_to_file(question, response):
    with open("shadow_responses.txt", "a", encoding="utf-8") as file:
        file.write(f"Question: {question}\nResponse: {response}\n{'-'*40}\n")

def shadow():
    print("Welcome to Shadow, your medical assistant. Ask me medical questions only. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if not user_input:
            user_input = listen()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            speak("Goodbye!")
            break
        
        response = get_local_ai_response(user_input)
        print("Shadow:", response)
        speak(response)
        write_response_to_file(user_input, response)

if __name__ == "__main__":
    shadow()
