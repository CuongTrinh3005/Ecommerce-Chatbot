from tkinter import *
from tensorflow.keras.models import load_model
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import pickle
import random
import json
from nltk import word_tokenize
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
speaker = pyttsx3.init()
from Communication import text_to_speech, speech_to_text
from Cart import cart

windows = Tk()
windows.wm_title("ChatBot GUI")
# windows.configure(background='red')
windows.geometry("500x350")

sb = Scrollbar(windows)
sb.pack(side=RIGHT, fill=Y)
#canvas = Canvas(windows, bg='pink', width=500, yscrollcommand=sb.set)
#canvas.pack()
messages = Text(windows, bg='cyan', width='500', height='18', yscrollcommand=sb.set)
messages.pack()
messages.tag_config('warning', background="cyan", foreground="green")

label = Label(windows, text="Enter message:").place(x=0, y=320)
txt = Text(windows)
txt.place(x=100, y=300, width=300)

# b_voice = Button(windows, text="VOICE", width=50, fg="green", activeforeground="red",activebackground="pink")

model = load_model("chatbot.h5")
list_of_products = []

with open('intents.json') as file:
    data_chatbot = json.load(file)

with open('information.pickle', 'rb') as file:
    vocab, classes, training = pickle.load(file)

def create_bag_of_words(sentence):
    bag = [0 for _ in range(len(vocab))]
    word_of_sentence = word_tokenize(sentence)
    stemmed_word = [stemmer.stem(w.lower()) for w in word_of_sentence]
    for i, w in enumerate(vocab):
        if w in stemmed_word:
            bag[i] = 1

    return np.array([bag])

def count_frequence_input(user_input, vocab_list):
    list_of_word = word_tokenize(user_input.lower())
    score = 0
    for w in list_of_word:
        if stemmer.stem(w) in vocab_list:
            score += 1

    freq = score / len(vocab_list) * 100
    return freq

def getResponse(request):
    result = model.predict(create_bag_of_words(request))
    tag = classes[np.argmax(result)]

    for content in data_chatbot['intents']:
        if content['tag'] == tag:
            responses = content['responses']
    response = 'Bot: '
    response += random.choice(responses)

    if tag == 'datetime' and count_frequence_input(request, vocab) > 0.0:
        import datetime

        x = datetime.datetime.now()
        response = "Bot: It is on " + x.strftime("%A") + ', ' + x.strftime('%m/%d/%Y, %H:%M:%S')
        # print('Bot: It is on', x.strftime("%A"), x)

    if tag == "order":
        request = request.lower()
        list_of_order = request.split()
        product = list_of_order[list_of_order.index("order") + 1]
        print("Product is ", product)
        list_of_products.append(product)
        print(list_of_products)
    return response

def enter_pressed(event):
    user_input = "User: " + txt.get('1.0', END)
    if user_input != '':
        messages.insert(INSERT, '%s' % user_input)
        txt.delete(1.0, END)
        bot_response = getResponse(user_input)
        messages.insert(INSERT, '%s\n\n' % bot_response, 'warning')
        # messages.mark_set(INSERT, '1.0') # insert text at the first position of dialog
        messages.see("end") # insert text and focus at the end of dialog

    return "break"

def use_voice():
    text0 = "please say something"
    text_to_speech(speaker, text0)
    while True:
        try:
            text = speech_to_text(r)
            if text.lower() == "stop":
                break
            else:
                result = model.predict(create_bag_of_words(text))
                tag = classes[np.argmax(result)]

                for content in data_chatbot['intents']:
                    if content['tag'] == tag:
                        responses = content['responses']

                response = random.choice(responses)

                if tag == 'datetime' and count_frequence_input(text, vocab) > 0.0:
                    import datetime

                    x = datetime.datetime.now()
                    response = "It is on " + x.strftime("%A") + ', ' + x.strftime('%m/%d/%Y, %H:%M:%S')
                    # print('Bot: It is on', x.strftime("%A"), x)

                if tag == "order":
                    text = text.lower()
                    list_of_order = text.split()
                    product = list_of_order[list_of_order.index("order") + 1]
                    print("Product is ", product)
                    list_of_products.append(product)
                    print(list_of_products)

                text_to_speech(speaker, response)
                messages.insert(INSERT, '%s\n' % ('User: ' + text))
                messages.insert(INSERT, '%s\n\n' % ("Bot: " + response), 'warning')
                messages.see("end")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition; {0}".format(e))
        except sr.UnknownValueError as uv:
            print("Google Speech Recognition could not understand audio")

b_voice = Button(windows,text="VOICE", fg="green", activeforeground="yellow",activebackground="red", command=use_voice)
b_voice.place(x=410, y=290)

b_cart = Button(windows, text="CART ", fg="green", activeforeground="yellow",activebackground="red", command=lambda: cart(list_of_products))
b_cart.place(x=410, y=320)
txt.bind("<Return>", enter_pressed)
mainloop()