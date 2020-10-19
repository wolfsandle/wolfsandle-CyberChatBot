# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 17:23:33 2020

MS548 
@author: CWolfsandle
"""

import bs4 as bs #Beautiful Soup is a Python library for pulling data out of HTML and XML files.
import urllib.request #Urllib module is the URL handling module for python
import re
import nltk #Natural Language Toolkit. NLTK is a leading platform for building Python programs to work with human language data.
import random
import string
import tkinter #GUI library
from tkinter import * #GUI library

raw_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Computer_security')
raw_data = raw_data.read()

html_data = bs.BeautifulSoup(raw_data, 'lxml')

all_paragraphs = html_data.find_all('p')

article_content = ""

for p in all_paragraphs:
    article_content += p.text

article_content = article_content.lower()  # converts to lowercase

article_content = re.sub(r'\[[0-9]*\]', ' ', article_content)
article_content = re.sub(r'\s+', ' ', article_content)

sentence_list = nltk.sent_tokenize(article_content)
article_words = nltk.word_tokenize(article_content)

nltk.download('punkt') # This tokenizer divides a text into a list of sentences by using an unsupervised algorithm to build a model for abbreviation words, collocations, and words that start sentences.
nltk.download('wordnet') #WordNet is a NLTK corpus reader

lemmatizer = nltk.stem.WordNetLemmatizer()


def LemmatizeWords(words):
    return [lemmatizer.lemmatize(word) for word in words]


remove_punctuation = dict((ord(punctuation), None) for punctuation in string.punctuation)


def RemovePunctuations(text):
    return LemmatizeWords(nltk.word_tokenize(text.lower().translate(remove_punctuation)))


greeting_input_texts = ("hey", "hi", "hello", "morning", "evening", "afternoon", "greetings")
greeting_reply_texts = ["Hey", "Hi, how are you?", "*nods*", "Hello there", "Hello", "Welcome, how can I help you?"]


def reply_greeting(text): #chooses a random greeting reply
    for word in text.split():
        if word.lower() in greeting_input_texts:
            return random.choice(greeting_reply_texts)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def give_reply(user_input): #determines how similar a response is to the original input
    chatbot_response = ''
    sentence_list.append(user_input)
    word_vectors = TfidfVectorizer(tokenizer=RemovePunctuations)
    vecrorized_words = word_vectors.fit_transform(sentence_list)
    similarity_values = cosine_similarity(vecrorized_words[-1], vecrorized_words)
    similar_sentence_number = similarity_values.argsort()[0][-2]
    similar_vectors = similarity_values.flatten()
    similar_vectors.sort()
    matched_vector = similar_vectors[-2]
    if (matched_vector == 0):
        chatbot_response = chatbot_response + "I'm sorry! I don't understand."
        return chatbot_response
    else:
        chatbot_response = chatbot_response + sentence_list[similar_sentence_number]
        return chatbot_response


def submit(): #main function that handles interaction with user
    
    ChatLog.config(state=NORMAL)
    ChatLog.tag_config('bot', foreground="dim gray", font=('bold'))
    ChatLog.tag_config('user', foreground="midnight blue", font=('bold'))

    user_input = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    print("User: " + user_input)
    ChatLog.insert(END, "User: " + user_input + '\n', 'user')
    
    continue_discussion = True

    if (continue_discussion == True):
        user_input = user_input.lower()
        if (user_input != 'bye'):
            if (user_input == 'thanks' or user_input == 'thank you very much' or user_input == 'thank you'):
                continue_discussion = False
                print("CyberBOT: Most welcome")
                ChatLog.insert(END, "CyberBOT: You are welcome" + '\n', 'bot')
            else:
                if (user_input == 'topics'): 
                    return_topics()
                else:
                    replygreeting = reply_greeting(user_input)
                    if (replygreeting != None):
                        print("CyberBOT: " + replygreeting)
                        ChatLog.insert(END, "CyberBOT: " + (replygreeting) + '\n', 'bot')
                    else:
                        replytopic = give_reply(user_input)
                        print("CyberBOT: ", end="")
                        print(replytopic)
                        ChatLog.insert(END, "CyberBOT: " + (replytopic) + '\n', 'bot')
                        sentence_list.remove(user_input)
        else:
            continue_discussion = False
            
            print("CyberBOT: Take care, bye ..")
            ChatLog.insert(END, "CyberBOT: Thanks for chatting, bye!" + '\n', 'bot')
    ChatLog.yview(END)   
    ChatLog.config(state=DISABLED)        

def clear(): #clears input box and chatlog

    ChatLog.config(state=NORMAL)    
    EntryBox.delete(1.0, END)
    ChatLog.delete(1.0, END)
    welcome()
    ChatLog.config(state=DISABLED)
    print("clear")
    
def quitprogram(): #quits the program
    base.destroy()
    print("clear")

def welcome(): #prints the welcome message
    ChatLog.tag_config('welcome', foreground="dim gray", font=('bold'))
    ChatLog.insert(END, 'Welcome!' + '\n\n', 'welcome')
    ChatLog.insert(END, 'I am a Cyber Security Bot. I can help you learn about' + '\n\n', 'welcome')
    ChatLog.insert(END, 'Cyber Security. Type "topics" to learn What I know About.' + '\n', 'welcome')
    
def return_topics(): #returns the topics from topics.txt
    ChatLog.tag_config('topics', foreground="dim gray", font=("Arial",12,'bold'))
   
    topic_file = open("topics.txt")
    lines = topic_file.readlines()
    ChatLog.insert(END, '--------------------------------------------' + '\n', 'welcome')
    ChatLog.insert(END, 'The topics that I can tell you about:' + '\n\n', 'welcome')
    for line in lines:
       ChatLog.insert(END, line, 'topics')
       print(line)
    ChatLog.insert(END, '\n\n') 
    ChatLog.insert(END, '--------------------------------------------' + '\n\n', 'welcome')
    ChatLog.insert(END, '\n\n') 
    topic_file.close()
    
     
#Creating GUI with tkinter
base = Tk()
base.title("CyberBot: Cyber Security ChatBOT")#Window title
base.geometry("600x800")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="light gray", height="8", width="50", font="Arial",)
welcome()
ChatLog.config(state=DISABLED)

#Add scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview)
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to search
SubmitButton = Button(base, font=("Verdana",10,'bold'), text="Submit", width="8", height=3,
                    bd=0, bg="spring green", activebackground="sea green",fg='black',
                    command= submit)
#Create Button to clear
ClearButton = Button(base, font=("Verdana",10,'bold'), text="Clear", width="8", height=3,
                    bd=0, bg="tomato", activebackground="orange red",fg='white',
                    command= clear )

ExitButton = Button(base, font=("Verdana",10,'bold'), text="Exit", width="8", height=3,
                    bd=0, bg="tomato", activebackground="orange red",fg='white',
                    command= quitprogram)

#Create the box to enter search term
EntryBox = Text(base, bd=0, bg="light steel blue",width="29", height="5", font="Arial")
#Place all components on the screen
scrollbar.place(x=578,y=6, height=686)
ChatLog.place(x=8,y=6, height=686, width=568)
EntryBox.place(x=96, y=701, height=90, width=435)
SubmitButton.place(x=8, y=701, height=40)
ClearButton.place(x=8, y=750, height=40)
ExitButton.place(x=540, y=701, height=90, width=50)
base.mainloop()   