import anthropic
import pyttsx3
import speech_recognition as sr

import os
import requests
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import json
from dotenv import load_dotenv

#load environment variables from .env file
load_dotenv()

#access the variables
user = os.getenv('USER')
botname = os.getenv('BOTNAME')

#initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_user_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print('Recognizing...')
        query = recognizer.recognize_google(audio, language='en-in').lower()
        print(f"You said: {query}")
        return query
    except Exception as e:
        speak('Sorry, I could not understand. Could you please say that again?')
        return None

def check_stop_intent(text):
    #list of phrases that indicate stopping
    stop_phrases = ["stop", "exit", "goodbye", "that's it", "end", "quit"]
    return any(phrase in text for phrase in stop_phrases)

def get_claude_response(query):
    client = anthropic.Client(api_key="your-anthropic-api-key")
    response = client.completions.create(
        model="claude-instant",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message['content']

def open_cmd():
    os.system('start cmd')

def open_discord():
    os.system('start discord')

def open_camera():
    os.system('start microsoft.windows.camera:')

def open_calculator():
    os.system('calc')

def find_my_ip():
    ip = requests.get('https://api64.ipify.org?format=json').json()
    return ip["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+{number}", message)

def send_email(receiver_address, subject, message):
    try:
        sender_address = 'your-email@gmail.com'
        sender_password = 'your-password'
        msg = MIMEMultipart()
        msg['From'] = sender_address
        msg['To'] = receiver_address
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_password)
        text = msg.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        return True
    except Exception as e:
        print(e)
        return False

def get_random_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts."
    ]
    return random.choice(jokes)

def get_random_advice():
    advices = [
        "Don't count the days, make the days count.",
        "Your limitation—it's only your imagination.",
        "Push yourself, because no one else is going to do it for you."
    ]
    return random.choice(advices)

def get_trending_movies():
    movies = ["Movie 1", "Movie 2", "Movie 3"]  # Replace with actual API call if needed
    return movies

def get_latest_news():
    news = ["News 1", "News 2", "News 3"]  # Replace with actual API call if needed
    return news

def get_weather_report(city):
    api_key = "your-weather-api-key"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url).json()
    weather = response['weather'][0]['description']
    temperature = response['main']['temp']
    feels_like = response['main']['feels_like']
    return weather, temperature, feels_like

def main():
    # Greet the user with the bot name
    speak(f"Hello {user}, i am  {botname}. How can I assist you today?")
    
    while True:
        query = take_user_input()
        if query is None:
            continue

        if 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia, sir?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(results)

        elif 'youtube' in query:
            speak('What do you want to play on Youtube, sir?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('What do you want to search on Google, sir?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak('On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message sir?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")

        elif "send an email" in query:
            speak("On what email address do I send sir? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject sir?")
            subject = take_user_input().capitalize()
            speak("What is the message sir?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email sir.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

        elif 'joke' in query:
            speak(f"Hope you like this one sir")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen sir.")
            print(joke)

        elif "advice" in query:
            speak(f"Here's an advice for you, sir")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen sir.")
            print(advice)

        elif "trending movies" in query:
            trending_movies = get_trending_movies()
            speak(f"Some of the trending movies are: {', '.join(trending_movies)}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(*trending_movies, sep='\n')

        elif 'news' in query:
            latest_news = get_latest_news()
            speak(f"I'm reading out the latest news headlines, sir")
            for headline in latest_news:
                speak(headline)
            speak("For your convenience, I am printing it on the screen sir.")
            print(*latest_news, sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

        elif 'exit' in query or 'stop' in query:
            speak("Alright sir, I am shutting down the system. Have a great day!")
            break

if __name__ == "__main__":
    main()

