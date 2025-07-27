from http.client import responses
import random
import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import pyjokes
import webbrowser
import time
import requests

# Initialize the speech engine(System side audio)
engine = pyttsx3.init()
voices = engine.getProperty('voices') #Retrives available system voice(male,female,accent)
engine.setProperty('voice', voices[1].id) # Select female voice 
engine.setProperty('rate', 140) #Speech Speed 

def talk(text):
    #Converts text to speech
    print(f"Assistant:{text}")
    engine.say(text)
    engine.runAndWait()
  
def write(text):
    print(f"Assistant:{text}")

def take_command():
    """Captures voice or text command based on user choice"""
    print("\nChoose input method:")
    print("1. Speak")
    print("2. Type")
    method = input("Enter 1 or 2: ")

    if method == "1":
        listener = sr.Recognizer() #Create obj
        with sr.Microphone() as source: #open microphone to listen
            listener.adjust_for_ambient_noise(source) #Improve filtering in background noise
            print("Listening...")
            try:
                voice = listener.listen(source) #Records the usr voice
                command = listener.recognize_google(voice).lower() #convert audio to text
                print("You said:", command)
                return command
            except sr.UnknownValueError:
                talk("Sorry, I couldn't understand. Please repeat.")
            except sr.RequestError:
                talk("Network error. Please check your connection.")
            return ""
    elif method == "2":
        command = input("Type your command: ").lower()
        return command
    else:
        talk("Invalid choice.")
        return ""


def get_time():
    #Tells the current time
    time_now = datetime.datetime.now().strftime('%I:%M %p') # current time strftime->String format time
    talk(f"The time is {time_now}")

def get_date(): #default show current date no observation is required
    #Tell me current date
    date_today=datetime.datetime.now().strftime('%B:%d %Y')
    talk(f"The date is {date_today}")

def play_music(command): #Parameter present bcs to observe whether have used particular song or not
    #Plays music on YouTube
    song = command.replace("play", "").strip()
    talk(f"Playing {song}")
    pywhatkit.playonyt(song)

def tell_joke():
    #Tells a joke
    joke = pyjokes.get_joke()
    talk(joke)

def open_website(command):
    #Opens requested website
    websites = {
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "news": "https://www.bbc.com/news",
        "weather": "https://www.weather.com"
    }
    for site in websites:
        if site in command:
            talk(f"Opening {site}")
            webbrowser.open(websites[site])
            return
    talk("Sorry, I can't open that site.")

def emergency_contact():
    #Triggers an emergency alert
    talk("Calling emergency contact now.")
    # You can integrate Twilio API or phone call feature here


def set_reminder():

    talk("What would you like me to remind you about?")
    reminder = take_command()

    if reminder:
        talk("When should I remind you?")
        time_info = take_command()
        if time_info:
            date_today=datetime.datetime.now().strftime('%B %d, %Y')
            confirmation = f"Reminder set for '{reminder}' at '{time_info}'."
            talk(confirmation)
            print(confirmation)
            # Save the reminder to a text file 
            with open("reminders.txt", "a") as file:
                file.write(f"{reminder} at {time_info}\n")
        else:
            talk("I didn't catch the time.")
    else:
        talk("I didn't catch the reminder.")


def get_weather():
    """Fetches weather details (dummy implementation, replace with API)"""
    talk("Fetching the weather...")
    # Replace with API call to OpenWeatherMap or similar service
    talk("The weather today is sunny with a temperature of 25 degrees Celsius.")


def random_chat(command):
    """Responds based on user's emotion or situation"""
    command = command.lower()

    if any(word in command for word in ["sad", "depressed", "unhappy", "lonely"]):
        talk("I'm really sorry to hear that. You're not alone. I'm here for you.")

    elif any(word in command for word in ["happy", "excited", "good", "great"]):
        talk("That's wonderful to hear! I'm so happy for you.")

    elif any(word in command for word in ["tired", "sick", "unwell", "weak"]):
        talk("Make sure to get some rest. Should I set a reminder to take medicine?")

    elif any(word in command for word in ["angry", "frustrated", "annoyed"]):
        talk("It’s okay to feel that way sometimes. Want to hear a joke or listen to music?")

    elif any(word in command for word in ["bored", "nothing to do"]):
        talk("How about a joke or a song to lighten the mood?")

    else:
        talk("I'm here with you. Let me know how I can help.")


def run_assistant():
    while True:
        command = take_command()
        if not command:
            continue
        if "time" in command or "current time" in command:
            get_time()
        elif "date" in command or "current date" in command:
            get_date()
        elif "play" in command:
            play_music(command)
        elif "joke" in command:
            tell_joke()
        elif "open" in command:
            open_website(command)
        elif "emergency" in command or "help" in command:
            emergency_contact()
        elif "reminder" in command:
            set_reminder()
        elif "weather" in command:
            get_weather()
        elif any(word in command for word in["sad","happy","tired","bored","angry","sick","lonely","excited", "frustrated"]):
            random_chat(command)
        elif "exit" in command or "stop" in command:
            talk("Goodbye! Stay safe.")
            break
        else:
            talk("I'm not sure how to help with that. Please try again.")

# Start the assistant
run_assistant()
