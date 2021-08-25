
from kivymd.uix import dialog, label
from kivymd.uix import selectioncontrol
from kivymd.uix.behaviors import elevation
from kivymd.uix.button import MDFlatButton

from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.color_definitions import theme_colors
import json
from kivy.properties import StringProperty
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.card import MDSeparator
from kivymd.uix.boxlayout import MDBoxLayout
from dialogs.deleteMyFileDialog import deleteMyFileDialog
from dialogs.deleteSelectedMyFiles import deleteSelectedMyFilesDialog
from dialogs.myfilesdetails import getOperationFileDetailsDialog
from RoundedCornersCard import RoundedCornersCard

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch

from utils import *
from widgets.myscrollview import MyScrollView


class Container(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True

class MyfilesScreen(MyScrollView):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.cols = 1

        self.app = app

        self.mdls = MDList(spacing=40)
        self.pos_hint = {"top":1}

    
        self.add_widget(self.mdls)




        # Checkbox on card footer
        self.selectedFiles = []

        # All checkboxes
        self.checkboxes = []

        self.updateFiles()

    def openDeleteSelectedMyFilesDialog(self):
        dialog = deleteSelectedMyFilesDialog(self.app, self)
        dialog.open()


    def setToDict(self, key, value):
        """
        set a key value pair in cardCheckboxes
        """

        self.cardCheckboxes[key] = value

    def onCheck(self, widget):
        # Toolbar of application
        toolbar = self.app.root.ids.AppToolbar

    
        # List of the state of all checkboxes
        statesLs = []
        

        # Iterate through all checkboxes
        for checkbox in self.cardCheckboxes:
            # Append current checkbox's state to the stateLs
            statesLs.append(checkbox.state)


        # If user checks the checkbox
        if widget.state == "down":            
            # If there are only checkbox in toolbar then add delete button in the toolbar
            if len(toolbar.right_action_items) == 1:
                toolbar.right_action_items.append(["trash-can-outline", lambda x: self.app.onToolbarTrashCanClick(x)])
            

            # If all checkboxes are checked then check the checkbox that is in toolbar
            if "normal" not in statesLs:
                self.app.action_checkbox.check()

        
        # If user unchecks the checkbox
        else:
            # if user unchecks all selected files then remove the delete button from toolbar's right action items
            if len(self.selectedFiles) == 0:
                toolbar.right_action_items = [["checkbox-blank-outline", lambda x: self.app.toggleCheckAll(x)]]

            
            # If all checkboxes are not check then uncheck the checkbox that is in toolbar
            if "normal" in statesLs:
                self.app.action_checkbox.uncheck(False)

    def NoFilesAvailable(self):
        card = RoundedCornersCard(orientation="vertical",size_hint=(0.8, None),height="230dp",padding= "10dp",pos_hint={"center_x":.5, "center_y":.5})
        layout = GridLayout(cols=1)
        headerIcon = MDIcon(icon="emoticon-sad-outline", halign="center")
        heading = MDLabel(text="Oops!", font_style="H2", halign="center") 

        message = MDLabel(text="Please upload a pdf file to view features!",font_style="Button",halign="center")

        layout.add_widget(headerIcon)
        layout.add_widget(heading)
        layout.add_widget(message)
        card.add_widget(layout)

        return card


    def updateFiles(self):

        self.cardCheckboxes = {}
        self.selectedFiles = []
        self.mdls.clear_widgets()

        myfiles = ReadMyFiles()

        mylabel = MDLabel(text="You have deleted available files!", halign="center")

        # If there are no files then remove actions from toolbar
        if len(myfiles) == 0:
            # Remove all action items from toolbar
            emptyToolbarActions(self.app)

            # Create a rounded corners card to show message (No files available!)
            roundedCorsCard = RoundedCornersCard(orientation="vertical",size_hint=(0.8, None),height="230dp",padding= "10dp",elevetion=12,pos_hint={"center_x":.5, "center_y":.5})


            # The main layout of the card (roundedCorsCard)
            gLayout = GridLayout(cols=1)


            # Add an icon to show on the card (roundedCorsCard)
            gLayout.add_widget(MDIcon(icon="emoticon-sad-outline",halign="center"))


            # add title of the message to the card (roundedCorsCard)
            gLayout.add_widget(MDLabel(text="No files available!",font_style="H4",halign="center"))


            # Add desc of the message to the card (roundedCorsCard)
            gLayout.add_widget(MDLabel(text="You have no operated pdf files! Your opereated pdf files will shown here!",font_style="Button",halign="center"))


            # Add the main grid layout (gLayout) to the card (roundedCorsCard)
            roundedCorsCard.add_widget(gLayout)


            # Add the card (roundedCorsCard) to the UI
            self.app.root.ids.MyFilesNav.add_widget(roundedCorsCard)


            # set the card (roundedCorsCard) as a property of this class to use from other classes
            self.NoFilesAvailableMSG = roundedCorsCard


            
            try:
                self.app.root.ids.MyFilesNav.remove_widget(self)
            except Exception as e:
                self.app.root.ids.MyFilesNav.remove_widget(roundedCorsCard)


        
        # If there are any file(s) then show them in a list
        else:
            for file in myfiles:
                filename = truncate(file.get("name").split("/")[-1], 30)

                src = truncate(file.get("src"), 35)
                timestamp = file.get("timestamp")
                id = file.get('id')


                box_1 = MDBoxLayout(size_hint_y=None, height=80)
                icon = MDIcon(icon="folder", size_hint_x=0.2, halign="center")
                filesDetailLayout = GridLayout(rows=2)
                filenameLabel = MDLabel(text=f"{filename}\n{src}")
                # filesrcLabel = MDLabel(theme_text_color="Secondary", text=src)
                filesDetailLayout.add_widget(filenameLabel)
                # filesDetailLayout.add_widget(filesrcLabel)
                box_1.add_widget(icon)
                box_1.add_widget(filesDetailLayout)

                # Second box of the card
                box_2 = MDBoxLayout(size_hint_y=None, height=40)
                operationName = file.get("operationName")
                operationNameWidget = MDLabel(text=f"Operation : {operationName}", halign="right")
                box_2.add_widget(operationNameWidget)

                box_3 = MDBoxLayout(size_hint_y=None, height=40)
                

                card = MDCard(orientation="vertical",size_hint=(.5, None), height=(box_1.height + box_2.height + box_3.height), padding="8dp", elevation=5)

                # Operation time of the file
                timeStampLabel = MDLabel(text=timestamp, halign="right")

                # Add checkbox on the card's footer
                checkbox = MDCheckbox(size_hint=(None, None), size=("48dp", "48dp"), on_press=lambda x:self.selectedFiles.append(x) if x.state == "down" else self.selectedFiles.remove(x), pos_hint={"center_x":.5, "center_y":.5}, on_release=lambda y: self.onCheck(y))
                box_3.add_widget(checkbox)


                box_3.add_widget(timeStampLabel)


                card.add_widget(box_1)
                card.add_widget(MDSeparator())
                card.add_widget(box_2)
                card.add_widget(MDSeparator())
                card.add_widget(box_3)

                self.mdls.add_widget(card)

                # Append the checkbox to checkboxes list of this class
                self.checkboxes.append(checkbox)

                self.cardCheckboxes[checkbox] = file





