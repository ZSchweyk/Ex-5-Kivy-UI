import os
import random
from threading import Thread
from pidev.Joystick import Joystick
import pygame

os.environ['DISPLAY'] = ":0.0"
# os.environ['KIVY_WINDOW'] = 'sdl2'
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel

from datetime import datetime
import time

t = time

time = datetime
rand = random

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
# os.environ["DISPLAY"] = ":0"
# pygame.display.init()
joy = Joystick(0, False)


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (random.random(), random.random(), random.random(), random.random())  # White


class MainScreen(Screen):
    """
        Class to handle the main screen and its associated touch events
        """

    def start_joy_thread(self):
        self.t = Thread(target=self.joy_update)
        self.t.do_run = True
        self.t.start()

        def close():
            self.t.do_run = False

        Window.on_request_close = close

    def end_joy_thread(self):
        self.t.do_run = False

    def joy_update(self):
        joystick_values = ObjectProperty(None)
        while self.t.do_run:
            self.x = round(joy.get_axis('x'), 2)
            self.y = round(-1 * joy.get_axis('y'), 2)
            disp_coord = (round(self.x * 100), round(self.y * 100))
            self.joystick_values.text = "x: " + str(disp_coord[0]) + "\ny: " + str(disp_coord[1])
            t.sleep(.025)

    def create_animation(self, instance):
        num_sec = 3
        rand_int = random.randint(20, 200)
        anim1 = Animation(size=(rand_int, rand_int), duration=num_sec)
        anim1.start(instance)
        self.change_screen_to_myNewScreen()

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    def toggle(self):
        toggle_btn = ObjectProperty(None)
        if self.toggle_btn.text == "Off":
            self.toggle_btn.text = "On"
        else:
            self.toggle_btn.text = "Off"

    def toggle_label_text(self):
        toggle_label_btn = ObjectProperty(None)
        toggling_label = ObjectProperty(None)
        if self.toggling_label.text == "Motor Off":
            self.toggling_label.text = "Motor On"
        else:
            self.toggling_label.text = "Motor Off"

    def counter(self):
        counter_btn = ObjectProperty(None)
        previous = int(self.counter_btn.text)
        self.counter_btn.text = str(previous + 1)
        pass

    @staticmethod
    def change_screen_to_myNewScreen():
        SCREEN_MANAGER.current = 'myNewScreen'

    @staticmethod
    def admin_action():
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


class MyNewScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_file('myNewScreen.kv')
        super(MyNewScreen, self).__init__(**kwargs)

    def create_animation(self, instance):
        num_sec = 3
        rand_int = random.randint(20, 200)
        anim1 = Animation(size=(rand_int, rand_int), duration=num_sec)
        anim1.start(instance)
        self.change_screen_to_mainScreen()

    @staticmethod
    def change_screen_to_mainScreen():
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(MyNewScreen(name='myNewScreen'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
