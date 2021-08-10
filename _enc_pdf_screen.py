from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast


KV = '''
MDBoxLayout:
    orientation: "vertical"
    spacing: "10dp"

    GridLayout:
        cols:1
        MDToolbar:
            elevation: 10
            title: "ENCRYPT PDF."

        
'''