
from kivymd.uix import label
from kivymd.uix.screen import MDScreen
from RoundedCornersCard import RoundedCornersCard
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.list import ThreeLineIconListItem, TwoLineIconListItem
from kivymd.uix.list import IconLeftWidget
import json
from kivymd.uix.card import MDCardSwipe
from kivy.properties import StringProperty
from RoundedCornersCard import RoundedCornersCard
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel

KV = '''
<MyfilesScreen>:
    MDScreen:
        GridLayout:
            cols:1
            MDToolbar:
                title:"My operated pdf files."


            MDCard:
                orientation: "vertical"
                size_hint: .5, None
                height: 120
                pos_hint: {"center_x": .5, "center_y": .5}
                padding:"8dp"

                
                MDBoxLayout:
                    orientation:"vertical"
                    MDBoxLayout:
                        size_hint_y:None
                        height:70
                        MDIcon:
                            icon:"language-python"
                            size_hint_x: 0.2
                            halign:"center"
                        MDBoxLayout:
                            orientation:"vertical"
                            MDLabel:
                                markup:True
                                text:"[b]pdf-tools-test.pdf[/b][color=969191]F:/AllTets/pdf-tools-ss.pdf[/color]"

                    MDSeparator:
                    
                    MDLabel:
                        text:"18 June 2021 at 15:30 PM"
                        halign:"right"

                    
                        

                

'''

Builder.load_string(KV)


class MyfilesScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        with open("myfiles.json", "r") as f:
            files = json.loads(f.read())

        # def setScrollView():
        #     self.ids.filesScrollView.size_hint = (1, None)
        #     self.ids.filesScrollView.size=(Window.width, Window.height - 60)  
        
        # setScrollView()  

        # for file in files:
        #     filename = file.get("name").split("/")[-1]
        #     print(file.get("name").split("/"))
        #     src = file.get("src")
        #     timestamp = file.get("timestamp")

        #     mainLayout = BoxLayout(orientation="vertical")
        #     cardLayout = GridLayout(cols=2)
        #     labelsLayout = GridLayout(rows=2)

        #     heading = MDLabel(text=filename)
        #     path = MDLabel(text=src)

        #     labelsLayout.add_widget(heading)
        #     labelsLayout.add_widget(path)


        #     icon = MDIcon(icon="file-pdf-box", size_hint_x=0.3, halign="center")


        #     card = RoundedCornersCard()

        #     cardLayout.add_widget(icon)
        #     cardLayout.add_widget(labelsLayout)

        #     card.add_widget(cardLayout)


        #     timeStampCard = RoundedCornersCard(size_hint_y=None, height=20)
        #     timeStampText = MDLabel(text="Saved on 31 December 2020 at 12:59 PM")

        #     timeStampCard.add_widget(timeStampText)

        #     mainLayout.add_widget(card)
        #     mainLayout.add_widget(timeStampCard)

        #     self.ids.filesList.add_widget(mainLayout)



