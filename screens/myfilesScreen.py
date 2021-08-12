
from kivymd.uix import dialog, label
from kivymd.uix.behaviors import elevation
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from RoundedCornersCard import RoundedCornersCard
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.list import MDList
from kivymd.color_definitions import theme_colors
import json
from kivy.properties import StringProperty
from RoundedCornersCard import RoundedCornersCard
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.card import MDSeparator
from kivymd.uix.boxlayout import MDBoxLayout
from dialogs.deleteMyFileDialog import deleteMyFileDialog

class MyfilesScreen(ScrollView):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.mdls = MDList(spacing=40)
        self.add_widget(self.mdls)
        self.pos_hint = {"top":1}

        with open("myfiles.json", "r") as f:
            self.files = json.loads(f.read())


        def setScrollView():
            self.size_hint = (1, None)
            self.size=(Window.width, Window.height - 60)  
        
        setScrollView() 


        self.dialog = deleteMyFileDialog(app)

        self.updateFiles()

    def openDeleteFileDialog(self, widget):
        self.app.fileId = self.deleteFileButtons[widget]
        self.app.myfilesScreen = self
        self.dialog.open()

    def updateFiles(self,f=None, read=False):

        self.deleteFileButtons = {}

        for file in self.files:
            filename = file.get("name").split("/")[-1]
            print(file.get("name").split("/"))
            src = file.get("src")
            timestamp = file.get("timestamp")
            id = file.get('id')
            print(id)

            box_1 = MDBoxLayout(size_hint_y=None, height=80)
            icon = MDIcon(icon="language-python", size_hint_x=0.2, halign="center")
            filesDetailLayout = GridLayout(rows=2)
            filenameLabel = MDLabel(text=f"{filename}\n{src}")
            # filesrcLabel = MDLabel(theme_text_color="Secondary", text=src)
            filesDetailLayout.add_widget(filenameLabel)
            # filesDetailLayout.add_widget(filesrcLabel)
            box_1.add_widget(icon)
            box_1.add_widget(filesDetailLayout)

            box_2 = MDBoxLayout(size_hint_y=None, height=40)
            deleteButton = MDFlatButton(on_release=lambda x: self.openDeleteFileDialog(x))
            deleteButton.add_widget(MDIcon(icon="trash-can-outline", halign="center"))
            timeStampLabel = MDLabel(text=timestamp, halign="right")
            box_2.add_widget(deleteButton)
            box_2.add_widget(timeStampLabel)

            card = MDCard(orientation="vertical",size_hint=(.5, None), height=(box_1.height + box_2.height), padding="8dp", elevation=5)

            card.add_widget(box_1)
            card.add_widget(MDSeparator())
            card.add_widget(box_2)

            self.mdls.add_widget(card)

            self.deleteFileButtons[deleteButton] = id



