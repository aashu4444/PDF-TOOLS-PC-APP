
from kivymd.uix.card import MDCard
from kivy.lang import Builder

kv = """
<RoundedCornersCard>:
    ripple_behavior:True
    orientation: "vertical"
    size_hint_x: 0.8
    size_hint_y:1
    elevation: 20
    canvas:
        Color:
            rgb: 255/255, 255/255, 255/255
        RoundedRectangle:
            size:(self.size[0] + 20, 80)
            pos:(self.pos[0] - 10, self.pos[1] - 6)
            
            radius: (25,25,25,25)
"""

Builder.load_string(kv)

class RoundedCornersCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
