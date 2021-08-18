
from kivymd.uix.card import MDCard
from kivy.lang import Builder

kv = """
<RoundedCornersCard>:
    ripple_behavior:True
    orientation: "vertical"
    canvas:
        Color:
            rgb: 255/255, 255/255, 255/255
        RoundedRectangle:
            size:(self.size[0] + 20, self.size[1] + 20)
            pos:(self.pos[0] - 10, self.pos[1] - 10)
            
            radius: (25,25,25,25)
"""

Builder.load_string(kv)

class RoundedCornersCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
