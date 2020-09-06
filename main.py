import multiprocessing
import random
import sys
from multiprocessing import Process
from time import sleep
from kivy.properties import ObjectProperty
import pyttsx3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.logger import LoggerHistory


class P(FloatLayout):
    def __init__(self, text):
        super().__init__()
        self.add_widget(Label(text=text, size_hint=(0.6, 0.2), 
        pos_hint={"x":0.2, "top":1}))

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.n_names = len(names)
        self.names = names 
        self.bot_speak = pyttsx3.init()
        self.bot_speak.setProperty('rate', 125) 
        self.answer = ''
        self.count = 0

        self.inside = GridLayout()
        self.inside.cols = 2
        self.cols = 1

        self.inside.add_widget(Label(text="Your Answer: "))
        self.user_answer = TextInput(multiline=False)
        self.inside.add_widget(self.user_answer)

        self.add_widget(self.inside)

        self.listen = Button(text="Listen", font_size=20)
        self.listen.bind(on_press=self.listen_pressed)
        self.add_widget(self.listen)

        self.submit = Button(text="Submit", font_size=20)
        self.submit.bind(on_press=self.submit_pressed)
        self.add_widget(self.submit)
        
    def submit_pressed(self, instance):
        # self.count = 3 # spell new name
        user_answer = self.user_answer.text 
        if user_answer != '' and self.answer == user_answer.upper():
            self.show_popup(True)
        else:
            self.show_popup(False)
        # print("Your answer: ", user_answer)
        # print("Answer: ", self.answer)

    def speak_name(self):
        self.bot_speak.say(self.answer)
        self.bot_speak.runAndWait()
        for spell in self.answer:
            self.bot_speak.say(spell)
            self.bot_speak.runAndWait()
    
    def speak_phone(self):
        for spell in self.answer:
            self.bot_speak.say(spell)
            self.bot_speak.runAndWait()

    def speak_year(self):
        self.bot_speak.say(self.answer)
        self.bot_speak.runAndWait()

        self.answer = str(self.answer)
        self.bot_speak.say(self.answer[0:2])
        self.bot_speak.runAndWait()

        self.bot_speak.say(self.answer[-2:])
        self.bot_speak.runAndWait()


    def speak(self):
        if self.count == 0:
            
            self.idx = random.randint(0, self.n_names - 1)
            self.answer1 = self.names[self.idx]

            self.tmp_arr = []
            self.tmp_arr.append(str(random.randint(1, 9)))
            for _ in range(9):
                self.tmp_arr.append(str(random.randint(0, 9)))
            self.answer2 = ''.join(self.tmp_arr)

            self.answer3 = random.randint(1000, 7000)

        if self.count != 3:
            if self.choose == 1:
                self.answer = self.answer1
                self.speak_name()
            elif self.choose == 2:
                self.answer = self.answer2
                self.speak_phone()
            else:
                self.answer = self.answer3
                self.speak_year()
            
        else:
            self.count = 0
            self.bot_speak.say('Listen')
            self.bot_speak.runAndWait()
        self.count += 1

    def listen_pressed(self, instance):
        if self.count == 0:
            self.choose = random.randint(1, 3)
        self.speak()          


    def show_popup(self, boolean):
        if boolean:
            self.count = 0
            text = "Your answer is correct."
        else:
            if self.count == 3:
                text = f"You are wrong. It must be '{self.answer}'. Try again."
            else:
                text = "One more time ^_^ ."
        show = P(text) # Create a new instance of the P class 
        popupWindow = Popup(title="Result Window", content=show, size_hint=(None,None),size=(400,400)) 
        # Create the popup window
        show.add_widget(Button(text='OK', size_hint=(0.8, 0.2), pos_hint={"x":0.1, "y":0.1}, on_release=popupWindow.dismiss))
        popupWindow.open() # show the popup

class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    with open('all_names.txt', 'r') as f:
        doc = f.read()
    global answer 
    names = doc.split('\n')
    n_names = len(names)
    MyApp().run()
    
    sys.stderr = open('output.txt', 'w')
    sys.stdout = sys.stderr

    print('\n'.join([str(l) for l in LoggerHistory.history]))