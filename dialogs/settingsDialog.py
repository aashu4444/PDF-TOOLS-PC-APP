from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from filemanager import FileManager
import json
from kivymd.uix.menu import MDDropdownMenu
from utils import writeSettings

KV = '''
<settingsDialogCls>:
    orientation:"vertical"
    size_hint_y:None
    height:"50dp"
    MDScreen:
        MDBoxLayout:
            adaptive_height:True
            padding:"10dp"

            MDLabel:
                id:myDefaultSavePath
                text:"Default save folder : "
                
            MDRaisedButton:
                id:DropdownCaller
                text:"Browse"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                elevation_normal:12
                on_release:root.menu.open()

'''

Builder.load_string(KV)
class settingsDialogCls(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [
            {
                "text": f"Ask first",
                "viewclass": "OneLineListItem",
                "on_release":lambda : self.menu.dismiss(), # Close the dropdown
                "on_press": self.askFirst
            },
            {
                "text": f"Browse",
                "viewclass": "OneLineListItem",
                "on_release":lambda : self.menu.dismiss(), # Close the dropdown
                "on_press":self.askDefaultSaveFolder
            },
        ]

        self.menu = MDDropdownMenu(
            caller=self.ids.DropdownCaller,
            items=menu_items,
            width_mult=4,
        )

        self.ids.myDefaultSavePath.text = "Default save folder: " + json.loads(self.readSettings())["default_save_folder"]

    def writeSettings(self, data):
        with open("settings.json", "w") as f:
            f.write(data)

    def readSettings(self):
        with open("settings.json", "r") as f:
            return f.read()

    def askFirst(self):
        loaded = json.loads(self.readSettings())

        
        loaded["default_save_folder"] = "ask_first"

        # Change text of myDefaultSavePath label to ask_first
        self.ids.myDefaultSavePath.text = "Default save folder: ask_first"

        writeSettings(loaded)


    def askDefaultSaveFolder(self):
        filemanager = FileManager()
        filemanager.askDir(title="Select a default path where all pdf file will be saved.")

        # If user selected a directory
        if filemanager.askedDir != "":
            loaded = json.loads(self.readSettings())

            loaded["default_save_folder"] = filemanager.askedDir

            # Change text of myDefaultSavePath label to the selected directory's path
            self.ids.myDefaultSavePath.text = "Default save folder: " + filemanager.askedDir
            
            # Write the selected directory's path to settings.json
            self.writeSettings(json.dumps(loaded))


def getDialog(app):
    dialog = MDDialog(
                    title="Settings",
                    type="custom",
                    content_cls=settingsDialogCls(),
                )

    return dialog