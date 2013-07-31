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
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.screenmanager import ScreenManager, Screen


class Database:
    def __init__(self):
        try: 
            self.stratlist = cPickle.load(open('stratlist.p', 'rb')) # Pickle with dict of current directory mapped with save directories.
        except (IOError, cPickle.UnpicklingError):
            self.stratlist = []
            self.Save()

    def Save(self):
        cPickle.dump(self.stratlist, open('stratlist.p', 'wb'))

    def Append(self, string):
        self.stratlist.append(string)
        self.Save()

# Create database instance.
db = Database()


##################### Start of GUI:
Builder.load_string("""

#:import label kivy.uix.label
#:import la kivy.adapters.listadapter
#:import listview kivy.uix.listview
#:import ListItemButton kivy.uix.listview.ListItemButton

<MenuScreen>:
    label: main_label

    BoxLayout:
        orientation: 'vertical'
        padding: [4,4,4,4]

        UpdatingLabel:
            text: 'Welcome'
            id: main_label
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Next Term'
                on_press: root.NewTerm()
            Button:
                text: 'Add New Terms'
                on_press: root.manager.current = 'add_terms'
            Button:
                text: 'Quit'
                on_press: root.Exit()

<AddTermsScreen>:
    list_view: list_view_id

    BoxLayout:
        orientation: 'vertical'
        padding: [2,2,2,2]

        TextInput:
            id: txti
            multiline: False
            on_text_validate: root.AddTerm(self.text); self.text= ''; self.focus= True
            focus: True
        ListView:
            id: list_view_id
            adapter:
                la.ListAdapter(
                data=root.all_strategies, 
                selection_mode = 'single',
                allow_empty_selection = False,
                cls = ListItemButton)
        BoxLayout:
            orientation: 'horizontal'
            Button: 
                text: 'Add Term'
                on_press: root.AddTerm(txti.text)
            Button:
                text: 'Delete Item'
                on_press: root.DeleteTerm()
            Button:
                text: 'Back to Menu'
                on_press: root.manager.current = 'menu'
""")

class UpdatingLabel(Label):
    #import pdb; pdb.set_trace()
    pass

## Declaration of both screens.
class MenuScreen(Screen):
    # Set the initial display term. 
    label = ObjectProperty(None)

    def InitiateTerm(self):
        self.label.text = "Welcome"

    def NewTerm(self):
        self.label.text = choice(db.stratlist)

    def Exit(self):
        import sys; sys.exit()

class AddTermsScreen(Screen):
    all_strategies = ListProperty(db.stratlist)

    def __init__(self, **kwargs):
        super(AddTermsScreen, self).__init__(**kwargs)
        self.list_view.adapter.bind(on_selection_change=self.selection_changed)

    def selection_changed(self, *args):
        self.selected_item = args[0].selection[0].text

    def AddTerm(self, strat):
        db.Append(strat)
        self.all_strategies = db.stratlist
        self.list_view.adapter.bind(on_selection_change=self.selection_changed)

    def DeleteTerm(self):
        try:
            db.stratlist = [item for item in db.stratlist if item != self.selected_item]
        except:
            pass
        self.all_strategies = db.stratlist
        db.Save()
        self.list_view.adapter.bind(on_selection_change=self.selection_changed)



#####

# Create the manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(AddTermsScreen(name='add_terms'))
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

