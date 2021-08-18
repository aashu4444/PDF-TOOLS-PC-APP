
from tkinter import Grid
from kivymd.uix.screen import MDScreen
from RoundedCornersCard import RoundedCornersCard
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.list import IconLeftWidget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList
from dialogs.settingsDialog import getDialog
from dialogs.mergePdfDialog import getMergePdfDialog
from RoundedCornersCard import RoundedCornersCard
from kivy.graphics import Color, Rectangle
from kivymd.uix.card import MDSeparator



class HomeScreen(ScrollView):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        mdls = MDList(spacing=30)
        self.pos_hint = {"top":1}
        
        self.add_widget(mdls)

        settingsDialog = getDialog(app)

        items = [
            {
                "icon":"cloud-upload",
                "text":"Upload a file",
                "desc":"Upload a file to use pdf tools",
                "footerText":"Currently : No file choosen",
                "on_release":app.askFile
            },
            {
                "icon":"cog",
                "text":"Settings",
                "desc":"Change basic settings.",
                "footerText":"e.x. - default save folder",
                "on_release":lambda x: settingsDialog.open()
            },         
        
        ]
        
        def setScrollView():
            self.size_hint = (1, None)
            self.size=(Window.width, Window.height - 60) 
        
        setScrollView() 

        Window.bind(on_resize=lambda a,b,c:setScrollView())        


        for index, item in enumerate(items):
            # Layout of card - 2 columns
            cardLayout = GridLayout(cols=2, size_hint=(1, None), height="70dp")

            # Icon in card
            icon = MDIcon(icon=item.get("icon"), size_hint_x=0.3, halign="center")
            cardLayout.add_widget(icon)

            # Layout that contains the title and desc
            textLayout = GridLayout(cols=1)

            # Title of the card
            heading = MDLabel(text=item.get("text"), font_style="Button", valign="center")

            # Desc of the card
            desc = MDLabel(text=item.get("desc"), font_style="Button", theme_text_color="Secondary")


            # Footer of the card that contains additional text
            cardFooter = GridLayout(cols=2, size_hint=(1, None), height="40dp")


            # Main card object
            card = RoundedCornersCard(size_hint=(0.8, None), height=cardLayout.height + cardFooter.height, padding="8dp", on_release=item.get("on_release"))

            # Add heading and desc in textLayout
            textLayout.add_widget(heading)
            textLayout.add_widget(desc)


            # Add textLayout in cardLayout
            cardLayout.add_widget(textLayout)


            # Add cardLayout in main card
            card.add_widget(cardLayout)

            
            # Footer text of the card
            footer_text = MDLabel(text=item.get("footerText"), font_style="Button")

            # If the footer is of first item (Upload file card) then add it to the class
            # It is used to target the text later and change the current uploaded file text
            if index == 0:
                self.currentlyUploadedText = footer_text

            # Add the footer text to the card footer
            cardFooter.add_widget(footer_text)

            # Add a seperator in the card
            card.add_widget(MDSeparator())

            # Add the footer to the card
            card.add_widget(cardFooter)

            # Add the card in main list of scroll view
            mdls.add_widget(card)


