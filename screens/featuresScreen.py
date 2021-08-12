from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.list import IconLeftWidget
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.toolbar import MDToolbar
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.lang import Builder

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList

kv = '''
MDFloatingActionButtonSpeedDial:
    data: app.data
    root_button_anim: True
    hint_animation: True
    label_text_color: 1,1,1,1
    callback:app.callback
'''


class FeaturesScreen(ScrollView):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.pos_hint = {"top":1}
        mdls = MDList()
        self.add_widget(mdls)


        features = [
            {
                "title":"Encrypt PDF",
                "desc":"Set password on your pdf file",
                "icon":"lock",
                "on_release":lambda x: app.encpdfDialog.open(),
            },
            {
                "title":"Decrypt PDF",
                "desc":"Remove password on your pdf file",
                "icon":"lock-off",
                "on_release":lambda x: app.decryptpdfDialog.open(),
            },
            {
                "title":"Remove links",
                "desc":"Remove links on your pdf file.",
                "icon":"link",
                "on_release":lambda x: app.operate(mystr='self.mytool.remove_links(self.selectedDest)', operationName=x.text),
            },
            {
                "title":"Remove images",
                "desc":"Remove images on your pdf file.",
                "icon":"image-off",
                "on_release":lambda x: app.operate(mystr='self.mytool.remove_images(self.selectedDest)', operationName=x.text),
            },
            {
                "title":"Extract images",
                "desc":"Extract images from your pdf file.",
                "icon":"image-multiple",
                "on_release":lambda x: app.operate(mystr='self.mytool.extract_images(self.selectedDest)', operationName=x.text, askDir=True),
            },
            {
                "title":"Save operation pages",
                "desc":"Save operation pages that you have set.",
                "icon":"format-page-break",
                "on_release":lambda x: app.operate(mystr='self.mytool.save_operation_pages(self.selectedDest)', operationName=x.text),
            },
        ]


        
        def setScrollView():
            self.size_hint = (1, None)
            self.size=(Window.width, Window.height - 60)  
        
        setScrollView()  

        Window.bind(on_resize=lambda a,b,c:setScrollView())        


        for feature in features:
            title = feature.get("title")
            desc = feature.get("desc")
            icon = feature.get("icon")
            on_release = feature.get("on_release")

            # List item widget
            widget = TwoLineIconListItem(text=title, secondary_text=desc,   on_release=on_release)
            
            # Icon of the list item
            icon = IconLeftWidget(icon=icon)

            # Add icon to the list item widget
            widget.add_widget(icon)

            mdls.add_widget(
                widget
            )

        Builder.load_string(kv)
