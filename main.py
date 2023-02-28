import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import ctypes
import time
import requests
import shutil
import re
import sys
from twilio.rest import Client
from ecapture import ecapture as ec
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'english_rp+f3')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour <= 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    
    speak("I am your Assistant Sara")

def username():
    speak("What should I call you sir?")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    speak("How can I help you, Sir?")

def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    except sr.UnknownValueError:
        print('....')
        command = takeCommand();
    return command

#TODO: This becomes a larger microservice
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    #Enable low security in gmail for this to work
    server.login('emailid', 'emailpass')
    server.sendmail('emailid', to , content)
    server.close()


if __name__ == '__main__':
    #clear = lambda: os.system('cls')

    #clear()
    wishMe()

    while True:

        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        #opening subreddits
        elif 'open reddit' in query:
            reg_ex = re.search('open reddit (.*)', query)
            url = 'https://www.reddit.com/'
            if reg_ex:
                subreddit = reg_ex.group(1)
                url = url + 'r/' + subreddit
            webbrowser.open(url)
            speak('The Reddit content has been opened for you Sir.')

        #opening any website
        elif 'open website' in query:
            reg_ex = re.search('open website (.+)', query)
            if reg_ex:
                domain = reg_ex.group(1)
                print(domain)
                url = 'http://www.' + domain
                webbrowser.open(url)
                speak('The website you have requested has been opened for you Sir.')
            else:
                pass


        elif 'time' in query:
            import datetime
            now = datetime.datetime.now()
            speak('Current time is %d hours %d minutes' % (now.hour, now.minute))

        elif 'quit' in query:
            speak('Bye Bye')
            sys.exit()

        else:
            speak("Sorry I didn't understand that")
