import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import json
from bs4 import BeautifulSoup as soup 
import wikipedia
import random
from time import strftime 

def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def allisonResponse(audio):
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

def assistant(command):

    #opening subreddits
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        allisonResponse('The Reddit content has been opened for you Sir.')

    #opening any website
    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'http://www.' + domain
            webbrowser.open(url)
            allisonResponse('The website you have requested has been opened for you Sir.')
        else:
            pass
    
    #sending emails
    elif 'email' in command:
        allisonResponse('Who is the recipient?')
        recipient = myCommand()
        names, emails = get_email_contacts("/contacts.txt")
    #This part needs to become more generic, this was only a specific usecase
        if recipient in names:
            index = names.index(recipient)
            allisonResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('bradleybsf12@gmail.com', 'TEMOP')
            mail.sendmail('bradleybsf12@gmail.com', emails[index], content)
            mail.close()
            allisonResponse('Email has been sent successfully.')
        else:
            allisonResponse('I don\'t know what you mean!')

    #launch any system application, the example was only good for apple. Need a more generic solution
    # elif 'launch' in command:
    #     reg_ex = re.search('launch (.*)', command)
    #     if reg_ex:
    #         appname = reg_ex.group(1)
    #         appname1 = appname+".exe"
    #         subprocess.Popen(["open", "-n", "/App"])

    elif 'forecast for today' in command:
        reg_ex = re.search('forecast for today in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM('1a367db7eabbb7d64fd68fb1fe87b044')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='fahrenheit')
            allisonResponse('Current weather in %s is %s. The high for today is %0.2f and the low is' + 
            '%0.2f degrees' % (city, k, x['temp_max'], x['temp_min']))

    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        allisonResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

    #Greet Allison
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            allisonResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            allisonResponse('Hello Sir. Good Afternoon')
        else:
            allisonResponse('Hello sir. Good evening')

    #to terminate the program
    elif 'quit' in command:
        allisonResponse('Bye Bye')
        sys.exit()
    
    #News feed, this may not work
    elif 'news for today' in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client = url(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")
            for news in news_list[:15]:
                allisonResponse(news.title.text.encode('utf-8'))
        except Exception as e:
            print(e)

    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                allisonResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
            allisonResponse(e)

def get_email_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

while True:
    assistant(myCommand())

