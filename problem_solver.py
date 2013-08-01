"""
problem_solver.py
"""
import kivy
kivy.require('1.0.7')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen


## Declare both screens.

class MenuScreen(Screen):
	label = "This is a test"
	pass

class AddTermsScreen(Screen):
	pass

# Create the manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(AddTermsScreen(name='add_terms'))

class probsolApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    probsolApp().run()

