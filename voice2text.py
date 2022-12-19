import speech_recognition as sr
import NER
import pyttsx3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser
import time
import pandas as pd
import os 
import audioop
# import pyaudio as pa
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pprint
from nltk import Tree
import pdb
# import api_calls

def prepare_text(string):
    sentences = nltk.sent_tokenize(string)
    sentences = [nltk.word_tokenize(sent) for sent in sentences] 
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    sentences = [NPChunker.parse(sent) for sent in sentences]
    return sentences

def initiate_dialogue():
    engine = pyttsx3.init()
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0" 
    engine.setProperty('voice', voice_id) 
    engine.say("Hola! I am your Virtual Realtor. How can I help you today?") 
    engine.runAndWait()
    ########################################################    
    
    string = userCommand()    
    print("Command:", string)
    location, price, room_number, date = NER.find_all_entity(string)
    
    if(location):
        location = ','.join(location)
        print("Location:", location)
    else:
        while(1):
            engine.say("What is the location you are looking for?") 
            engine.runAndWait()
            user_command = userCommand() 
            location = NER.find_location(user_command)
            if(location):
                location = ','.join(location)
                print("Location:", location)
                break
    ##########################################
    if(price):
        price = ','.join(price)
        print("Price:", price)
    else:
        while(1):
            engine.say("What is your preferred price range?") 
            engine.runAndWait()
            user_command = userCommand() 
            price = NER.find_price(user_command)
            if(price):
                price = ','.join(price)
                print("Price:", price)
                break


    if(room_number):
        room_number = ','.join(room_number)
        print("Room Number:", room_number)
    else:
        while(1):
            engine.say("What is your preferred number of rooms?") 
            engine.runAndWait()
            user_command = userCommand() 
            room_number = NER.find_room(user_command)
            if(room_number):
                room_number = ','.join(room_number)
                print("Room:", room_number)
                break
 
    if(date):
            date = ','.join(date)
            print("Date:", date)
    else:
            while(1):
                engine.say("When are you looking to move in?") 
                engine.runAndWait()
                user_command = userCommand() 
                date = NER.find_date(user_command)
                if(date):
                    date = ','.join(date)
                    print("Date:", date)
                    break
    return location, price, room_number, date
    
##############################################################################

# This function is to convert voice speech into string text
##############################################################################
def speechToText(r, source2):
    try:
        r.adjust_for_ambient_noise(source2, duration=0.2)
        audio2 = r.listen(source2)
        myText = r.recognize_google(audio2)
        myText = myText.lower()
        return myText
                
        #print("Did you say " + myText)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
            
    except sr.UnknownValueError:
        print("Unknown error occured")
##############################################################################        

def userCommand():
    r = sr.Recognizer() # Creating a recognizer instance
    # print(sr.Microphone.list_microphone_names())
    mic = sr.Microphone(device_index=0) # index = 0 is for Built-in Microphone 
    
    result = ''
    with mic as source:
        audio = r.listen(source)
        
        """
            recognize_google is speech recognition model created by Google
        """
        result = r.recognize_google(audio)
        
    #print(result)
    return result


def run_voice2text():
    # Setting up computer in-built audio voice for the prompt
    #########################################################
    engine = pyttsx3.init()
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0" 
    engine.setProperty('voice', voice_id) 
    ########################################################    
    location, price, room, date = initiate_dialogue()
    print("Location:", location, ", Price:", price, ", Room Number:", room, ", Date:", date)
    text = "Okay, I will find an apartment of " + room+" rooms at"+ location+ " available from"+ date
    engine.say(text)
    engine.runAndWait()
    # print(sent_parse(string)) # pass the converted string text of the user voice to the regex parser. It will extract food items from the string text
    return location, price, room, date
            
    
    
    
    
