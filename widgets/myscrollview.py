from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class MyScrollView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        def setScrollView():
            self.size_hint = (1, None)
            self.size=(Window.width, Window.height - 120)  
        
        setScrollView()  

        Window.bind(on_resize=lambda a,b,c:setScrollView())  
