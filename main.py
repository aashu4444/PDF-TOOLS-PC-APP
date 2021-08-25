# Imports from kivy
from tkinter.constants import E
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.config import Config
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.animation import AnimationTransition

# Imports from kivymd
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.bottomnavigation import MDBottomNavigation

# Screens
from screens.featuresScreen import FeaturesScreen
from screens.homeScreen import HomeScreen
from screens.myfilesScreen import MyfilesScreen

# Other imports
# datetime - for getting date
from datetime import datetime

# filedialog - to open dialogs
from tkinter import filedialog as fd 
import tkinter

# Some utility functions
from utils import *

from encrypt_pdf_dialog import *

# To operate a pdf file
from tool import Tool

# To operate a pdf file
import PyPDF2

# Dialog
from set_operation_pages_dialog import SetOperationPages
from dialogs.deleteSelectedMyFiles import deleteSelectedMyFilesDialog

import json

import time


from classes.ActionCheckBox import ActionCheckBox

# The kv file of app
KV = '''
GridLayout:
    cols:1
    MDToolbar:
        id:AppToolbar
        title:"PDF TOOLS."
        right_action_items: []
    
    MDBottomNavigation:
        panel_color: 156/255, 39/255, 176/255, 1
        id:Navigator

        text_color_active: 1, 1, 1, 0.9
        text_color_normal: 1, 1, 1, 0.5

        MDBottomNavigationItem:
            name: 'screen 1'
            icon: 'home-outline'
            text:"Home"
            id:HomeNav
            

        MDBottomNavigationItem:
            name: 'FeaturesTab'
            icon: 'format-list-text'
            text:"Features"
            id:FeaturesNav

            RoundedCornersCard:
                id:UploadInstruction
                orientation:"vertical"
                size_hint:(0.8, None)
                height:"230dp"
                padding: "10dp"
                pos_hint:{"center_x":.5, "center_y":.5}

                GridLayout:
                    cols:1
                    MDIcon:
                        icon:"emoticon-sad-outline"
                        text_size:(250,250)
                        halign:"center"
                    MDLabel:
                        text:"Oops!"
                        font_style:"H2"
                        halign:"center"
                    MDLabel:
                        text:"Please upload a pdf file to view features!"
                        font_style:"Button"
                        halign:"center"
                

        MDBottomNavigationItem:
            name: 'screen 3'
            icon: 'folder-outline'
            text:"My Files"
            id:MyFilesNav
            
            on_tab_press: app.toggleRightActionItems(1) if len(app.ReadMyFiles()) != 0 else lambda x:None
            on_leave: app.toggleRightActionItems(0)

            RoundedCornersCard:
                id:NoFilesAvailableMessage
                orientation:"vertical"
                size_hint:(0.8, None)
                height:"230dp"
                padding: "10dp"
                elevetion:12
                pos_hint:{"center_x":.5, "center_y":.5}

                GridLayout:
                    cols:1
                    MDIcon:
                        icon:"emoticon-sad-outline"
                        halign:"center"
                    MDLabel:
                        text:"No files available!"
                        font_style:"H4"
                        halign:"center"
                    MDLabel:
                        text:"You have no operated pdf files! Your opereated pdf files will be shown here!"
                        font_style:"Button"
                        halign:"center"
            


'''

from dialogs.mergePdfDialog import getMergePdfDialog



def hi(*a):
    Window.size = (380,600)

# Window.bind(on_resize = hi)


# This will change when user will type something on any text field
wrote = ""


# Remove tkinter window
root = tkinter.Tk()
root.withdraw()



class EncpdfScreen(Screen):
    pass


class Pdftools(MDApp):

    # This function will run when any instance of this class will create.
    def __init__(self, **kwargs):

        # Accept all arguments from super class(MDApp)
        super().__init__(**kwargs)

        
        self.wrote = ""
        self.ReadMyFiles = ReadMyFiles

        # The data of speedDial btn
        self.data = {
            "Set operation pages":"book-open-page-variant",
        }



        # Dialog to encrypt pdf
        self.encpdfDialog = MDDialog(
                title="ENCRYPT PDF:",
                type="custom",
                content_cls=EncryptPdf(),
                buttons=[
                    MDFlatButton(
                        text="ENCRYPT", text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.operate(mystr="self.mytool.encrypt(self.wrote, self.selectedDest)",dialog=self.encpdfDialog, processText="ENCRYPTING PDF PLEASE WAIT...", completeText="PDF ENCRYPTED", operationName="Encrypt PDF")
                    ),
                ],
            )

        # Data of input fill will set here
        self.inputData = {"MergeFrom":0, "MergeTo":"end"}


        # Dialog to decrypt pdf
        self.decryptpdfDialog = MDDialog(
                title="DECRYPT PDF:",
                type="custom",
                content_cls=EncryptPdf(),
                buttons=[
                    MDFlatButton(
                        text="DECRYPT", text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.operate(mystr="self.mytool.decrypt(self.wrote, self.selectedDest)", operationName="DECRYPT PDF", dialog=self.decryptpdfDialog)
                    ),
                ],
            )

        


    # This function will call when user type something on a text field
    def text_ontext(self, widget):
        # Change wrote property to the text of text field
        self.wrote = widget.text

    def set(self, key, value):
        """
        Sets a key,value pair in inputData var of the app.
        """
        self.inputData[key] = value

    # This function will call when the run method of this class is called
    def build(self):
        # Change theme color to purple
        self.theme_cls.primary_palette = "Purple"

        # Read my files
        self.myfiles = ReadMyFiles()

        # Change size of window
        Window.size = (380,600)

        # Create a home screen
        homescreen = HomeScreen(self)
        self.homescreen = homescreen


        # Create a my file screen
        # myfilesscreen = MyfilesScreen(self)
        # self.myfilesscreen = myfilesscreen

        # Load the kv file
        self.root = Builder.load_string(KV)

        # Add all screen as the content of bottomnavigation's nav content
        self.root.ids.HomeNav.add_widget(homescreen)
        
        # If there are some file in myfiles.json then show them
        # if len(self.myfiles) != 0:
        #     self.root.ids.MyFilesNav.remove_widget(self.root.ids.NoFilesAvailableMessage)
        #     self.root.ids.MyFilesNav.add_widget(myfilesscreen)


        self.action_checkbox = ActionCheckBox(self)

        self.namessage = self.root.ids.NoFilesAvailableMessage

        # Return the loaded kv
        return self.root

    def operate(self, mystr, dialog=None, processText=None, completeText=None, askDir=False, operationName=None):
        """
        To operate a pdf file
        mystr: the python code to evaluate
        dialog: any other dialog to close
        processText: text to show when a operation is in progress
        completeText: text to show when a operation is completed
        askDir: to open a fd.askdirectory() dialog
        operationName: the name of operation
        """


        # Read the settings files
        settings = readSettings()
        with open("myfiles.json", "r") as f:
            data = json.loads(f.read())

        
        # Get process text from operation name
        processText = toProcessText(operationName) if processText==None else processText

        # Get complete text from operation name
        completeText = toCompleteText(operationName) if completeText==None else completeText

        # The default name to show in filedialog
        initialName = self.srcFile.split("/")[-1].replace(".pdf", "") + "_" + operationName.replace(" ", "_") + ".pdf" if "/" in self.srcFile else self.srcFile

        # If user want to ask a pdf file
        if askDir == False:
            # ask a pdf file if default_save_folder in settings is set to "ask_first"
            if settings["default_save_folder"] == "ask_first":
                # Ask the pdf file
                askedFile = fd.asksaveasfilename(
                        initialfile=initialName,
                        filetypes=(
                            ("PDF Files", "*.pdf"),
                        ),
                )

                if askedFile != "":
                    # if the user not type extension then add it
                    if not askedFile.endswith(".pdf"):
                        askedFile += ".pdf"


                    # Set the app's selected destination to askedFile
                    self.selectedDest = askedFile

                else:
                    self.selectedDest = None

            # if the folder path in aleready set in default_save_folder in settings. so get the path
            else:
                # Set the app's selected destination to default_save_folder
                self.selectedDest = settings["default_save_folder"] + "/" + initialName 

                # Set the asked file to selected destination
                askedFile = self.selectedDest

            # Continue the code if user selected a pdf file
            if askedFile != "":
                # Create the id for current pdf file
                fileId = data[-1]["id"] + 1 if len(data) != 0 else 1

                
                # Add the data of current pdf file to data variable
                data.append({"name":self.srcFile, "src":askedFile, "timestamp":datetime.now().strftime("%d %B %Y at %I:%M %p"), "operationName":operationName ,"id":fileId})

                # Write the data to myfiles.json
                with open("myfiles.json", "w") as f:
                    f.write(json.dumps(data))

                
                # Add the new files screen to the myfiles tab because now a operated file is available!
                updateMyFiles(self)
        
        # If user wants to ask a directory
        else:
            if settings["default_save_folder"] == "ask_first":
                # Ask directory
                askedDir = fd.askdirectory()
            
            else:
                askedDir = settings["default_save_folder"]

            # Set the app's selected destination to askedDir
            self.selectedDest = askedDir if askedDir != "" else None


        # Continue if user selected a pdf file
        if self.selectedDest != None:
            # If there are any dialog to close then close it
            if dialog != None:
                dialog.dismiss()

            # Dialog to show when the operation is in process
            processDialog = MDDialog(text=processText.upper())

            # Dialog to show when the operation is completed
            completeDialog = MDDialog(text=completeText.upper())

            # Open the processDialog
            processDialog.open()

            # Start operating the pdf file
            eval(mystr)

            # If user is extracting images from pdf
            if "extract_images" in mystr.lower():
                fileId = data[-1]["id"] + 1 if len(data) != 0 else 1

                WriteMyFiles(data={"name":self.selectedDest, "src":self.selectedDest, "timestamp":datetime.now().strftime("%d %B %Y at %I:%M %p"), "operationName":operationName ,"id":fileId, "srcImages":Tool.dstImages}, append=True)

            updateMyFiles(self)

            processDialog.dismiss()


            # Open the completeDialog
            completeDialog.open()

        

    def callback(self, instance):
        """
        Called when user click on a button of speedDialBtn
        """

        # If user wants to set operation pages
        if instance.icon == "book-open-page-variant":
            
            # Create a setOperationPagesDialog dialog
            self.setOperationPagesDialog =  MDDialog(
                title="Set operation pages:",
                type="custom",
                content_cls=SetOperationPages(),
                buttons=[
                    MDRaisedButton(
                        text="SET OPERATION PAGES",
                        on_release=lambda x: self.setOperationPages(self.wrote)
                    ),
                ],
            )


            # Open the setOperationPagesDialog
            self.setOperationPagesDialog.open()



    def askFile(self, widget, title="Select a pdf file"):
        """
        Open a dialog to upload a pdf file
        title: Title of the dialog
        """

        # Ask the pdf file
        self.filename = fd.askopenfilename(
        title=title,
        initialdir='/',
        filetypes=(("PDF Files", "*.pdf"),))


        
        # If user selects a pdf file
        if self.filename != "":
            # Set the app's property srcFile to asked file's name
            self.srcFile = self.filename

            # Open the uploaded file in read binary mode
            obj = open(self.srcFile, 'rb')

            # Create a pdf file reader with obj
            self.reader = PyPDF2.PdfFileReader(obj)


            try:
                # Create a pdf file writer
                writer = PyPDF2.PdfFileWriter()

                # Copy all pages from reader to writer
                for i in range(self.reader.getNumPages()):
                    writer.addPage(self.reader.getPage(i))

                # set the writer as a property of Tool object
                Tool.pdf_writer = writer

                # set pages of the uploaded file as a property of Tool object
                Tool.pages = list(range(self.reader.getNumPages()))

                # Set the open file obj as a property of Tool object
                Tool.obj = obj


                # Create an instance of Tool object
                self.mytool = Tool(self.srcFile)

                # Set the pdf reader object as a property of mytool
                self.mytool.pdf_reader = self.reader

                # Switch the currently opened tab from home to features
                self.root.ids.Navigator.switch_tab("FeaturesTab")


                self.select_path(self.filename)


            except PyPDF2.utils.PdfReadError as e:
                # If the file is encrypred
                if "File has not been decrypted" == str(e):
                    # Set pages to all
                    Tool.requested_pages = ["all"]

                    # Create an instance of Tool object
                    self.mytool = Tool(self.srcFile)

                    # Switch the currently opened tab from home to features
                    self.root.ids.Navigator.switch_tab("FeaturesTab")



            # Change text of a label that contains the file name of currently uploaded file
            currentFileName = self.srcFile.split("/")[-1] if "/" in self.srcFile else self.srcFile
            self.homescreen.currentlyUploadedText.text = f"Currently : {truncate(currentFileName, 30)}"

            # Remove instructions from the features tab and show features
            try:
                self.root.ids.FeaturesNav.remove_widget(self.root.ids.UploadInstruction)

                # Create a features screen
                featuresscreen = FeaturesScreen(self)
                
                # Show features on features tab
                self.root.ids.FeaturesNav.add_widget(featuresscreen)
                
            except Exception as e:
                pass
            

    def toggleRightActionItems(self, code):
        """
        Called when user opens the my file tab.

        This function show the right action items of toolbar when user opens the myfiles tab and hides these item when user leaves the tab.

        Also this function create a myfilesscreen and adds to the app if the screen not exists.

        code: 1 to show and 0 to hide
        """

        # If there are no items in toolbar then add item
        if code == 1:
            # Add the right action items to the toolbar
            self.action_checkbox.show()


            # Try to access myfilesscreen, if not exists then create it
            try:
                self.myfilesscreen

                # if myfilesscreen is accesible then check that the user's operated files are available
                if len(ReadMyFiles()) != 0:
                    # Remove the No Files available message because there are some files are available to show
                    self.root.ids.MyFilesNav.clear_widgets()

                    # Add available files to the UI
                    self.root.ids.MyFilesNav.add_widget(self.myfilesscreen)




            except Exception as e:
                # Create a instance of myfilesscreen
                self.myfilesscreen = MyfilesScreen(self)

                # Add the myfilesscreen to the root and remove the message if there are some operated file.
                if len(ReadMyFiles()) != 0:
                    self.root.ids.MyFilesNav.clear_widgets()
                    self.root.ids.MyFilesNav.add_widget(self.myfilesscreen)


        # If there are some items in toolbar then hide then
        else:
            self.action_checkbox.hide()




    def select_path(self, path):
        self.path = path

    def setOperationPages(self, pagesStr):
        """
        Function to set operation pages globally
        pagesStr: pages that entered by user(e.x. - 1,2,5-8)
        """

        # Create a blank list of pages
        ls = []

        # Split each page number by ,
        splitted = pagesStr.split(",")

        # Iterate through splitted numbers
        for i in splitted:
            # If current item is a range of pages
            if "-" in str(i):
                # merge a list of unpacked range into ls
                ls.extend(list(range(int(i.split("-")[0]) - 1, int(i.split("-")[1]))))
            else:
                # Add the page number to ls
                # Note: 1 is subtracted from current page number because page index starts with 0
                ls.append(int(i) - 1)


        # Create a blank writer object
        writer = PyPDF2.PdfFileWriter()


        # Iterate through pages that is entered by user
        for i in ls:
            # Add current page to writer object
            writer.addPage(self.reader.getPage(i))

        # Set writer object as a property of Tool object
        Tool.pdf_writer = writer

        # Set ls as a property of Tool object
        Tool.pages = ls


        # Set requested_pages as a property of Tool object
        Tool.requested_pages = ls


        # Close the currently opened setOperationPagesDialog
        self.setOperationPagesDialog.dismiss()

        # Show a success message
        toast(text="Operation pages set successfully!")

    def toggleCheckAll(self, widget):
        """
        This will call when user wants to select all items in myfiles tab.
        """
        toolbar = self.root.ids.AppToolbar

        # If checkbox is check then uncheck it
        if len(self.myfilesscreen.selectedFiles) != 0 :
            toolbar.right_action_items = [["checkbox-blank-outline", lambda x: self.toggleCheckAll(x)]]

            self.myfilesscreen.selectedFiles = []

            for i in self.myfilesscreen.cardCheckboxes:
                i.active = False
                
        
        # if checkbox is not checked then check it
        else:            
            toolbar.right_action_items = [["checkbox-marked-outline", lambda x: self.toggleCheckAll(x)], ["trash-can-outline", lambda x: self.onToolbarTrashCanClick(x)]]

            self.myfilesscreen.selectedFiles = []

            for i in self.myfilesscreen.checkboxes:
                i.active = True

                self.myfilesscreen.selectedFiles.append(i)

    def onToolbarTrashCanClick(self, widget):
        """
        Called with user click on trash-can-outline icon on the toolbar.
        """
        dialog = deleteSelectedMyFilesDialog(app)
        dialog.open()



# Create an instance of app
app = Pdftools()


# Run app
app.run()
