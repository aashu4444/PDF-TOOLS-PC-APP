from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

style = '''
<EncryptPdf>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "50dp"

    MDTextField:
        icon_left: "key-variant"
        hint_text: "Enter password to set."
        on_text: app.text_ontext(self)
        password: True
'''

Builder.load_string(style)


class EncryptPdf(BoxLayout):
    pass

