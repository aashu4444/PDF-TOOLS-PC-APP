from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import json
import os


KV = '''
<contentCls>:
    orientation:"vertical"
    size_hint_y:None
    height:"50dp"
    MDScreen:
        MDBoxLayout:
            adaptive_height:True
            padding:"10dp"

            MDLabel:
                id:myLabel
                text:"Delete source file too!"
                
            MDCheckbox:
                id:checkBox
                size_hint:None, None
                size:"48dp", "48dp"


'''

Builder.load_string(KV)

class contentCls(BoxLayout):
    pass


def deleteFile(dialog, app):
    with open("myfiles.json", "r") as f:
        loaded = json.loads(f.read())

        for i in loaded:
            if i["id"] == app.fileId:
                loaded.remove(i)

                if str(dialog.content_cls.ids.checkBox.state) == "down":
                    os.remove(i["src"])

        dataToWrite = json.dumps(loaded)

    with open("myfiles.json", "w") as file:
        file.write(dataToWrite)

    

    with open("myfiles.json", "r") as file:
        app.myfilesScreen.files = json.loads(file.read())
        app.myfilesScreen.ids.filesList.clear_widgets()
        app.myfilesScreen.updateFiles(file, read=True)
        dialog.dismiss()


def deleteMyFileDialog(app):
    dialog = MDDialog(
                    title="Are you sure?",
                    type="custom",
                    content_cls=contentCls(),
                    buttons=[
                        MDFlatButton(
                            text="DELETE", 
                            text_color=app.theme_cls.primary_color,
                            on_release=lambda x: deleteFile(dialog,app),
                            )
                    ],
                )
    return dialog
    