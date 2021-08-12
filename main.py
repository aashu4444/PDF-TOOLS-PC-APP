
from kivy.lang import Builder
from datetime import datetime
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix import screen
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.uix.screenmanager import Screen
from tkinter import filedialog as fd
import tkinter
from encrypt_pdf_dialog import *
from tool import Tool
import PyPDF2
from kivy.config import Config
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton

from set_operation_pages_dialog import SetOperationPages

from screens.featuresScreen import FeaturesScreen
from screens.homeScreen import HomeScreen
from screens.myfilesScreen import MyfilesScreen
from utils import *
import json
import json


KV = '''
GridLayout:
    cols:1
    MDToolbar:
        title:"PDF TOOLS."
    
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

        MDBottomNavigationItem:
            name: 'screen 3'
            icon: 'folder-outline'
            text:"My Files"
            id:MyFilesNav
            


'''


Config.set('graphics', 'resizable', False)

def hi(*a):
    Window.size = (380,600)

# Window.bind(on_resize = hi)

wrote = ""

root = tkinter.Tk()
root.withdraw()


sources = {}



class EncpdfScreen(Screen):
    pass


class Pdftools(MDApp):
    firstRectPosY, secondRectPosY = (170, 155)
    middleRectPosY = (firstRectPosY + secondRectPosY) - 35
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
        )
        self.wrote = "test"
        self.data = {
            "Set operation pages":"book-open-page-variant",
        }


        self.encpdfDialog = MDDialog(
                title="ENCRYPT PDF:",
                type="custom",
                content_cls=EncryptPdf(),
                buttons=[
                    MDFlatButton(
                        text="ENCRYPT", text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.operate("self.mytool.encrypt(self.wrote, self.selectedDest)",self.encpdfDialog, "ENCRYPTING PDF PLEASE WAIT...", "PDF ENCRYPTED")
                    ),
                ],
            )


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



    def text_ontext(self, widget):
        self.wrote = widget.text

    def backTo(self, screen):
        self.sm.current = screen

    def askDir(self):
        root = tkinter.Tk()
        root.withdraw()
        askedDir = fd.askdirectory()


    def build(self):
        self.theme_cls.primary_palette = "Purple"
        Window.size = (380,600)
        homescreen = HomeScreen(self)
        featuresscreem = FeaturesScreen(self)
        myfilesscreen = MyfilesScreen(self)

        self.root = Builder.load_string(KV)

        self.root.ids.HomeNav.add_widget(homescreen)
        self.root.ids.FeaturesNav.add_widget(featuresscreem)
        self.root.ids.MyFilesNav.add_widget(myfilesscreen)


        return self.root

    def onTabsSwitch(self, bottom_navigation_item, name_tab):
        print(bottom_navigation_item, name_tab)

    def operate(self, mystr, dialog=None, processText=None, completeText=None, askDir=False, operationName=None):
        settings = readSettings()
        with open("myfiles.json", "r") as f:
            data = json.loads(f.read())


        processText = toProcessText(operationName) if processText==None else processText
        completeText = toCompleteText(operationName) if completeText==None else completeText

        if askDir == False:
            if settings["default_save_folder"] == "ask_first":
                askedFile = fd.asksaveasfilename(
                        initialfile=self.srcFile.split("/")[-1].replace(".pdf", "") + "_" + operationName.replace(" ", "_") + ".pdf" if "/" in self.srcFile else self.srcFile,
                        filetypes=(
                            ("PDF Files", "*.pdf"),
                        ),
                )
                if not askedFile.endswith(".pdf"):
                    askedFile += ".pdf"

                self.selectedDest = askedFile

            else:
                name = self.srcFile.split("/")[-1].replace(".pdf", "") + "_" + operationName.replace(" ", "_") + ".pdf"

                self.selectedDest = settings["default_save_folder"] + "/" + name 

                askedFile = self.selectedDest

            fileId = data[-1]["id"] + 1 if len(data) != 0 else 1
            
            data.append({"name":askedFile, "src":askedFile, "timestamp":datetime.now().strftime("%d %B %Y at %I:%M %p"), "id":fileId})

            with open("myfiles.json", "w") as f:
                f.write(json.dumps(data))
        
        else:
            askedDir = fd.askdirectory()
            self.selectedDest = askedDir

        if dialog != None:
            dialog.dismiss()

        processDialog = MDDialog(text=processText.upper())
        completeDialog = MDDialog(text=completeText.upper())

        processDialog.open()
        eval(mystr)
        processDialog.dismiss()


        completeDialog.open()

        

    def callback(self, instance):
        if instance.icon == "book-open-page-variant":
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

            self.setOperationPagesDialog.open()


    def askFile(self, title="Select a pdf file"):
        self.filename = fd.askopenfilename(
        title=title,
        initialdir='/',
        filetypes=(("PDF Files", "*.pdf"),))

        
        if self.filename != "":
            self.srcFile = self.filename

            obj = open(self.srcFile, 'rb')
            self.reader = PyPDF2.PdfFileReader(obj)

            try:
                writer = PyPDF2.PdfFileWriter()

                for i in range(self.reader.getNumPages()):
                    writer.addPage(self.reader.getPage(i))

                Tool.pdf_writer = writer
                Tool.pages = list(range(self.reader.getNumPages()))

                self.mytool = Tool(self.srcFile)

                # self.file_manager.show("/")
                self.manager_open = True

                self.root.ids.Navigator.switch_tab("FeaturesTab")


                self.select_path(self.filename)

            except PyPDF2.utils.PdfReadError as e:
                if "File has not been decrypted" == str(e):
                    Tool.requested_pages = ["all"]
                    self.mytool = Tool(self.srcFile)

                    self.sm.current = "Features"

            

    def select_path(self, path):
        self.path = path

    def setOperationPages(self, pagesStr):
        ls = []
        splitted = pagesStr.split(",")
        for i in splitted:
            if "-" in str(i):
                ls.extend(list(range(int(i.split("-")[0]) - 1, int(i.split("-")[1]))))
            else:
                ls.append(int(i) - 1)


        writer = PyPDF2.PdfFileWriter()



        for i in ls:
            writer.addPage(self.reader.getPage(i))

        Tool.pdf_writer = writer
        Tool.pages = ls
        Tool.requested_pages = ls

        self.setOperationPagesDialog.dismiss()

        toast(text="Operation pages set successfully!")

        print(ls)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


app = Pdftools()

app.run()