import speech_recognition as sr
from time import ctime
import time
import wikipedia
from gtts import gTTS
import requests
import os
from bs4 import BeautifulSoup
from googlesearch import search
import sys


def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


def find_news():

    content = "The latest news is "
    # the target we want to open
    url = 'http://www.hindustantimes.com/top-news'
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            print("Successfully Scrapped")
            print("The news is as follow :-\n")
            soup = BeautifulSoup(resp.text, 'html.parser')
            # print(soup.prettify())
            l = soup.find("ul", attrs={'class': 'latest-news-bx more-latest-news more-separate'})
            #print(l.prettify())
            for i in l.findAll("a"):
                content += i.text
                content += "."
                content += ","
                #content += "Next News"

            content = content.replace("read more", " ")
            return content
        else:
            content = "Error Occurred"
            return content
    except:
        print("Error Here")
    # http_response 200 means OK status


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        speak("Could not understand what you are asking for..")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data


def ask_wiki(query):
    wikipedia.set_lang("en")
    info = wikipedia.summary(query, sentences=2)
    return info


def scrape_this(url):
    url_ans = url
    ans = " "
    try:
        resp = requests.get(url_ans)
        if resp.status_code == 200:
            print("Successfully Scrapped")
            soup = BeautifulSoup(resp.text, 'html.parser')
            l = soup.find("div", attrs={'class': 'ui_qtext_expanded'})
            for i in l.findAll("span"):
                ans += i.text
            return ans
        else:
            ans = "Error Occured"
            return ans
    except:
        print("Error in reaching the page")


def ask_quora(query):
    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
        url = j
        print(url)
        ret = scrape_this(url)
        return ret


def jarvis(data):
    if "how are you" in data:
        speak("I am fine")

    if "what time is it" in data:
        speak(ctime())

    if "where is" in data:
        data = data.split(" ")
        location = data[2]
        speak("Hold on Friend, I will show you where " + location + " is.")
        os.system("firefox quantum https://www.google.com/maps/place/" + location + "/&amp;")

    if "news" in data:
        news_content = find_news()
        speak(news_content)

    if "what is" in data:
        query = data
        query = query.replace("what is ", "")
        wiki_says = ask_wiki(query)
        speak(wiki_says)

    if "who is" in data:
        query = data
        query = query.replace("who is ", "")
        wiki_says = ask_wiki(query)
        speak(wiki_says)

    else:
        try:
            quora_reply = ask_quora(data)
            speak(quora_reply)
        except:
            speak("Sorry! I am unable to find an answer for you..")


# initialization

time.sleep(1)
speak("Hi Friend, what can I do for you?")
while 1:
    data = recordAudio()
    jarvis(data)
    speak("I am done.. What Can I do for you now?")

