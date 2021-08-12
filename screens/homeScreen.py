
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



class HomeScreen(ScrollView):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        mdls = MDList()
        self.pos_hint = {"top":1}
        
        self.add_widget(mdls)

        settingsDialog = getDialog(app)

        items = [
            {
                "icon":"cloud-upload",
                "text":"Upload a file",
                "desc":"Upload a file to use pdf tools",
                "on_release":app.askFile
            },
            {
                "icon":"cog",
                "text":"Settings",
                "desc":"Change basic settings.",
                "on_release":lambda x: settingsDialog.open()
            },
        ]
        
        def setScrollView():
            self.size_hint = (1, None)
            self.size=(Window.width, Window.height - 60) 
        
        setScrollView() 

        Window.bind(on_resize=lambda a,b,c:setScrollView())        


        for item in items:
            # List item widget
            widget = TwoLineIconListItem(text=item.get("text"), secondary_text=item.get("desc"),   on_release=item.get("on_release"))
            
            # Icon of the list item
            icon = IconLeftWidget(icon=item.get("icon"))

            # Add icon to the list item widget
            widget.add_widget(icon)

            mdls.add_widget(
                widget
            )



