import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser

listener = sr.Recognizer()
#Creating an engine where machine can talk to user (using py text to speech(pyttsx3))
engine = pyttsx3.init()
#Changing Alexa voice into female voice
voices= engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def talk(text):
  # engine.say('I am your alexa')
  # engine.say('What can I do for you')
  engine.say(text)
  engine.runAndWait()

#If microphone is not able capture voice properly order
def take_command():
    command="" # Initialize command with a default value
    try:
        with sr.Microphone() as source:
           print('listening')
        #Creating a variable for listener listen the src (microphone)
           voice=listener.listen(source)
           command=listener.recognize_google(voice)
        #Detect whether alexa is present or not
           command=command.lower() #cmd for lowercase
           if 'alexa' in command:
            #Removing alexa word from text
              command=command.replace('alexa','').strip()
              # print(command)
           # talk(command) #Alexa same as you say
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        talk("Sorry, I didn't catch that.")
    except sr.RequestError:
        print("Network error. Please check your connection.")
        talk("Network error. Please check your connection.")
    except Exception as e:
        print(f"An error occurred: {e}")
    except:
      pass
    return command

def run_alexa():
    #cmd indicate it goes to take_command() functn
    command=take_command()
    print(command)
    if 'play' in command:
        song=command.replace('play','')
        talk('playing'+song)
        #by using imported libraries playing song from youtube
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time=datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is'+time)
    elif 'who is' in command:
        person = command.replace('who is','')
        try:
            info = wikipedia.summary(person, sentences=1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("There are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("I couldn't find any information on that.")
    elif 'date' in command:
        talk('sorry,You can get other person better than me')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        machine=(pyjokes.get_joke())
        talk(machine)
        print(machine)

    elif 'open' in command:
        # Open social media platforms
        if 'youtube' in command:
            talk('Opening YouTube')
            webbrowser.open('https://www.youtube.com')
        elif 'facebook' in command:
            talk('Opening Facebook')
            webbrowser.open('https://www.facebook.com')
        elif 'instagram' in command:
            talk('Opening Instagram')
            webbrowser.open('https://www.instagram.com')
        elif 'twitter' in command:
            talk('Opening Twitter')
            webbrowser.open('https://www.twitter.com')
        else:
            talk('I am not sure which platform you want to open. Please specify.')
    elif 'stop' in command or 'exit' in command:
        talk('Goodbye!')
        exit()  # Gracefully terminate the program

    else:
        talk('Please say command again.')

while True:
  run_alexa()
