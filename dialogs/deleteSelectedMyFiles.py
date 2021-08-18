from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import json
import os
from utils import *


KV = '''
<dialogContentClass>:
    orientation:"vertical"
    size_hint_y:None
    height:"100dp"
    MDScreen:
        GridLayout:
            cols:1
            MDLabel:
                text: "Are you sure that you wants to delete all selected items?"
                theme_text_color:"Secondary"
            MDBoxLayout:
                adaptive_height:True
                padding:"10dp"

                MDLabel:
                    id:myLabel
                    text:"Delete source file(s) too!"
                    
                MDCheckbox:
                    id:deleteSource
                    size_hint:None, None
                    size:"48dp", "48dp"


'''

Builder.load_string(KV)

class dialogContentClass(BoxLayout):
    pass


def deleteSelectedFiles(dialog, app):
    loaded = ReadMyFiles()
    deleteSource = dialog.content_cls.ids.deleteSource.active

    for item in app.myfilesscreen.selectedFiles:
        file = app.myfilesscreen.cardCheckboxes[item]


        loaded.remove(file)
        if deleteSource == True:
            try:
                srcImages = file.get("srcImages", "None")

                if srcImages != "None":
                    for image in srcImages:
                        os.remove(image)
                
                else:
                    os.remove(file.get("src"))

            except Exception as e:
                pass



    WriteMyFiles(loaded, append=False)


    app.myfilesscreen.updateFiles()
    dialog.dismiss()


def deleteSelectedMyFilesDialog(app):
    dialog = MDDialog(
                    title="Are you sure?",
                    type="custom",
                    content_cls=dialogContentClass(),
                    buttons=[
                        MDFlatButton(
                            text="CONFIRM", 
                            text_color=app.theme_cls.primary_color,
                            on_release=lambda x: deleteSelectedFiles(dialog,app),
                            )
                    ],
                )
    return dialog
    