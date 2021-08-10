from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

style = '''
<SetOperationPages>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "50dp"

    MDTextField:
        icon_left: "book-open-page-variant"
        hint_text: "Enter page number(s)."
        on_text: app.text_ontext(self)
'''

Builder.load_string(style)


class SetOperationPages(BoxLayout):
    pass

