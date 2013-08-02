"""
problem_solver.py
"""
import kivy
from random import choice
import cPickle
kivy.require('1.0.7')
from functools import partial
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.screenmanager import ScreenManager, Screen

class SaveData:
        pass

class Database:
    def __init__(self):
        try: 
            self.sd = cPickle.load(open('savedata.p', 'rb')) # Pickle with dict of current directory mapped with save directories.
        except (IOError, cPickle.UnpicklingError):
            self.sd = SaveData()
            self.sd.dbdict = {}
            self.sd.theme = 'Setup'
            self.sd.dbdict[self.sd.theme] = []
            self.Save()

    def Save(self):
        cPickle.dump(self.sd, open('savedata.p', 'wb'))

    def Append(self, string):
        self.sd.dbdict[self.sd.theme].append(string)
        self.Save()

# Create database instance.
db = Database()


##################### Start of GUI:
Builder.load_string("""

#:import label kivy.uix.label
#:import la kivy.adapters.listadapter
#:import listview kivy.uix.listview
#:import ListItemButton kivy.uix.listview.ListItemButton

<InitializeScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Welcome! Please enter the name of your first theme.'
        TextInput:
            id: txti
            multiline: False
            on_text_validate: root.SetInitialMode(self.text); root.manager.current = 'main'
            focus: True


<MainScreen>:
    label: main_label

    BoxLayout:
        orientation: 'vertical'
        padding: [4,4,4,4]

        Label:
            text: 'Welcome'
            id: main_label
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Next Term'
                on_press: root.NewTerm()
            Button:
                text: 'Settings'
                on_press: root.manager.current = 'settings'
            Button:
                text: 'Quit'
                on_press: root.Exit()

<SettingsScreen>:
    settings_screen: self
    list_view: list_view_id
    on_pre_enter: root.initiate_label()
    add_button: add_button_id

    BoxLayout:
        orientation: 'vertical'
        padding: [2,2,2,2]

        Label:
            text: root.theme
        TextInput:
            id: txti
            multiline: False
            on_text_validate: root.AddTerm(self.text); self.text= ''; self.focus= True
            focus: True
        ListView:
            id: list_view_id
            adapter:
                la.ListAdapter(
                data=root.list_contents, 
                selection_mode = 'single',
                allow_empty_selection = False,
                cls = ListItemButton)
        BoxLayout:
            orientation: 'horizontal'
            Button: 
                id: add_button_id
                text: 'Add Term'
                on_press: root.AddTerm(txti.text); self.focus= True
            Button: 
                text: 'Change Theme'
                on_press: root.change_theme()
            Button:
                text: 'Delete Item'
                on_press: root.DeleteTerm()
            Button:
                text: 'Back to Main'
                on_press: root.manager.current = 'main'
""")

## Declaration of screens.

# Initialize screen will only show up the first time.

class InitializeScreen(Screen):
    def SetInitialMode(self, text):
        db.sd.dbdict[text] = []
        db.sd.theme = text


class MainScreen(Screen):
    # Set the initial display term. 
    label = ObjectProperty(None)

    def InitiateTerm(self):
        self.label.text = "Welcome"

    def NewTerm(self):
        self.label.text = choice(db.sd.dbdict[db.sd.theme])

    def Exit(self):
        import sys; sys.exit()

class SettingsScreen(Screen):
    list_contents = ListProperty(db.sd.dbdict[db.sd.theme])
    add_button = ObjectProperty(None)
    theme = StringProperty(db.sd.theme)

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        #self.list_view.adapter.bind(on_selection_change=self.selection_changed)
        self.cm = False # This will manage the change_theme function later.

    def initiate_label(self):
        self.theme = db.sd.theme

    # def selection_changed(self, *args):
    #     self.selected_item = args[0].selection[0].text

    def AddTerm(self, strat):
        if self.cm == True:
            db.sd.dbdict[strat] = []
            self.list_contents = db.sd.dbdict.keys()
        elif self.cm == False:
            db.Append(strat)
            self.list_contents = db.sd.dbdict[db.sd.theme]
        db.Save()
        #self.list_view.adapter.bind(on_selection_change=self.selection_changed)

    def DeleteTerm(self):
        if self.cm == True:
            bl = BoxLayout()
            btn1 = Button(text='yes')
            db.current_selection = self.list_view.adapter.selection[0].text

            def btn1press(self):
                del db.sd.dbdict[db.current_selection]
                popup.dismiss()

            btn1.bind(on_press=btn1press)
            btn2 = Button(text='no')

            def btn2press(self):
                popup.dismiss()

            btn2.bind(on_press=btn2press)
            bl.add_widget(btn1)
            bl.add_widget(btn2)

            def pdismiss(self):
                ss.list_contents = db.sd.dbdict.keys()
                db.Save()

            popup = Popup(title='Warning: Do you sure you want to delete %s?' % self.list_view.adapter.selection[0].text,
                content=bl,
                auto_dismiss=False,
                size_hint=(0.6, 0.6),
                on_dismiss = pdismiss               
                )
            popup.open()
        elif self.cm == False:
            try:
                db.sd.dbdict[db.sd.theme] = [item for item in db.sd.dbdict[db.sd.theme] if item != self.list_view.adapter.selection[0].text]
            except:
                pass
            self.list_contents = db.sd.dbdict[db.sd.theme]
        
        #self.list_view.adapter.bind(on_selection_change=self.selection_changed)

    def change_theme(self):
        if self.cm == True:
            self.cm = False
            db.sd.theme = self.list_view.adapter.selection[0].text
            self.theme = db.sd.theme
            self.list_contents = db.sd.dbdict[db.sd.theme]
            self.add_button.text = 'Add Term'
        elif self.cm == False:
            self.cm = True
            self.list_contents = db.sd.dbdict.keys()
            self.add_button.text = 'Add Theme'
       # self.list_view.adapter.bind(on_selection_change=self.selection_changed)
        db.Save()

class MyPopup(Popup):
    def __init__(self, **kwargs):
        super(MyPopup, self).__init__(**kwargs)


#####

# Create the manager
sm = ScreenManager()
# Set up functionality to set up the key of the dictionary when the program first launches.
if db.sd.theme == 'Setup':
    sm.add_widget(InitializeScreen(name='initialize'))
ms = MainScreen(name='main')
ss = SettingsScreen(name='settings')
sm.add_widget(ms)
sm.add_widget(ss)
#####

# The main app:
class ProbSolApp(App):
    def build(self):
        return sm
#####

# Running the app:
if __name__ == '__main__':
    ProbSolApp().run()
#####

