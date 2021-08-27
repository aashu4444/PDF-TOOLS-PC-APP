from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from filemanager import FileManager
from tool import Tool

KV = '''
<mergePdfContentCls>:
    orientation:"vertical"
    size_hint_y:None
    height:"181dp"
    MDScreen:
        GridLayout:
            rows:2
            cols:1
            GridLayout:
                cols:2

                MDLabel:
                    text:"Merge position : "
                MDTextField:
                    hint_text:"Enter position"
                    on_text:root.app.text_ontext(self, "int")


                MDLabel:
                    text:"Pages range: "
                GridLayout:
                    cols:2
                    MDTextField:
                        hint_text:"From"
                        text: "1"
                        on_text: root.app.set(key="MergeFrom", value=self.text, forceInt=True, widget=self)
                    MDTextField:
                        hint_text:"To"
                        id:MergeTO
                        text:"end"
                        on_text: root.app.set(key="MergeTo", value=self.text)
            
            MDRaisedButton:
                text:"Browse pdf files to merge"
                theme_text_color:"Custom"
                text_color:1,1,1,1
                on_release:root.browse()

            # MDRaisedButton:
            #     text:"MERGE"
            #     theme_text_color:"Custom"
            #     text_color:1,1,1,1
            #     on_release: root.app.operate(mystr='self.mytool.merge_pdf(self.askedFiles, self.selectedDest)', operationName=self.text)


'''

Builder.load_string(KV)

class mergePdfContentCls(BoxLayout):
    def __init__(self, app, **kwargs):
        # Access all arguments of super class (BoxLayout)
        super().__init__(**kwargs)

        # Set app as an property of this class
        self.app = app
        

    def browse(self):
        # Create a instance of filemanager object
        filemanager = FileManager()

        # Ask pdf files to merge
        askedFiles = filemanager.askFiles(title="Select pdf files to merge.")

        # set askedFiles as a property of app class
        self.app.askedFiles = askedFiles
        
        




def getMergePdfDialog(app):
    dialog = MDDialog(
                    title="Merge PDF",
                    type="custom",
                    content_cls=mergePdfContentCls(app),
                    buttons=[
                        MDFlatButton(
                            text="MERGE", text_color=app.theme_cls.primary_color,
                            on_release=lambda x: app.operate(mystr="self.mytool.merge_pdf(position=self.wrote, pages=(int(self.inputData['MergeFrom'])-1, int(self.inputData['MergeTo']) if self.inputData['MergeTo'] != 'end' else 'end'), fileobjs=self.askedFiles, saveTo=self.selectedDest)", dialog=dialog, operationName=dialog.title)
                        ),
                    ],                    
                )

    return dialog
    