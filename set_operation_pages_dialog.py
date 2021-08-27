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
        id:OperationPagesInp
        icon_left: "book-open-page-variant"
        hint_text: "Enter page number(s)."
        on_text: app.text_ontext(self, "int")
        helper_text: "Enter valid page"
        helper_text_mode: "on_error"
'''

Builder.load_string(style)


class SetOperationPages(BoxLayout):
    pass

