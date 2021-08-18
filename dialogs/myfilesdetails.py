from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from filemanager import FileManager
import json
from kivymd.uix.menu import MDDropdownMenu

KV = '''
<OpereatedFileDetails>:
    orientation:"vertical"
    size_hint_y:None
    height:"200dp"
    MDScreen:
        MDBoxLayout:
            adaptive_height:True
            padding:"10dp"

            GridLayout:
                cols:2
                rows:4

                MDLabel:
                    text:"File name : "
                MDLabel:
                    id:FileName
                    text:"None"

                MDLabel:
                    text:"File source : "
                MDLabel:
                    id:FileSrc
                    text:"None"
                    
                MDLabel:
                    text:"Operation name : "
                MDLabel:
                    id:OperationName
                    text:"None"

                MDLabel:
                    text:"Operation date : "
                MDLabel:
                    id:OperationDate
                    text:"None"

'''

Builder.load_string(KV)
class OpereatedFileDetails(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



def getOperationFileDetailsDialog(app, file):
    dialog = MDDialog(
                    title="Settings",
                    type="custom",
                    content_cls=OpereatedFileDetails(),
                )

    return dialog