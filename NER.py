from flair.data import Sentence
from flair.models import SequenceTagger
from calendar import month_name



def find_all_entity(voice_command):
    location = []
    monetary = []
    room_number = []
    date = []
    tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")
    # make example sentence
    sentence = Sentence(voice_command)
    # predict NER tags
    tagger.predict(sentence)
    # iterate over entities and print
    for entity in sentence.get_spans('ner'):
        entity_label = entity.get_label("ner").value
        if(entity_label == 'GPE' or entity_label =='LOC'):
            location.append(entity.text)
        elif(entity_label == 'MONEY'):
            monetary.append(entity.text)
        elif(entity_label == 'QUANTITY' or entity_label == 'CARDINAL'):
            room_number.append(entity.text)
        elif(entity_label == "DATE"):
            date.append(entity.text)

    return location, monetary, room_number, date

def find_location(voice_command):
    location = []
    tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")
    # make example sentence
    sentence = Sentence(voice_command)
    # predict NER tags
    tagger.predict(sentence)
    # iterate over entities and print
    for entity in sentence.get_spans('ner'):
        entity_label = entity.get_label("ner").value
        if(entity_label == 'GPE' or entity_label =='LOC'):
            location.append(entity.text)
    return location

def find_price(voice_command):
    price = []
    tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")
    # make example sentence
    sentence = Sentence(voice_command)
    # predict NER tags
    tagger.predict(sentence)
    # iterate over entities and print
    for entity in sentence.get_spans('ner'):
        entity_label = entity.get_label("ner").value
        if(entity_label == 'MONEY'):
            price.append(entity.text)
    return price
def find_room(voice_command):
    room_number = []
    tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")
    # make example sentence
    sentence = Sentence(voice_command)
    # predict NER tags
    tagger.predict(sentence)
    # iterate over entities and print
    for entity in sentence.get_spans('ner'):
        entity_label = entity.get_label("ner").value
        if(entity_label == 'QUANTITY' or entity_label == 'CARDINAL'):
            room_number.append(entity.text)
    return room_number

def find_date(voice_command):
    months = {m.lower() for m in month_name[1:]}
    month = next((word for word in voice_command.split() if word.lower() in months), None)
    date = []
    tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")
    # make example sentence
    sentence = Sentence(voice_command)
    # predict NER tags
    tagger.predict(sentence)
    # iterate over entities and print
    for entity in sentence.get_spans('ner'):
        entity_label = entity.get_label("ner").value
        if(entity_label == "DATE"):
            date.append(entity.text)
        elif(month):
            date.append(month)
    return date
   
  
