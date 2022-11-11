import kivy
import pandas as pd
import datetime as dt
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

currentdate = dt.datetime.today().strftime("%m/%d/%Y")
sessions = pd.read_csv('H:\coding\projects\interferenceinputapp\Sessions.csv')


class RowEntry:
    def __init__(self):
        self.logdate = currentdate
        self.session = ''
        self.interferer = ''
        self.intensity = 0
        self.contact = 0
        self.mitigation = 0
        # self.log = pd.DataFrame([[self.logdate, self.session, self.interferer, self.intensity, self.mitigation, self.contact]], columns = ('Date', 'Session', 'Interferer', 'Intensity', 'Mitigation', 'Contact'))
 

    def save_entry(self):
        self.log = pd.DataFrame([[self.logdate, self.session, self.interferer, self.intensity, self.mitigation, self.contact]], columns = ('Date', 'Session', 'Interferer', 'Intensity', 'Mitigation', 'Contact'))



class InterferenceApp(App):
    def __init__(self, **kwargs):
        super(InterferenceApp, self).__init__(**kwargs)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(DateScreen(name='datescreen'))
        sm.add_widget(SessionScreen(name='sessionscreen'))
        sm.add_widget(InterfererScreen(name='interfererscreen'))

        return sm



class DateScreen(Screen):
    def __init__(self, **kwargs):
        super(DateScreen, self).__init__(**kwargs)
        datepage = BoxLayout(orientation = 'vertical')
        dategrid = GridLayout(cols=3, padding=30)

        welcomelabel = Label(text="Welcome to the Interference Tracking App")
        datelabel = Label(text="Confirm Date:")
        self.dateinput = TextInput(multiline=False, text=currentdate, font_size=30)
        datebutton = Button(text="Continue", font_size=40, on_press = self.next)

        datepage.add_widget(welcomelabel)
        dategrid.add_widget(datelabel)
        dategrid.add_widget(self.dateinput)
        dategrid.add_widget(datebutton)
        datepage.add_widget(dategrid)

        self.add_widget(datepage)


    def next(self, *args):
        self.activerow = RowEntry()
        self.activerow.logdate = self.dateinput.text
        self.manager.current = 'sessionscreen'




class SessionScreen(Screen, RowEntry):
    app= App.get_running_app()
    def __init__(self, **kwargs):
        super(SessionScreen, self).__init__(**kwargs)

    def on_enter(self, *args):

        #layouts: Box for overall, Stack for sessions
        sessionpage = BoxLayout(orientation='vertical')
        sessionchoice = StackLayout()

        #box layout, first label on top, then session choices, then back button on bottom
        date_screen = self.manager.get_screen('datescreen')
        datelabel = Label(text = f'You are logging for: {date_screen.activerow.logdate}', size_hint=(1, .15))
        backbutton = Button(text="back", on_press = self.backtodate, size_hint=(1, .15))

        for i in sessions['Sessions']:
            btn = Button(text=str(i), size_hint=(.2, .15), on_press=self.ssnbtn)
            sessionchoice.add_widget(btn)
            btn.sess = str(i)


        sessionpage.add_widget(datelabel)
        sessionpage.add_widget(sessionchoice)
        sessionpage.add_widget(backbutton)

        self.add_widget(sessionpage)

    def backtodate(self, instance):
        self.manager.current='datescreen'


    def ssnbtn(self, instance):
        #change screen to next, set current row session
        date_screen = self.manager.get_screen('datescreen')
        date_screen.activerow.session = instance.sess
        self.manager.current='interfererscreen'
        print(f'instance.sess = {instance.sess}')
        print(f'date_screen.activerow.session = {date_screen.activerow.session}')
        date_screen.activerow.log = pd.DataFrame([[date_screen.activerow.logdate, date_screen.activerow.session, date_screen.activerow.interferer, date_screen.activerow.intensity, date_screen.activerow.mitigation, date_screen.activerow.contact]], columns = ('Date', 'Session', 'Interferer', 'Intensity', 'Mitigation', 'Contact'))
        print(f'saved log: \n{date_screen.activerow.log}')


class InterfererScreen(Screen, RowEntry):
    def __init__(self, **kwargs):
        super(InterfererScreen, self).__init__(**kwargs)
    
    def on_enter(self, *args):
        backbutton = Button(text="back", on_press = self.backtosess, size_hint=(1, .15))
        self.add_widget(backbutton)

    def backtosess(self, instance):
        self.manager.current='sessionscreen'

if __name__ == "__main__":
    InterferenceApp().run()