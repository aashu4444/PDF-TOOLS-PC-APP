
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

KV = '''
<HomeScreen>:

    GridLayout:
        cols:1
        MDToolbar:
            title:"PDF TOOLS."

        BoxLayout:
            pos_hint:{"top":0.8}
            ScrollView:
                id:homeScrollView
                MDList:
                    id:homeLayout
                

'''

Builder.load_string(KV)

class HomeScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(**kw)

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
                "on_release":lambda x: print(x)
            },
            {
                "icon":"file-pdf-box",
                "text":"My Files",
                "desc":"View your operated pdf files.",
                "on_release":lambda x: print(x)
            },
        ]
        
        def setScrollView():

            self.ids.homeScrollView.size_hint = (1, None)
            self.ids.homeScrollView.size=(Window.width, Window.height - 60) 
        
        setScrollView() 

        Window.bind(on_resize=lambda a,b,c:setScrollView())        


        for item in items:
            # List item widget
            widget = TwoLineIconListItem(text=item.get("text"), secondary_text=item.get("desc"),   on_release=item.get("on_release"))
            
            # Icon of the list item
            icon = IconLeftWidget(icon=item.get("icon"))

            # Add icon to the list item widget
            widget.add_widget(icon)

            self.ids.homeLayout.add_widget(
                widget
            )



